#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  scan_converter.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  Version 0.2: 22 May 2014
#    -Error in CVSS score calculation (now weighted at end, not on the fly)
#    -Removed duplicate IPs in Affected Systems
#    -Changed CRLF to <br> to support MyState v2
#    -Created CVSS column to output - used in CVSS calculator
#    -Added color to output, because it's fun
#
#  Version 0.3: 28 October 2014
#   -Added byipsheet(xlsxFile) to create a second ws in the book to put in results by IP
#   -Added Port and CVE column on byIP sheet
#   -Changed <br> to CRLF since this sheet is not being used on portal
#
#  Version 0.3.1: April 2015
#   - Updated qualys_csv to handle the Qualys CVSS Base output change in their csv files
#   - Made a check for cvss_base in Qualys to prevent NoneType errors
#
#  Version 1.0.0 November 2015
#   - Rewrote to use OOP, support multiple input files and Python 3
#
#  Version 1.1.0 November 2015
#   - Added support for importing from openvas
#


from __future__ import print_function

import argparse
import collections
import csv
import os
import re
import shlex
import sys
import xml.etree.ElementTree as ET

import xlsxwriter
from smoke_zephyr.utilities import parse_server

__version__ = '1.1.0'

# Export to:
# Title, Vulnerability Description, Knowledge Level, Vulnerability Rating, Recommendation(s), Affected Systems

VULNERABILITY_RATINGS_TO_CVSS = {'high':7, 'medium':3, 'low':0}
VULNERABILITY_RATING_UNKNOWN = -1

def annotate(prop_name, prop_value):
	def _annotate(function):
		setattr(function, prop_name, prop_value)
		return function
	return _annotate

class Vulnerability(collections.namedtuple('_Vulnerability', ('uid', 'title', 'description', 'recommendations', 'cve', 'cvss', 'affected_systems'))):
	@property
	def rating(self):
		return cvss_to_vulnerability_rating(self.cvss)

def cvss_to_vulnerability_rating(score):
	rating = '(0) Unknown'
	if score == VULNERABILITY_RATING_UNKNOWN:
		return rating
	score = float(score)
	if score < 3:
		rating = '(1) Low'
	elif score < 7:
		rating = '(2) Medium'
	elif score <= 11:
		rating = '(3) High'
	return rating

