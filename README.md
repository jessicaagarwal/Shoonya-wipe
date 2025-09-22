# Shoonya Wipe (NIST SP 800-88r2 Compliant)

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

> **📖 For detailed step-by-step instructions, see [QUICK_START.md](QUICK_START.md)**

### **Docker Environment (Recommended)**
```bash
# 1. Clone and setup
git clone <repository-url>
cd shoonya-wipe

# 2. Start the web application
docker compose up -d

# 3. Access the web interface
# Open browser to: http://localhost:5000
```

### **Main Commands**
```bash
# Web GUI (recommended) - Access via http://localhost:5000
docker compose up -d

# CLI interface (inside container)
docker compose exec shoonya-wipe-web python main.py cli

# Verification tool
docker compose exec shoonya-wipe-web python main.py verify

# One-click wipe engine
docker compose exec shoonya-wipe-web python main.py engine
```

### **Access Web Interface**
- Open browser to: **http://localhost:5000**
- Follow the 4-step wizard
- Generate certificates offline

## 📁 **Project Structure**

```
shoonya-wipe/
├── 📁 src/
│   ├── 📁 core/                    # Core logic and NIST compliance
│   │   ├── safeerase.py           # Main CLI interface
│   │   ├── nist_compliance.py     # NIST SP 800-88r2 compliance engine
│   │   ├── sandbox.py             # Safe testing environment
│   │   ├── verify.py              # Certificate verification
│   │   └── 📁 engine/             # Modular wipe engine
│   │       ├── clear.py           # NIST Clear method implementation
│   │       ├── purge.py           # NIST Purge method implementation
│   │       ├── certificate.py     # Certificate generation
│   │       ├── utils.py           # Utility functions
│   │       └── dispatcher.py      # Engine dispatcher
│   └── 📁 web/
│       └── web_gui.py             # Flask web application
├── 📁 templates/
│   └── index.html                 # Web GUI template
├── 📁 virtual_media/              # Virtual disk images for testing
│   ├── vdisk0.img
│   └── vdisk1.img
├── 📁 out/                        # Generated certificates and logs
├── 📁 exports/                    # Export directory
├── 📁 keys/                       # RSA keys for digital signatures
├── 📄 main.py                     # Application entry point
├── 📄 requirements.txt            # Python dependencies
├── 📄 docker-compose.yml          # Docker configuration
├── 📄 Dockerfile                  # Docker image definition
├── 📄 NIST_COMPLIANCE.md          # NIST compliance documentation
└── 📄 IMPLEMENTATION_SUMMARY.md   # Implementation details
```

## 🔧 **Installation**

### **Docker (Recommended)**
```bash
# Start the application
docker compose up -d

# Access the web interface
# Open browser to: http://localhost:5000

# Access container for CLI usage
docker compose exec shoonya-wipe-web bash
```

### **Direct Installation**
```bash
# Install dependencies
pip install -r requirements.txt

# Run web interface
python main.py web

# Run CLI interface
python main.py cli
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
- **NIST Compliant** - SP 800-88r2 data sanitization
- **Audit Trail** - Complete wipe documentation
- **Docker Safety** - Sandboxed execution prevents real drive damage
- **Virtual Testing** - Safe testing with virtual disk images
- **Cross-Platform** - Windows, Linux, and Docker support

## 🛡️ **Safety Measures**

### **Docker Containerization**
- **Sandboxed Environment** - All operations run inside Docker containers
- **Virtual Media** - Uses virtual disk images for testing (vdisk0.img, vdisk1.img)
- **Read-Only Filesystem** - Prevents accidental system modifications
- **No Real Drive Access** - Cannot accidentally wipe real drives

### **NIST SP 800-88r2 Compliance**
- **Clear Method** - Single-pass overwrite for magnetic media
- **Purge Method** - SSD secure erase and cryptographic erase
- **AI Decision Flowchart** - Intelligent method selection based on device type
- **Verification & Validation** - Comprehensive compliance checking
- **Digital Certificates** - NIST-compliant PDF and JSON certificates

### **Testing Environment**
- **Virtual Disks** - 2GB virtual disk images for safe testing
- **Real Functionality** - Actual wipe operations on virtual media
- **Certificate Generation** - Full certificate generation and signing
- **Progress Simulation** - Realistic progress tracking and timing

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

- **📖 Quick Start**: `QUICK_START.md` - Get started in 5 minutes
- **🔧 API Documentation**: `API_DOCUMENTATION.md` - Complete API reference and usage examples
- **👨‍💻 Development Guide**: `DEVELOPMENT_GUIDE.md` - Development setup, architecture, and contribution guidelines
- **📋 Project Overview**: `PROJECT_OVERVIEW.md` - Complete project overview and architecture
- **🔒 NIST Compliance**: `NIST_COMPLIANCE.md` - NIST SP 800-88r2 compliance details
- **⚙️ Implementation Summary**: `IMPLEMENTATION_SUMMARY.md` - Technical implementation overview

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

**Shoonya Wipe** - Making e-waste recycling safe and trustworthy! 🌱
