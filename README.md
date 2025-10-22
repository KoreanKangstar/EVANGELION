# 🧠 EVANGELION - EdgeNAS

**EVANGELION - EdgeNAS** is a Flask-based hybrid NAS system for Raspberry Pi.  
It provides both **personal** and **shared** cloud storage areas, enabling seamless file management and collaboration between users.

---

## 🚀 Features

- 🔐 Multi-user login (Basic Auth)
- 🗂️ Separate **personal** and **shared** storage folders
- 📤 File upload, 📥 download, and ❌ delete functions
- 🧩 ZIP download for bulk access
- 🌐 UTF-8 filename & multi-language compatibility
- 💾 Modular Flask architecture (auth / personal / shared / utils separation)
- 🧱 Ready for deployment on Raspberry Pi 5 or any Linux system

---

## ⚙️ Setup Guide

### 1️⃣ Clone this repository
```bash
git clone https://github.com/KoreanKangstar/EVANGELION.git
cd EVANGELION
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Flask server
```bash
python3 app.py
```
