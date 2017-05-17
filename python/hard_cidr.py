#!/usr/bin/python3

import argparse
import sys
import netaddr

def main():
    # setup arguments
    parser = argparse.ArgumentParser(description='Put description here')
    parser.add_argument('-c', '--cidr', help='cidre to be converted to ip range')
    parser.add_argument('-r', '--iprange', help='ip address range')
    parser.add_argument('-v', '--verbose', help="prints ip addresses of a given range", action='store_true')
    args = parser.parse_args()

    if args.iprange:
        startIP, endIP = args.iprange.split('-', 1)
        cidr = str(netaddr.iprange_to_cidrs(startIP,endIP)).split("'")[1]
        hosts = list(cidr)
        print('[+] Cidr:', cidr)
        print ('[+] Hosts: ', len(hosts))

    elif args.cidr:
        cidr = netaddr.IPNetwork(args.cidr)
        hosts = list(cidr)
        print ('[+] Range:', str(netaddr.cidr_to_glob(cidr)))
        print ('[+] Hosts: ', len(hosts))
        print ('[+] Netmask', cidr.netmask)

        if args.verbose:
            for cidr in cidr.iter_hosts():
                print ('%s' % cidr)
            print('\n')
    else:
        print ('[!] Nothing specified, therefore nothing to convert. See ya Sucka')

if __name__ == '__main__':
    main()
