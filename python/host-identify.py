#!/usr/bin/env python3

import argparse
import datetime
import difflib
import os
import socket
import sys
import webbrowser

try:
    import netaddr
except ImportError:
    print('You need to install the "netaddr" module. Run: pip install netaddr')
    sys.exit(1)


def iter_ips_from_range(spec):
    spec = spec.strip()
    if '/' in spec:
        try:
            return (str(ip) for ip in netaddr.IPNetwork(spec))
        except netaddr.core.AddrFormatError:
            print('Invalid CIDR: ' + spec)
            sys.exit(1)
    if '-' in spec:
        left, right = spec.split('-', 1)
        left = left.strip()
        right = right.strip()
        if '.' not in right:
            parts = left.split('.')
            if len(parts) != 4:
                print('Invalid range: ' + spec)
                sys.exit(1)
            parts[-1] = right
            right = '.'.join(parts)
        try:
            return (str(ip) for ip in netaddr.iter_iprange(left, right))
        except netaddr.core.AddrFormatError:
            print('Invalid IP range: ' + spec)
            sys.exit(1)
    try:
        netaddr.IPAddress(spec)
        return iter([spec])
    except netaddr.core.AddrFormatError:
        print('Bad input: ' + spec)
        sys.exit(1)


def resolve_ip(ip):
    try:
        host = socket.gethostbyaddr(ip)[0]
        return f'{ip} - {host}'
    except Exception:
        return None


def scan_ips(ip_iter, outfile_path, verbose):
    total = 0
    resolved = 0
    with open(outfile_path, 'w') as out:
        for ip in ip_iter:
            total += 1
            line = resolve_ip(ip)
            if line:
                resolved += 1
                out.write(line + '\n')
                if verbose:
                    print(line)
            else:
                if verbose:
                    print('Could not resolve: ' + ip)
    if verbose:
        print(f'Total checked: {total}. Resolved: {resolved}.')


def scan_from_file(infile_path, outfile_path, verbose):
    if not os.path.isfile(infile_path):
        print('Input file not found: ' + infile_path)
        sys.exit(1)
    total = 0
    resolved = 0
    with open(outfile_path, 'w') as out, open(infile_path, 'r') as f:
        for raw in f:
            spec = raw.strip()
            if not spec:
                continue
            for ip in iter_ips_from_range(spec):
                total += 1
                line = resolve_ip(ip)
                if line:
                    resolved += 1
                    out.write(line + '\n')
                    if verbose:
                        print(line)
                else:
                    if verbose:
                        print('Could not resolve: ' + ip)
    if verbose:
        print(f'Total checked: {total}. Resolved: {resolved}.')


def write_html_diff(prev_scan_path, new_scan_path, html_prefix):
    if not os.path.isfile(prev_scan_path):
        print('Previous scan file not found: ' + prev_scan_path)
        return
    if not os.path.isfile(new_scan_path):
        print('New scan file not found: ' + new_scan_path)
        return

    now = datetime.datetime.now()
    out_html = f'{html_prefix}{now.strftime("%d-%b-%Y_%H-%M-%S")}.html'

    header = """
<style>
body{text-align:center; background:#EEE; width:80%; margin:0 auto;}
table{margin:0 auto; width:auto;}
td tr {padding:0px;}
.heading{width:80%; margin-left:400px;}
.clear{clear:both;}
</style>
<div class="heading">
<img src="http://www.bridgestone.com/etc/images/logos/bridgestone-logo-set-en.png" style="float:left; margin-top:10px;" />
<h1 style="float:left; width:50%;">Host Discovery and Comparison</h1>
</div>
<div class="clear"></div>
"""
    now_html = f'<h3 style="font-style:italic;">{now.strftime("%d-%b-%Y_%H:%M:%S")}</h3>'
    old_hdr = f'Orig File: {prev_scan_path}'
    new_hdr = f'New File: {new_scan_path}'

    diff = difflib.HtmlDiff()
    with open(prev_scan_path, 'r') as f1, open(new_scan_path, 'r') as f2:
        d_html = diff.make_file(f1.readlines(), f2.readlines(), fromdesc=old_hdr, todesc=new_hdr, context=True, numlines=0)

    with open(out_html, 'w') as doc:
        doc.write(header)
        doc.write(now_html)
        doc.write(d_html)

    print('HTML report written to: ' + out_html)
    try:
        webbrowser.open(out_html)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description='Reverse DNS discovery with optional comparison.')
    parser.add_argument('-r', '--range', help='CIDR, full range, or shorthand. Examples 192.168.1.0/24 or 192.168.1.10-192.168.1.250 or 192.168.1.0-255')
    parser.add_argument('-i', '--infile', help='File of IPs or ranges, one per line')
    parser.add_argument('-o', '--outfile', required=True, help='Output file for resolved hosts')
    parser.add_argument('-p', '--previous_scan', help='Previous results to compare against')
    parser.add_argument('-H', '--htmlfile', help='HTML output filename prefix for the diff report')
    parser.add_argument('-t', '--timeout', type=float, default=5, help='DNS lookup timeout in seconds')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    if not args.range and not args.infile:
        print('Provide --range or --infile')
        sys.exit(1)

    try:
        socket.setdefaulttimeout(float(args.timeout))
    except Exception:
        pass

    print('Writing results to: ' + args.outfile)

    if args.range:
        ip_iter = iter_ips_from_range(args.range)
        scan_ips(ip_iter, args.outfile, args.verbose)
    else:
        scan_from_file(args.infile, args.outfile, args.verbose)

    if args.previous_scan and args.htmlfile:
        try:
            write_html_diff(args.previous_scan, args.outfile, args.htmlfile)
        except Exception:
            print('Could not create HTML comparison')

    print('Done')


if __name__ == '__main__':
    main()
