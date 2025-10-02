# Shoonya WIPE (NIST SP 800-88r2 Compliant)
## National E-Waste Management Solution

**AI-Assisted, Verified, Cross-Platform Data Wiper with Digital Certificate**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![NIST Compliant](https://img.shields.io/badge/NIST-SP%20800--88r2-green.svg)](https://csrc.nist.gov/publications/detail/sp/800-88/rev-2/final)
[![Security](https://img.shields.io/badge/Security-RSA--PSS--SHA256-red.svg)](https://en.wikipedia.org/wiki/RSA-PSS)

## 🎯 **National Impact**

### **E-waste Crisis in India**
- **1.75 million tonnes** of e-waste generated annually
- **₹50,000 crore** worth of IT assets remain unused/hoarded
- **70% of users** avoid recycling due to data privacy concerns
- **Environmental hazard** from improper e-waste disposal

### **Our Solution**
A comprehensive, NIST SP 800-88r2 compliant data wiping solution that:
- **Builds Trust**: Cryptographically verifiable data wiping certificates
- **Promotes Recycling**: Safe, secure disposal of electronic devices
- **Protects Privacy**: Ensures complete data sanitization
- **Environmental Impact**: Reduces e-waste in landfills

## ✨ **Key Features**

### 🔒 **NIST SP 800-88r2 Compliance**
- **Complete Implementation**: All three sanitization methods (Clear, Purge, Destroy)
- **AI-Guided Process**: Intelligent decision flowchart for method selection
- **Verification System**: Complete sanitization verification and validation
- **Digital Certificates**: NIST-compliant PDF and JSON certificates

### 🛡️ **Security & Trust**
- **RSA-PSS-SHA256**: Industry-standard cryptographic signatures
- **Tamper-Proof**: Cryptographically secure certificates
- **Audit Trail**: Complete operation documentation
- **Docker Safety**: Sandboxed execution environment

### 🖥️ **User Experience**
- **Web GUI**: Modern 4-step wizard interface
- **CLI Interface**: Command-line tool for advanced users
- **Cross-Platform**: Windows, Linux, and Docker support
- **Offline Operation**: No internet required

### 🌱 **Environmental Impact**
- **E-Waste Reduction**: Promotes safe recycling of electronic devices
- **Resource Recovery**: Enables reuse of valuable materials
- **Public Awareness**: Educates citizens about data security
- **Trust Building**: Creates confidence in recycling processes

## 🚀 **Quick Start**

> **📖 For detailed step-by-step instructions, see [QUICK_START.md](QUICK_START.md)**

### **Docker Environment (Recommended)**
```bash
# 1. Clone and setup
git clone https://github.com/jessicaagarwal/shoonya-wipe.git
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

### **National Submission Package**
- **📊 Executive Summary**: `EXECUTIVE_SUMMARY.md` - Comprehensive overview for national submission
- **🔧 Technical Specifications**: `TECHNICAL_SPECIFICATIONS.md` - Complete technical architecture and compliance details
- **🚀 Deployment Guide**: `DEPLOYMENT_GUIDE.md` - Production deployment and scaling instructions
- **📈 National Impact Assessment**: `NATIONAL_IMPACT_ASSESSMENT.md` - Environmental, economic, and social impact analysis

### **Technical Documentation**
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

- **Issues:** [GitHub Issues](https://github.com/jessicaagarwal/shoonya-wipe/issues)
- **Documentation:** Complete technical documentation provided
- **Contact:** agarwaljessica25@gmail.com
- **Docker Hub:** [jessicaagarwal/shoonya-wipe](https://hub.docker.com/r/jessicaagarwal/shoonya-wipe)

---

**Shoonya Wipe** - Making e-waste recycling safe and trustworthy! 🌱
