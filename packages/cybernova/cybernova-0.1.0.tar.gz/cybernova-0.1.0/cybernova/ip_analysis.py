import subprocess
from whois import whois
import re
import platform
import os

def is_ip_up(ip_address):
    """Check if the IP address is up by pinging it."""
    # Determine the option for count based on the platform
    count_option = "-n" if platform.system().lower() == "windows" else "-c"
    # Determine the option for timeout based on the platform
    timeout_option = "-w" if platform.system().lower() == "windows" else "-W"

    try:
        subprocess.run(["ping", count_option, "1", timeout_option, "2000", ip_address],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def whois_lookup(domain):
    """Perform a WHOIS lookup for the given domain."""
    try:
        domain_info = whois(domain)
        if domain_info:
            return domain_info
        else:
            return "WHOIS information not found for this domain."
    except Exception as e:
        return f"Error: {str(e)}"

def os_fingerprinting(ip_address):
    """Determine the OS of a host by its IP TTL response."""
    try:
        # Adjust the ping command based on the OS
        command = ["ping", "-c", "1", ip_address] if os.name != 'nt' else ["ping", "-n", "1", ip_address]
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Search for TTL value in the ping output
        ttl_match = re.search(r"ttl=(\d+)", result.stdout, re.IGNORECASE)
        
        if ttl_match:
            ttl = int(ttl_match.group(1))
            if 0 < ttl <= 64:
                return "Likely Linux/Unix"
            elif 64 < ttl <= 128:
                return "Likely Windows"
            elif ttl > 128:
                return "Likely Solaris/AIX"
            else:
                return "Unable to determine OS"
        else:
            return "TTL not found in ping output"
    except subprocess.CalledProcessError as e:
        return f"Error: Unable to send ping request - {str(e)}"

    


