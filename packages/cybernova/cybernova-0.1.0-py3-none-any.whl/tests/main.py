from cybernova.dns_analysis import fetch_dns_info, reverse_dns_lookup, get_domain_ip
from cybernova.port_scanner import scan_ports
from cybernova.ssl_check import check_ssl_certificate
from cybernova.ip_analysis import is_ip_up, whois_lookup, os_fingerprinting
from cybernova.vulnerability import scan_ports,scan_vulnerabilities , save_scan_result
import sys
import subprocess

def print_dns_menu():
    print("\nDNS Analysis")
    print("1. Fetch DNS Information")
    print("2. Reverse DNS Lookup")
    print("3. Get IP Address")
    print("4. Back to Main Menu")

def perform_dns_analysis():
    while True:
        print_dns_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            domain = input("Enter domain to analyze: ")
            dns_info = fetch_dns_info(domain)
            for info in dns_info:
                print(info)
        elif choice == "2":
            ip = input("Enter IP address for reverse DNS lookup: ")
            result = reverse_dns_lookup(ip)
            print(result)
        elif choice == "3":
            domain = input("Enter domain to get IP address: ")
            ip = get_domain_ip(domain)
            print("IP Address:", ip)
        elif choice == "4":
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def print_menu():
    print("\nCyberNova Cybersecurity Toolkit")
    print("1. Perform DNS Analysis")
    print("2. Scan Ports")
    print("3. Check SSL Certificate")
    print("4. Perform IP Analysis")
    print("5. Scan for Vulnerabilities")
    print("6. Exit")

def perform_port_scanning():
    ip = input("Enter IP address to scan: ")
    ports_input = input("Enter the ports to be scanned (comma-separated, e.g., 80,443,22): ")
    # Convert the comma-separated string of ports into a list of integers
    ports = [int(port.strip()) for port in ports_input.split(',')]
    result = scan_ports(ip, ports)
    for res in result:
        print(res)

def perform_ssl_check():
    domain = input("Enter domain to check SSL certificate: ")
    result = check_ssl_certificate(domain)
    print(result)

def perform_ip_analysis():
    while True:
        ip = input("Enter IP address to analyze: ")
        print("1. Check if IP is up")
        print("2. Perform WHOIS lookup")
        print("3. Perform OS fingerprinting")
        print("4. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == "1":
            result = is_ip_up(ip)
            print(result)
        elif choice == "2":
            result = whois_lookup(ip)
            print(result)
        elif choice == "3":
            result = os_fingerprinting(ip)
            print(result)
        elif choice == "4":
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def perform_vulnerability_scan():
    ip = input("Enter IP address to scan for vulnerabilities: ")
    print("Scanning for open ports first. This may take a few moments...")
    # Scan all ports to determine which ones are open
    open_ports = scan_ports(ip)  # This should return a list of open ports

    if open_ports:
        print("Open ports found:", ', '.join(open_ports))
        check_vulns = input("Do you want to check for vulnerabilities on these ports? (yes/no): ").lower()
        if check_vulns == 'yes':
            specific_ports = input("Enter specific ports to check (comma-separated), or type 'all' to check all open ports: ")
            if specific_ports.lower() == 'all':
                ports_to_scan = open_ports
            else:
                ports_to_scan = [port.strip() for port in specific_ports.split(',')]
            
            print("Scanning for vulnerabilities on selected ports...")
            for port in ports_to_scan:
                # Convert string ports to integer
                port = int(port)
                result = scan_vulnerabilities(ip, [port])  # Assuming scan_vulnerabilities expects a list of ports
                print(f"Vulnerabilities on port {port}: {result}")
                
            # Ask the user for the location to save the scan results
            save_location = input("Enter the location to save the scan results: ")
            # Save the scan results to the specified location
            save_scan_result(result, save_location)
            print(f"Scan results saved to: {save_location}")
        else:
            print("Skipping vulnerability scan.")
    else:
        print("No open ports found, skipping vulnerability scan.")



def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            perform_dns_analysis()
        elif choice == "2":
            perform_port_scanning()
        elif choice == "3":
            perform_ssl_check()
        elif choice == "4":
            perform_ip_analysis()
        elif choice == "5":
            perform_vulnerability_scan()
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
