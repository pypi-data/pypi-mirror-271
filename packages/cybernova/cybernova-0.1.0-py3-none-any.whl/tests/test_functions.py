
import sys
sys.path.insert(0, 'C:/Users/anixk/Desktop/Functional')  # Path to the directory containing the 'cybernova' package

import unittest
from unittest.mock import patch
from cybernova.dns_analysis import get_domain_ip, fetch_dns_info
from cybernova.port_scanner import scan_ports
from cybernova.ssl_check import check_ssl_certificate
from cybernova.ip_analysis import is_ip_up, whois_lookup, os_fingerprinting
from cybernova.vulnerability import scan_ports as scan_vulnerabilities_ports, scan_vulnerabilities
import subprocess


class MockDNSRecord:
    def to_text(self):
        return "127.0.0.1"

class TestDNSAnalysis(unittest.TestCase):
    @patch('dns.resolver.resolve')
    def test_fetch_dns_info(self, mock_resolve):
        # Assuming fetch_dns_info appends 'A record:' itself
        mock_resolve.return_value = [MockDNSRecord()]
        result = fetch_dns_info("example.com")
        self.assertEqual(result, ['A record: 127.0.0.1'])

    @patch('dns.resolver.resolve')
    def test_fetch_dns_info(self, mock_resolve):
        mock_resolve.return_value = iter([MockDNSRecord()])
        result = fetch_dns_info("example.com")
        self.assertEqual(result, ['A record: 127.0.0.1'])

class TestPortScanner(unittest.TestCase):
    @patch('subprocess.run')
    def test_scan_ports(self, mock_run):
        # Mocking subprocess.run to return expected command output
        mock_run.return_value = subprocess.CompletedProcess(args=['nmap', '-p', '80,443', 'example.com'], returncode=0, stdout='80/tcp open\n443/tcp open')
        # Properly calling scan_ports with both arguments
        result = scan_ports("example.com", [80, 443])
        self.assertIn('80', result)
        self.assertIn('443', result)



class TestSSLCertificateCheck(unittest.TestCase):
    @patch('subprocess.run')
    def test_ssl_certificate(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['openssl'], returncode=0, stdout='Certificate: Valid')
        result = check_ssl_certificate("example.com")
        self.assertIn('Certificate: Valid', result)

class TestIPAnalysis(unittest.TestCase):
    @patch('subprocess.run')
    def test_is_ip_up(self, mock_run):
        mock_run.return_value.check_returncode = lambda: None  # Simulate no exception
        result = is_ip_up("8.8.8.8")
        self.assertTrue(result)

    @patch('whois.whois')
    def test_whois_lookup(self, mock_whois):
        mock_whois.return_value = {"domain_name": "example.com"}
        result = whois_lookup("example.com")
        self.assertIsInstance(result, dict)

    @patch('subprocess.run')
    def test_os_fingerprinting(self, mock_run):
        mock_run.return_value.stdout = 'ttl=128'
        result = os_fingerprinting("192.168.1.1")
        self.assertEqual(result, "Likely Windows")


if __name__ == '__main__':
    unittest.main()
