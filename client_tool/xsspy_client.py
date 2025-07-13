#!/usr/bin/env python3

import argparse
import requests
import os
import sys
import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from datetime import datetime

# --- CONFIGURATION ---
# The public URL of your API server.
# For local testing, this is correct. For online deployment,
# you would change this to your public server URL.
ANALYSIS_SERVER_URL = "https://xsspy-tool-3.onrender.com/analyze" 

# --- ASCII Art Banner ---
BANNER = r"""
\033[96m
 __  __ ____ ____ ____ __ __
 \ \/ /|  _ \  _ \  _ \ \ V /
  \  / | |_) | |_) | |_) | \ /
  /  \ |  __/|  __/|  __/  | |
 /_/\_\|_|   |_|   |_|     |_|

\033[0m
     \033[93mxsspy by hussain\033[0m
"""

# --- Terminal Color Codes ---
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    MAGENTA = '\033[95m'

# --- Logging and Printing Functions ---
def print_info(message):
    print(f"[{Colors.CYAN}INFO{Colors.RESET}] {message}")

def print_step(message):
    print(f"[{Colors.BLUE}STEP{Colors.RESET}] {message}")

def print_success(message):
    print(f"[{Colors.GREEN}+{Colors.RESET}] {Colors.BOLD}{message}{Colors.RESET}")

def print_error(message):
    print(f"[{Colors.RED}ERROR{Colors.RESET}] {message}", file=sys.stderr)

def print_vulnerability(message):
    print(f"\n[{Colors.RED}VULNERABLE{Colors.RESET}] {Colors.RED}{Colors.BOLD}{message}{Colors.RESET}")

def log_to_file(filename, message):
    with open(filename, 'a') as f:
        f.write(f"{message}\n")

# --- Core Functions ---

def discover_params(base_url, headers):
    print_step(f"Attempting to discover parameters from {base_url}...")
    try:
        response = requests.get(base_url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        discovered_params = set(re.findall(r'[\?&]([a-zA-Z0-9_\[\]]+)=', response.text))
        if discovered_params:
            print_info(f"Discovered {len(discovered_params)} potential parameters: {', '.join(discovered_params)}")
            return list(discovered_params)
        else:
            print_info("No parameters discovered automatically. Please provide them manually using --params.")
            return []
    except requests.exceptions.RequestException as e:
        print_error(f"Could not fetch base URL to discover parameters: {e}")
        return []

def get_analysis_from_server(response_text, injected_payload):
    """
    Sends data to YOUR hosted API, which then calls Gemini.
    """
    headers = {'Content-Type': 'application/json'}
    data = {
        'html_content': response_text,
        'payload': injected_payload
    }
    try:
        response = requests.post(ANALYSIS_SERVER_URL, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            print_error(f"Analysis server returned an error: {response.status_code}")
            return "SAFE: Analysis server error."
        
        result = response.json()
        return result.get('analysis', 'SAFE: Invalid response from analysis server.')
    except requests.exceptions.RequestException as e:
        print_error(f"Could not connect to the analysis server at {ANALYSIS_SERVER_URL}.")
        print_error("Please ensure the api_server.py script is running in another terminal.")
        return "SAFE: Could not connect to analysis server."

def main():
    print(BANNER)
    
    # [FIXED] The --api-key argument has been removed.
    parser = argparse.ArgumentParser(description="xsspy by hussain - AI-Powered Reflected XSS Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target URL to scan.")
    parser.add_argument("-p", "--params", help="Manual comma-separated list of parameters to test.")
    parser.add_argument("--payloads-file", default="payloads.txt", help="File containing XSS payloads (default: payloads.txt).")
    parser.add_argument("-o", "--output", default="scan_report.txt", help="Output file to save the report (default: scan_report.txt).")
    parser.add_argument("--first", action="store_true", help="Stop testing a parameter after the first vulnerability is found.")

    args = parser.parse_args()
    
    report_file = args.output
    if os.path.exists(report_file):
        os.remove(report_file)
    log_to_file(report_file, f"Scan initiated for {args.url} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        with open(args.payloads_file, 'r') as f:
            payloads = [line.strip() for line in f if line.strip()]
        if not payloads:
            print_error(f"Payload file '{args.payloads_file}' is empty."); sys.exit(1)
        print_info(f"Loaded {len(payloads)} payloads from '{args.payloads_file}'.")
    except FileNotFoundError:
        print_error(f"Payload file not found: '{args.payloads_file}'"); sys.exit(1)

    if args.params:
        parameters_to_test = [p.strip() for p in args.params.split(',')]
        print_info(f"Using manually provided parameters: {', '.join(parameters_to_test)}")
    else:
        parameters_to_test = discover_params(args.url, headers)
        if not parameters_to_test:
            print_error("Could not find any parameters to test. Exiting."); sys.exit(1)

    confirmed_findings = []
    for param in parameters_to_test:
        print_step(f"Testing parameter: {Colors.YELLOW}{param}{Colors.RESET}")
        param_vulnerable = False
        for payload in payloads:
            try:
                parsed_url = urlparse(args.url)
                query_params = parse_qs(parsed_url.query)
                query_params[param] = payload
                new_query_string = urlencode(query_params, doseq=True)
                test_url = urlunparse(parsed_url._replace(query=new_query_string))

                print(f"  -> Injecting payload: {Colors.CYAN}{payload[:70]}...{Colors.RESET}")
                response = requests.get(test_url, headers=headers, timeout=10, verify=False)
                
                print("     Sending response to analysis server...")
                analysis_result = get_analysis_from_server(response.text, payload)
                print(f"     {Colors.BOLD}[Analysis]:{Colors.RESET} {analysis_result}")

                if analysis_result.upper().startswith("VULNERABLE"):
                    param_vulnerable = True
                    print_vulnerability("Potential Reflected XSS Confirmed!")
                    report_data = {
                        "url": test_url,
                        "param": param,
                        "payload": payload,
                        "insight": analysis_result
                    }
                    confirmed_findings.append(report_data)
                    
                    report_text = (
                        f"  [+] URL:      {test_url}\n"
                        f"  [+] Payload:  {payload}\n"
                        f"  [+] Insight: {analysis_result}"
                    )
                    print(report_text)
                    log_to_file(report_file, f"--- VULNERABILITY FOUND ---\n{report_text}\n")
                    
                    if args.first:
                        print_info(f"Vulnerability found. Stopping scan for parameter '{param}' as per --first flag.")
                        break

            except requests.exceptions.RequestException as e:
                print_error(f"Connection failed for {test_url}: {e}"); break
            except Exception as e:
                print_error(f"An unexpected error occurred: {e}")
        
        if param_vulnerable and args.first:
            continue

    print("\n" + "="*50)
    print(f"{Colors.BOLD}{Colors.MAGENTA}Scan Summary{Colors.RESET}")
    print("="*50)
    if confirmed_findings:
        print_success(f"Found {len(confirmed_findings)} potential vulnerabilities.")
        for finding in confirmed_findings:
            print(f"  - {Colors.YELLOW}Param:{Colors.RESET} {finding['param']}, {Colors.YELLOW}Payload:{Colors.RESET} \"{finding['payload']}\"")
            print(f"    {Colors.YELLOW}PoC:{Colors.RESET} {finding['url']}")
    else:
        print_info("Scan complete. No vulnerabilities were confirmed.")
    
    print("\n" + f"Full report saved to: {Colors.YELLOW}{report_file}{Colors.RESET}")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n[{Colors.YELLOW}!{Colors.RESET}] Scan interrupted by user. Exiting.")
        sys.exit(0)
