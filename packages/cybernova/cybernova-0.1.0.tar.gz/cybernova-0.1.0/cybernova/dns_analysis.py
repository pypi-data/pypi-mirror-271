import dns.resolver
import socket
import dns.reversename

def get_domain_ip(domain_name):
    """Get the IP address of a given domain."""
    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror as e:
        return f"Error resolving domain: {e}"

def fetch_dns_info(domain):
    """Fetch various DNS records for a given domain."""
    record_types = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'SOA', 'PTR', 'SRV', 'CAA', 'DNSKEY']
    all_records = []
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records = [f"{record_type} record: {answer.to_text()}" for answer in answers]
            all_records.extend(records)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            all_records.append(f"No {record_type} records found for {domain}.")
        except Exception as e:
            all_records.append(f"Error fetching {record_type} records: {str(e)}")
    return all_records

def reverse_dns_lookup(ip_address):
    """Perform a reverse DNS lookup for a given IP address."""
    try:
        query = dns.reversename.from_address(ip_address)
        answers = dns.resolver.resolve(query, 'PTR')
        return [f"Reverse DNS: {answer.to_text().rstrip('.')}" for answer in answers]
    except Exception as e:
        return [f"Failed to perform reverse DNS lookup: {str(e)}"]

def verify_dnssec(domain):
    """Verify if DNSSEC is enabled for a given domain."""
    try:
        result = dns.resolver.resolve(domain, 'DNSKEY')
        if result.response.flags & dns.flags.DO:
            return ["DNSSEC is enabled for", domain]
        else:
            return ["DNSSEC is not enabled for", domain]
    except Exception as e:
        return ["Failed to perform DNSSEC verification:", str(e)]

