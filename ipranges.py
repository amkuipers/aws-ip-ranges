"""The ipranges tool, downloads the AWS ip-ranges.json, and enables listing and filters"""

import json
import ipaddress
import argparse
import requests

# usage: python3 ipranges.py
# from the ip-ranges.json it only uses the IPv4 prefixes


class IPRanges:
    """IPRanges to download, filter and print the AWS ip-ranges"""

    def __init__(self):
        """init with url, and loads it"""
        self.url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
        self.ip_ranges = self._load()

    def _load(self):
        """download the remote json ip-ranges file"""
        print('[+] Retrieving ip-ranges.json...')
        resp = requests.get(self.url)
        if resp.status_code == 200:
            print('[+] Retrieved ip-ranges.json')
            print(f'[+] File size {len(resp.text)}')
            return json.loads(resp.text)

        print(f'[-] Unexpected status {resp.status_code} retrieving ip-ranges.json')
        return None

    def _filter_ipv4(self, key, value):
        """mutates the IPv4 list with key value filter"""
        result = {'prefixes': []}
        for prefix in self.ip_ranges['prefixes']:
            if prefix[key] == value:
                result['prefixes'].append(prefix)
        self.ip_ranges = result

    def filter_ip_ranges(self, service, region):
        """mutates the IPv4 list with service and or region filter"""
        print(f'[+] IPv4 CIDR ranges filter for service {service} in region {region}')
        if service is not None:
            self._filter_ipv4('service', service)
        if region is not None:
            self._filter_ipv4('region', region)

    def filter_ipv4_by_ip(self, ip_number):
        """mutates the IPv4 list with IP filter"""
        print(f'[+] IPv4 CIDR ranges filter for {ip_number}')
        result = {'prefixes': []}
        for prefix in self.ip_ranges['prefixes']:
            cidr = prefix['ip_prefix'].strip()
            if ipaddress.IPv4Address(ip_number) in ipaddress.ip_network(cidr):
                result['prefixes'].append(prefix)
        self.ip_ranges = result

    def print_wide(self):
        """print the (remaining) IPv4 list"""
        if len(self.ip_ranges['prefixes']) == 0:
            print('[-] Empty result')

        for prefix in self.ip_ranges['prefixes']:
            service = prefix['service']
            region = prefix['region']
            cidr = prefix['ip_prefix'].strip()
            net = ipaddress.ip_network(cidr)
            print(f'[+] service {service}, region {region}, cidr {cidr} [{net[0]} - to {net[-1]}]')

    def print_filters(self):
        """print the services and regions from the (remaining) IPv4 list"""
        if len(self.ip_ranges['prefixes']) == 0:
            print('[-] Empty result')

        services = set()  # set
        regions = set()  # set
        for prefix in self.ip_ranges['prefixes']:
            services.add(prefix['service'])
            regions.add(prefix['region'])
        for service in services:
            print(f'[+] service {service}')
        for region in regions:
            print(f'[+] region {region}')


parser = argparse.ArgumentParser('Filter AWS IP Ranges')
parser.add_argument("-r", "--region", help="region filter, like eu-west-2")
parser.add_argument("-s", "--service", help="service filter, like S3, AMAZON")
parser.add_argument('-f', "--filters", help="list filters", action="store_true")
parser.add_argument("-ip", "--lookup", help="lookup service and region by ip")
args = parser.parse_args()

# hardcoded overwrites when running from IDE
# args.region = 'eu-west-2'
# args.service = None
# args.service = 'S3'
# args.filters = True
# args.lookup = '52.219.169.42'

ranges = IPRanges()

if args.region is not None or args.service is not None:
    ranges.filter_ip_ranges( args.service, args.region)

if args.lookup is not None:
    ranges.filter_ipv4_by_ip( args.lookup)

if args.filters:
    ranges.print_filters()
else:
    ranges.print_wide()
