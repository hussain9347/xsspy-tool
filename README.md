# 🧠 xsspy – AI-Enhanced Reflected XSS Scanner

**xsspy** is a powerful command-line tool designed to automate the detection of **Reflected Cross-Site Scripting (XSS)** vulnerabilities using **Google's Gemini AI**.

It reduces false positives by analyzing the actual exploitability of reflected payloads—making it more intelligent and accurate than traditional scanners.

---
<img width="640" height="640" alt="ChatGPT Image Jul 13, 2025, 10_28_50 PM" src="https://github.com/user-attachments/assets/19a7a66c-b06b-40e4-98bf-c59c2f2c0540" />


https://github.com/user-attachments/assets/66d5c6ef-76f5-4cbd-ad68-e1a4da73c275


## 🚀 Features

- ✅ AI-powered analysis using Gemini  
- ✅ Automatic parameter detection and payload injection  
- ✅ Clean CLI interface for bug hunters and pentesters  
- ✅ No need to set up your own API key  
- ✅ Client-server architecture for secure backend analysis  
- ✅ Open-source and beginner-friendly  

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/xsspy.git
cd xsspy
pip install -r requirements.txt

⚙️ Usage
Basic Command
python xsspy_client.py --url https://example.com --payloads payloads.txt

Options
Option	Description
--url	Target URL with injectable parameters
--payloads	Path to your custom or default payload list
--headers	(Optional) Add custom headers if needed

+----------------+      HTTP POST      +----------------+
| xsspy_client.py|  -----------------> | api_server.py  |
| (Public CLI)   |                    | (Flask Server) |
+----------------+ <-----------------  +----------------+
        |                                |
    Injects Payloads                Uses Gemini API
        |                                |
    Parses Reflections            Sends AI verdict

☁️ Deployment
Server Setup on Render
Create requirements.txt:
Flask
gunicorn
requests

🛡️ Security
The API key is stored securely on the server.

Never exposed to the public or client-side.

All traffic between client and server is encrypted.

AI analysis only occurs backend-side.

🧠 Powered By
Google Gemini API

Python 3.x

Flask

Render Cloud Hosting

Basic Q&A realted to this tool:-
Q: Does this tool only scan for Reflected XSS?

A: Yes, currently it is specifically designed to find and validate Reflected XSS vulnerabilities.

Q: What is the tech stack and what is each technology used for?

A:
Python: The programming language used to build both the client tool and the server.

Flask: A lightweight Python library used to create the API server.

Google Gemini: The AI model used for smart vulnerability analysis.

Render: The cloud service used to host the public API server.

Git & GitHub: Used for version control and to publish the open-source tool.

Q: Do I need an API key to use this tool?

A: No. The client tool is user-friendly and connects to a central server that handles the API key securely, so users don't need their own.

Q: How does the AI part work?

A: After injecting a payload, the tool sends the website's HTML response to the Gemini AI. The AI reads the code and determines if the payload was reflected in a dangerous, exploitable way, which reduces false positives.

Q: Is it safe to scan any website?

A: No. You should only use this tool on websites you have explicit permission to test or on dedicated practice sites like testphp.vulnweb.com. Unauthorized scanning is illegal.

📫 Contact
GitHub: https://github.com/hussain9347

LinkedIn: https://www.linkedin.com/in/syed-kaif-hussain/

