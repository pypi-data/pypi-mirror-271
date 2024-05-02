import subprocess

def check_ssl_certificate(domain):
    """Check SSL/TLS certificate details for a domain."""
    try:
        print(f"Checking SSL/TLS certificate details for: {domain}")
        # Construct the openssl command as a list of arguments
        command = ["openssl", "s_client", "-connect", f"{domain}:443", "-showcerts"]

        # Start the subprocess with Popen and stream the output
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            # Read output line by line as it becomes available
            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    print(output.strip())
            # Check if there were any errors
            err = proc.stderr.read()
            if err:
                print("Error:")
                print(err.strip())
            if proc.returncode != 0:
                print("OpenSSL command failed with return code", proc.returncode)

    except Exception as e:
        print(f"Error: {str(e)}")

