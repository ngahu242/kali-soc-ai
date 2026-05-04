# 🛡 Kali AI SOC Copilot

An AI-powered **Cybersecurity + IT Support Terminal Assistant** built for Linux / Kali Linux / Windows.

This project combines:

- 🧠 Artificial Intelligence
- 🛡 Security Operations Center (SOC) automation
- 🔍 Vulnerability Assessment
- ⚙️ IT Support Diagnostics
- 🌐 Network Scanning
- 💻 Process Monitoring
- 📊 System Health Analysis

---

# 🚀 Features

## 🛡 Cybersecurity Features

✔ Full System Security Audit  
✔ Open Ports Detection  
✔ Firewall Status Review  
✔ Suspicious Process Detection  
✔ Threat Hunting Assistance  
✔ Vulnerability Assessment  
✔ Security Recommendations  
✔ AI Threat Analysis  

---

## 🧰 IT Support Features

✔ Diagnose Slow Systems  
✔ CPU / RAM / Disk Analysis  
✔ Network Troubleshooting  
✔ Connectivity Testing  
✔ Service Diagnostics  
✔ Performance Optimization Tips  

---

# 🧠 AI BACKENDS

KALI SOC AI supports multiple AI providers.

---

## 🟢 GROQ (Recommended)

Groq is the **recommended cloud backend** for this project because it provides:

✔ Extremely fast responses  
✔ Lower cost than many alternatives  
✔ Great open-source models  
✔ Perfect for terminal AI workflows  
✔ Ideal for cybersecurity assistants  

Recommended Models:

- llama-3.3-70b-versatile
- llama-3.1-8b-instant
- mixtral-8x7b
- deepseek-r1-distill-llama
Use Groq for:

✔ Threat analysis  
✔ CVE explanations  
✔ SOC investigations  
✔ Linux troubleshooting  
✔ Report writing  
✔ Voice assistant responses  

---

## 🟡 OLLAMA (Local / Offline)

Best for:

✔ Offline environments  
✔ Private systems  
✔ Local AI inference  
✔ No internet required  

Recommended Models:

- llama3
- mistral
- gemma
- phi
- codellama

---
## 🔵 OPENAI (Optional)

Supported if preferred.

Best for:

✔ Premium reasoning  
✔ Larger ecosystem  
✔ Enterprise workflows  

---

⚙️ FULL INSTALLATION GUIDE
🪟 Windows Installation

1️⃣ Install Python

Download Python 3.10+

https://www.python.org/downloads/

During install check:

Add Python to PATH

2️⃣ Install Git

Download:

https://git-scm.com/downloads

3️⃣ Install Nmap

Download:

https://nmap.org/download.html

4️⃣ Clone Project
git clone https://github.com/YOURUSERNAME/kali-soc-ai.git
cd kali-soc-ai

5️⃣ Create Virtual Environment
python -m venv .venv

Activate:

.venv\Scripts\activate

6️⃣ Install Requirements
pip install -r requirements.txt

7️⃣ Optional AI Install (FREE)

Install Ollama:

https://ollama.com/download

Then run:

ollama run llama3

8️⃣ Run Program
python main.py

🐧 Kali Linux Installation

1️⃣ Update System
sudo apt update && sudo apt upgrade -y

2️⃣ Install Dependencies
sudo apt install python3 python3-pip python3-venv git nmap -y

3️⃣ Clone Repo
git clone https://github.com/YOURUSERNAME/kali-soc-ai.git
cd kali-soc-ai

4️⃣ Create Virtual Environment
python3 -m venv .venv

Activate:

source .venv/bin/activate

5️⃣ Install Python Packages
pip install -r requirements.txt

6️⃣ Install Ollama (FREE AI)
curl -fsSL https://ollama.com/install.sh | sh

Then run:

ollama run llama3

7️⃣ Run Project
python3 main.py

🔑 AI CONFIGURATION (.env)

Create .env
🟢 GROQ MODE (Recommended)
AI_MODE=groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

Get Groq API Key:

https://console.groq.com/

REPORT LOCATION

Reports saved in:

reports/

Example:

reports/soc_report_2026-05-01.txt


🔐 DISCLAIMER

Use only for:

Defensive Security
Blue Team Operations
SOC Training
Authorized Internal Assessments

Do not use against systems without permission.

👑 AUTHOR

Joseph Ngahu