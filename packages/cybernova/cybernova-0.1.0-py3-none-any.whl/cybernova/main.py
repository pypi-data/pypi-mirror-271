#!/usr/bin/env python3
import argparse
from .dns_analysis import get_domain_ip, fetch_dns_info, reverse_dns_lookup
from .port_scanner import scan_ports
from .ssl_check import check_ssl_certificate
from .ip_analysis import is_ip_up, whois_lookup, os_fingerprinting
from .vulnerability import scan_vulnerabilities



def main():
    # Setup argparse to handle command line arguments
    parser = argparse.ArgumentParser(description="CyberNova Cybersecurity Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Command for DNS analysis
    dns_parser = subparsers.add_parser('dns', help="Perform DNS analysis")
    dns_parser.add_argument("domain", help="Domain to analyze")
    dns_parser.add_argument("--info", action="store_true", help="Fetch DNS information")
    dns_parser.add_argument("--reverse", action="store_true", help="Perform reverse DNS lookup")

    # Command for port scanning
    port_parser = subparsers.add_parser('scan', help="Scan ports")
    port_parser.add_argument("ip", help="IP address to scan")
    port_parser.add_argument("--ports", nargs="+", type=int, help="Ports to scan")

    # Command for SSL certificate checking
    ssl_parser = subparsers.add_parser('ssl', help="Check SSL certificate")
    ssl_parser.add_argument("domain", help="Domain to check SSL certificate")

    # Command for IP analysis
    ip_parser = subparsers.add_parser('ip', help="Perform IP analysis")
    ip_parser.add_argument("ip", help="IP address to analyze")
    ip_parser.add_argument("--up", action="store_true", help="Check if IP is up")
    ip_parser.add_argument("--whois", action="store_true", help="Perform WHOIS lookup")
    ip_parser.add_argument("--os", action="store_true", help="Perform OS fingerprinting")

    # Command for vulnerability scanning
    vuln_parser = subparsers.add_parser('vuln', help="Scan for vulnerabilities")
    vuln_parser.add_argument("ip", help="IP address to scan")
    vuln_parser.add_argument("--ports", nargs="+", type=int, help="Specify ports for vulnerability scanning")

    args = parser.parse_args()

    if args.command == "dns":
        if args.info:
            print(fetch_dns_info(args.domain))
        if args.reverse:
            print(reverse_dns_lookup(args.domain))

    elif args.command == "scan":
        if args.ports:
            print(scan_ports(args.ip, args.ports))
        else:
            print("No ports specified for scanning.")

    elif args.command == "ssl":
        print(check_ssl_certificate(args.domain))

    elif args.command == "ip":
        if args.up:
            print(is_ip_up(args.ip))
        if args.whois:
            print(whois_lookup(args.ip))
        if args.os:
            print(os_fingerprinting(args.ip))

    elif args.command == "vuln":
        if args.ports:
            print(scan_vulnerabilities(args.ip, args.ports))
        else:
            print("No ports specified for vulnerability scanning.")

if __name__ == "__main__":
    main()
