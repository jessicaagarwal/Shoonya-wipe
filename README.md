# SafeErasePro (NIST SP 800-88r2 Compliant)

**AI-Assisted, Verified, Cross-Platform Data Wiper with Digital Certificate**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

## 🎯 **Problem Statement**

**E-waste Crisis in India:**
- 1.75 million tonnes of e-waste generated yearly
- ₹50,000 crore worth of IT assets remain unused/hoarded
- Users avoid recycling due to data privacy concerns

**Our Solution:**
A simple, secure, verifiable, and tamper-proof data wiping solution that builds user trust and promotes safe e-waste disposal.

## ✨ **Key Features**

### 🔒 **Secure Data Wiping**
- NIST SP 800-88r2 compliant methods (Clear, Purge, Destroy guidance)
- SSD secure erase and cryptographic erase
- Single-pass overwrite for Clear (NIST guidance)

### 📜 **Digital Certificates**
- Digitally signed NIST-compliant certificates (PDF + JSON)
- RSA-PSS-SHA256 cryptographic signatures
- Third-party verification support
- Tamper-proof certificates

### 🖥️ **User-Friendly Interface**
- **Web GUI** - Modern 4-step wizard interface
- **CLI** - Command-line interface for advanced users
- **Portable Mode** - No installation required
- **Offline Mode** - Works without internet

### 🔍 **Verification System**
- Offline signature verification
- Third-party validation tools
- Certificate authenticity checking
- Audit trail for compliance

## 🚀 **Quick Start**

### **Development Environment**
```bash
# 1. Clone and setup
git clone <repository-url>
cd safe-erase-pro
docker compose up -d

# 2. Run SafeErasePro
docker compose exec saferase-dev python main.py web
```

### **Main Commands**
```bash
# Web GUI (recommended)
python main.py web

# CLI interface
python main.py cli

# Verification tool
python main.py verify

# Create portable package
python main.py portable
```

### **Access Web Interface**
- Open browser to: **http://localhost:5000**
- Follow the 4-step wizard
- Generate certificates offline

## 📁 **Project Structure**

```
safe-erase-pro/
├── 📁 src/
│   ├── 📁 core/              # Core logic (CLI, NIST engine, verifier)
│   │   ├── safeerase.py
│   │   ├── nist_compliance.py
│   │   └── verify.py
│   └── 📁 web/
│       └── web_gui.py        # Flask app
├── 📁 templates/
│   └── index.html            # Web GUI template (top-level)
├── 📄 main.py
├── 📄 requirements.txt
├── 📄 NIST_COMPLIANCE.md
└── 📄 IMPLEMENTATION_SUMMARY.md
```

## 🔧 **Installation**

### **Docker (Recommended)**
```bash
# Start development environment
docker compose up -d

# Access container
docker compose exec saferase-dev bash
```

### **Direct Installation**
```bash
# Install dependencies
pip install -r requirements.txt

# Run directly (Windows: use `python`)
python main.py web
```

## 📦 **Distribution**

### **Portable Package**
```bash
# Create portable package
python main.py portable

# Use anywhere (no installation)
cd dist/portable
./launch.sh  # Linux/Mac
launch.bat   # Windows
```

### **Third-Party Verification**
```bash
# Share verification tool
cd dist/verifier
python verify_simple.py certificate.json
```

## 🔒 **Security Features**

- **Offline Operation** - No internet required
- **RSA-PSS-SHA256** - Industry-standard signatures
- **Tamper-Proof** - Cryptographically secure certificates
- **NIST Compliant** - SP 800-88 data sanitization
- **Audit Trail** - Complete wipe documentation

## 🎯 **Use Cases**

### **For Individuals**
- Secure data deletion before selling devices
- Privacy protection before recycling
- Compliance with data protection regulations

### **For Organizations**
- IT asset disposal with audit trails
- Compliance with data retention policies
- Secure device recycling programs

### **For Recyclers**
- Verify data has been properly wiped
- Provide certificates to customers
- Build trust in recycling process

## 📚 **Documentation**

- NIST Compliance: `NIST_COMPLIANCE.md`
- Implementation Summary: `IMPLEMENTATION_SUMMARY.md`

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- **Issues:** GitHub Issues
- **Documentation:** Check the docs/ folder
- **Questions:** Create a discussion

---

**SafeErasePro** - Making e-waste recycling safe and trustworthy! 🌱
