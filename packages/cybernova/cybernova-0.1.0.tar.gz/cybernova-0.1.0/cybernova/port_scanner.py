import socket
import ipaddress
import os

def scan_port(host, port):
    """Attempt to connect to a specific port on a host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            return f"Port {port} is open"
        else:
            return f"Port {port} is closed"
        sock.close()
    except socket.error as e:
        return f"Error: {e}"

def scan_ports(host, ports):
    """Scan a list of ports on a specified host."""
    results = []
    for port in ports:
        result = scan_port(host, port)
        results.append(result)
        
    return results

def save_scan_results(results, filename):
    """Save the scan results to a file."""
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(filename, "w") as f:
        f.write("\n".join(results))
    return f"Results saved to {filename}"

