xsspy
xsspy is a powerful, AI-enhanced command-line tool designed to automate the detection of Reflected Cross-Site Scripting (XSS) vulnerabilities. It leverages the analytical power of Google's Gemini AI to analyze potential reflections, providing more accurate results than traditional scanners and reducing false positives.

\033[96m
 __  __ ____ ____ ____ __ __
 \ \/ /|  _ \  _ \  _ \ \ V /
  \  / | |_) | |_) | |_) | \ /
  /  \ |  __/|  __/|  __/  | |
 /_/\_\|_|   |_|   |_|     |_|

\033[0m
     \033[93mxsspy by hussain\033[0m

Disclaimer
This tool is intended for educational purposes and for use in authorized security testing scenarios only. The author is not responsible for any misuse or damage caused by this program. Use it ethically and responsibly.

Features
🤖 AI-Powered Analysis: Uses Google's Gemini AI to intelligently determine if a reflected payload is exploitable.

🔎 Automatic Parameter Discovery: Crawls the target URL to find potential parameters to test.

⚡ Fast & Efficient: Includes a --first flag to stop scanning a parameter as soon as a vulnerability is confirmed.

📄 Clean Reporting: Provides a color-coded summary in the terminal and saves a detailed report to a file.

✅ User-Friendly: No need for users to configure API keys.

Installation on Kali Linux
xsspy is designed to be simple to set up on penetration testing distributions like Kali Linux.

Open your terminal and update your package list.

sudo apt update && sudo apt upgrade -y

Ensure you have git and pip installed.

sudo apt install git python3-pip -y

Clone the repository from GitHub.

git clone https://github.com/hussain9347/xsspy-tool.git

Navigate into the client tool directory.

cd xsspy-tool/client_tool

Install the required Python libraries.

sudo apt install python3-requests -y

Usage
The tool is run from the command line.

Basic Scan (scans all discovered parameters):

python3 xsspy_client.py -u "http://testphp.vulnweb.com/search.php?test=query"

Fast Scan (stops after the first finding per parameter):

python3 xsspy_client.py -u "YOUR_TARGET_URL" --first

Manual Scan (specify your own parameters):

python3 xsspy_client.py -u "YOUR_TARGET_URL" -p "q,query,search"

How It Works
This tool uses a client-server architecture. The xsspy_client.py tool you run connects to a centralized analysis server that securely handles the interaction with the Google Gemini API. This means users can run the scanner without needing to manage their own API keys.
