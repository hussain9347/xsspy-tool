# 🧠 xsspy – AI-Enhanced Reflected XSS Scanner

**xsspy** is a powerful command-line tool designed to automate the detection of **Reflected Cross-Site Scripting (XSS)** vulnerabilities using **Google's Gemini AI**.

It reduces false positives by analyzing the actual exploitability of reflected payloads—making it more intelligent and accurate than traditional scanners.

---

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

📫 Contact
GitHub: https://github.com/hussain9347

LinkedIn: https://www.linkedin.com/in/syed-kaif-hussain/