class ScanConverter(object):
	def __init__(self, minimum_cvss):
		self.vulnerabilities = {}
		self.minimum_cvss = minimum_cvss

	def export_to_xlsx(self, file_name):
		workbook = xlsxwriter.Workbook(file_name)
		worksheet = workbook.add_worksheet('Results By Vulnerability')
		for column, text in enumerate(('Title', 'Vulnerability Description', 'Vulnerability Rating', 'Recommendation(s)', 'CVSS', 'Affected Systems')):
			worksheet.write(0, column, text)
		unique_systems = []
		for row, vuln in enumerate(self.vulnerabilities.values(), 1):
			for system in vuln.affected_systems:
				system, _ = parse_server(system, 0)
				if system not in unique_systems:
					unique_systems.append(system)
			for column, text in enumerate((vuln.title, vuln.description, vuln.rating, vuln.recommendations, vuln.cvss, ' '.join(vuln.affected_systems))):
				worksheet.write(row, column, text)
		unique_systems.sort()
		worksheet = workbook.add_worksheet('Results By Host')
		for column, text in enumerate(('Host', 'Port', 'CVE', 'Title', 'Vulnerability Description', 'Vulnerability Rating', 'Recommendation(s)', 'CVSS')):
			worksheet.write(0, column, text)
		row = 1
		for system in unique_systems:
			for vuln in self.vulnerabilities.values():
				affected = False
				for affected_system in vuln.affected_systems:
					affected_system = parse_server(affected_system, 0)
					if affected_system[0] == system:
						affected = True
						system = affected_system
						break
				if not affected:
					continue
				for column, text in enumerate((system[0], system[1], vuln.cve, vuln.title, vuln.description, vuln.rating, vuln.recommendations, vuln.cvss)):
					worksheet.write(row, column, text)
				row += 1
				system = system[0]
		workbook.close()

	def get_importer(self, in_h):
		data = in_h.read(16)
		extension = os.path.splitext(in_h.name)[1]
		handler = None
		if extension == '.csv':
			if re.match('^"?Scan Results"?,', data):
				handler = self.qualys_csv
			elif data == 'IP,Hostname,Port':
				handler = self.openvas_csv
			elif data == 'Plugin ID,CVE,CV':
				handler = self.nessus_csv
		in_h.seek(0, os.SEEK_SET)
		return handler

	def import_file(self, in_h):
		handler = self.get_importer(in_h)
		count = 0
		for vuln in handler(in_h):
			if vuln.cvss < self.minimum_cvss:
				continue
			count =+ 1
			if vuln.uid in self.vulnerabilities:
				self.vulnerabilities[vuln.uid].affected_systems.extend(vuln.affected_systems)
			else:
				self.vulnerabilities[vuln.uid] = vuln
		return count

	@annotate('name', 'Nessus CSV')
	def nessus_csv(self, in_h):
		in_h = csv.DictReader(in_h)
		columns = in_h.fieldnames
		for row in in_h:
			if len(row) != len(columns):
				break
			solution = 'N/A'
			if row['Solution']:
				solution = row['Solution'].replace('\n', '<br>')
			system = row['Host']
			if row['Port']:
				system = system + ':' + row['Port']
			cvss_base = float(row['CVSS'] or VULNERABILITY_RATING_UNKNOWN)
			cve_id = row['CVE']
			description = row['Synopsis'] + ' ' + row['Description']
			description = ' '.join(description.split())
			description = description.replace('\n', '<br>')
			if cvss_base >= 0:
				description += "<br><br>CVE ID: {0}<br>CVSSv2 Base Score: {1}".format((cve_id or 'Unknown'), cvss_base)
			yield Vulnerability(
				uid='Nessus-' + row['Plugin ID'],
				title=row['Name'],
				description=description,
				recommendations=solution,
				cve=cve_id,
				cvss=cvss_base,
				affected_systems=[system]
			)

	@annotate('name', 'OpenVAS CSV')
	def openvas_csv(self, in_h):
		in_h = csv.DictReader(in_h)
		columns = in_h.fieldnames
		for row in in_h:
			if len(row) != len(columns):
				break
			if row['Severity'] == 'Log':
				continue
			solution = 'N/A'
			if row['Solution']:
				solution = row['Solution'].replace('\n', '<br>')
			system = row['IP']
			if row['Port']:
				system = system + ':' + row['Port']
			cvss_base = float(row['CVSS'] or VULNERABILITY_RATING_UNKNOWN)
			cve_id = row['CVEs']
			if cve_id:
				cve_id = cve_id[1:-1]
				cve_id = cve_id.split(', ')[0]
			description = row['Summary']
			description = ' '.join(description.split())
			description = description.replace('\n', '<br>')
			if cvss_base >= 0:
				description += "<br><br>CVE ID: {0}<br>CVSSv2 Base Score: {1}".format((cve_id or 'Unknown'), cvss_base)
			yield Vulnerability(
				uid='OpenVAS-' + row['NVT OID'],
				title=row['NVT Name'],
				description=description,
				recommendations=solution,
				cve=cve_id,
				cvss=cvss_base,
				affected_systems=[system]
			)

	@annotate('name', 'Qualys CSV')
	def qualys_csv(self, in_h):
		for _ in range(0, 7):
			in_h.readline()
		in_h = csv.DictReader(in_h)
		columns = in_h.fieldnames
		for row in in_h:
			if len(row) != len(columns):
				break
			solution = 'N/A'
			if row['Solution']:
				solution = row['Solution'].replace('\n', '<br>')
			system = row['IP']
			if row['Port']:
				system = system + ':' + row['Port']
			cvss_base = str(row['CVSS Base'] or VULNERABILITY_RATING_UNKNOWN)
			if ' ' in cvss_base:
				cvss_base = float(cvss_base.split(' ', 1)[0])
			else:
				cvss_base = float(cvss_base)
			cve_id = row['CVE ID']
			description = (row['Threat'] or '').replace('\n', '<br>')
			if cvss_base >= 0:
				description += "<br><br>CVE ID: {0}<br>CVSSv2 Base Score: {1}".format((cve_id or 'Unknown'), cvss_base)
			yield Vulnerability(
				uid='Qualys-' + str(row['QID']) or '0',
				title=row['Title'],
				description=description,
				recommendations=solution,
				cve=cve_id,
				cvss=cvss_base,
				affected_systems=[system]
			)

def main():
	parser = argparse.ArgumentParser(description='Scan Converter', conflict_handler='resolve')
	parser.add_argument('output', help='file to write converted results to')
	parser.add_argument('scan_files', type=argparse.FileType('r'), nargs='+', help='file with exported scan data')
	parser.add_argument('-v', '--version', action='version', version=parser.prog + ' Version: ' + __version__)
	parser.add_argument('-m', '--minimum-rating', dest='minimum_rating', action='store', default='', choices=('LOW', 'MEDIUM', 'HIGH', 'EXTREME'), help='the miniumum vulnerability rating')
	arguments = parser.parse_args()
	
	if not arguments.output.endswith('.xlsx'):
		print('[-] xlsx must be file type for output! scan_converter.py <output>.xlsx <input(s)>.csv')
		return 0
	
	minimum = VULNERABILITY_RATINGS_TO_CVSS.get(arguments.minimum_rating.lower(), 0)
	converter = ScanConverter(minimum)
	for scan_file in arguments.scan_files:
		importer = converter.get_importer(scan_file)
		if importer is None:
			print('[-] failed to identify file ' + scan_file.name)
			continue
		print("[*] loading {0} file {1}...".format(importer.name, scan_file.name), end='')
		converter.import_file(scan_file)
		print(' done')
		scan_file.close()

	print("[*] writing {0:,} vulnerabilities to xlsx file: {1}...".format(len(converter.vulnerabilities), arguments.output), end='')
	converter.export_to_xlsx(arguments.output)
	print(' done')
	return 0

if __name__ == '__main__':
	main()
