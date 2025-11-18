#!/usr/bin/env python3

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Optional

try:
    import netaddr
except ImportError:
    print('[-] You need to install the "netaddr" module. Get it with "pip install netaddr".')
    sys.exit(1)


def get_ips_from_range(ip_range: str) -> Iterable[str]:
    ip_range = ip_range.strip()

    if '/' in ip_range:
        try:
            network = netaddr.IPNetwork(ip_range)
        except netaddr.core.AddrFormatError:
            print(f'[-] Invalid CIDR specified: {ip_range}')
            sys.exit(1)
        return (str(ip) for ip in network)

    if '-' in ip_range:
        start_raw, end_raw = ip_range.split('-', 1)
        start_raw = start_raw.strip()
        end_raw = end_raw.strip()

        if '.' not in end_raw:
            base_octets = start_raw.split('.')
            if len(base_octets) != 4:
                print(f'[-] Invalid IP range specified: {ip_range}')
                sys.exit(1)
            base_octets[3] = end_raw
            end_ip = '.'.join(base_octets)
        else:
            end_ip = end_raw

        try:
            ip_range_obj = netaddr.IPRange(start_raw, end_ip)
        except netaddr.core.AddrFormatError:
            print(f'[-] Invalid IP range specified: {ip_range}')
            sys.exit(1)

        return (str(ip) for ip in ip_range_obj)

    print(f'[-] Invalid range format: {ip_range}')
    sys.exit(1)


def build_ping_command(ip: str, timeout: int) -> List[str]:
    if sys.platform.startswith('win'):
        return ['ping', '-n', '1', '-w', str(timeout * 1000), ip]
    else:
        return ['ping', '-c', '1', '-W', str(timeout), ip]


def ping_host(ip: str, timeout: int) -> bool:
    cmd = build_ping_command(ip, timeout)
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return False
    return result.returncode == 0


def scan_hosts(
    hosts: Iterable[str],
    timeout: int,
    output_path: Optional[str],
    max_workers: int = 64,
) -> None:
    outfile = None
    if output_path:
        outfile = open(output_path, 'w', encoding='utf-8')

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {executor.submit(ping_host, ip, timeout): ip for ip in hosts}

            for future in as_completed(future_map):
                ip = future_map[future]
                try:
                    is_up = future.result()
                except Exception as exc:
                    print(f'[-] {ip} ping error: {exc}')
                    continue

                if is_up:
                    line = f'[+] {ip} is up'
                    print(line)
                    if outfile:
                        outfile.write(line + '\n')
    finally:
        if outfile:
            outfile.close()
            print(f'[*] Results saved to: {output_path}')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Simple host reachability scanner (ping based)')
    parser.add_argument('-r', '--range', help='IP range, for example 192.168.1.0/24 or 192.168.1.10-50')
    parser.add_argument('-H', '--host', help='Single host, for example 192.168.1.10')
    parser.add_argument('-i', '--input', help='File with IP addresses, one per line')
    parser.add_argument('-o', '--output', help='File to write reachable hosts to')
    parser.add_argument('-t', '--timeout', type=int, default=5, help='Ping timeout in seconds per host, default 5')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    timeout = args.timeout
    output_path = args.output
    hosts: List[str] = []

    if args.range:
        hosts.extend(list(get_ips_from_range(args.range)))
    elif args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                for line in f:
                    host = line.strip()
                    if not host:
                        continue
                    if '/' in host or '-' in host:
                        hosts.extend(list(get_ips_from_range(host)))
                    else:
                        hosts.append(host)
        except FileNotFoundError:
            print(f'[-] Input file not found: {args.input}')
            sys.exit(1)
    elif args.host:
        hosts.append(args.host)
    else:
        print('[-] You need to specify a range, input file, or a host.')
        sys.exit(1)

    scan_hosts(hosts, timeout, output_path)

if __name__ == '__main__':
    main()
