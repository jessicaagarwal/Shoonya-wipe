# SafeErasePro

**AI-Assisted, Verified, Cross-Platform Data Wiper with Digital Certificate**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

## 🎯 **Problem Statement**

**E-waste Crisis in India:**
- 1.75 million tonnes of e-waste generated yearly
- ₹50,000 crore worth of IT assets remain unused/hoarded
- Users avoid recycling due to data privacy concerns

**Current Tools Shortcomings:**
- Complex to use
- Expensive
- Lack verifiable proof of data erasure

**Our Solution:**
A simple, secure, verifiable, and tamper-proof data wiping solution that builds user trust and promotes safe e-waste disposal.

## ✨ **Key Features**

### 🔒 **Secure Data Wiping**
- File system & partition aware wiping
- SSD secure erase commands
- Multi-pass overwrite (NIST SP 800-88 compliant)
- Hidden/SSD sectors coverage

### 🤖 **AI-Powered Intelligence**
- Smart scan & wipe suggestions
- Detects leftover sensitive files
- Suggests extra wipe actions for apps
- Maximum data removal with minimal effort

### 📜 **Digital Certificates**
- Digitally signed wipe certificates (PDF + JSON)
- Timestamp, device metadata, wipe summary
- Cryptographic signatures for authenticity
- Third-party verification support

### 🖥️ **User-Friendly Interface**
- One-click intuitive UI
- Visual progress & status messages
- Advanced mode with detailed options
- Offline usability (bootable ISO/USB)

### 🔍 **Verification System**
- Public-key cryptography (RSA/ECDSA)
- No blockchain or external servers required
- Verification portal for recyclers
- Tamper-proof certificate validation

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Wipe Engine   │───▶│  Logger & Cert  │───▶│   Verifier      │
│   (Python)      │    │   Generator     │    │   (Web/CLI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Linux Tools    │    │  PDF + JSON     │    │  Signature      │
│  (lsblk, etc.)  │    │  Certificates   │    │  Verification   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### **Prerequisites**
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Git

### **Development Setup**

#### **Windows/Mac (Development)**
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/SafeErasePro.git
cd SafeErasePro

# Start development environment
docker compose up --build

# Test the setup
docker compose exec saferase-dev python test_device_scan.py
```

#### **Linux (Testing)**
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/SafeErasePro.git
cd SafeErasePro

# Build and test with real devices
docker build -t saferase-pro .
docker run --rm -v /dev:/dev:ro -v /proc:/proc:ro -v /sys:/sys:ro saferase-pro
```

## 📁 **Project Structure**

```
SafeErasePro/
├── src/                    # Source code
│   ├── wipe_engine/        # Core wiping functionality
│   ├── certificate/        # Certificate generation
│   ├── verification/       # Signature verification
│   └── ui/                 # User interfaces
├── tests/                  # Test files
├── docs/                   # Documentation
├── scripts/                # Build and deployment scripts
├── Dockerfile              # Development environment
├── docker-compose.yml      # Container management
└── README.md              # This file
```

## 🛠️ **Development Workflow**

### **Daily Development (Windows/Mac)**
```bash
# 1. Start your day
git pull origin main

# 2. Start development environment
docker compose up -d

# 3. Develop your features
# Edit code in your IDE

# 4. Test your changes
docker compose exec saferase-dev python test_device_scan.py

# 5. Commit and push
git add .
git commit -m "Feature: Add device wiping functionality"
git push origin main
```

### **Testing (Linux Laptop)**
```bash
# 1. Pull latest changes
git pull origin main

# 2. Test with real devices
docker run --rm -v /dev:/dev:ro saferase-pro

# 3. Test actual wipe operations (when ready)
# This is where you test with real hardware
```

## 🔒 **Safety Features**

- **Docker Isolation**: All development in containers
- **Read-only Mounts**: Device access is read-only for safety
- **Non-root User**: Container runs as unprivileged user
- **No Accidental Wiping**: Development environment only
- **Real Device Testing**: Isolated Linux laptop for testing

## 📋 **Development Phases**

### **Phase 1: Core Wipe Engine** ✅
- [x] Docker development environment
- [x] Device detection and scanning
- [ ] File system aware wiping
- [ ] SSD secure erase commands
- [ ] Multi-pass overwrite implementation

### **Phase 2: Certificate System** 🚧
- [ ] JSON log generation
- [ ] RSA digital signatures
- [ ] PDF certificate creation
- [ ] Metadata collection

### **Phase 3: Verification System** 📋
- [ ] Signature verification CLI
- [ ] Web verification portal
- [ ] Certificate validation

### **Phase 4: UI and Polish** 📋
- [ ] Rich TUI interface
- [ ] CLI interface improvements
- [ ] Bootable ISO creation
- [ ] Cross-platform deployment

## 🧪 **Testing**

### **Development Testing (Windows/Mac)**
```bash
# Run device scanner
docker compose exec saferase-dev python test_device_scan.py

# Run specific tests
docker compose exec saferase-dev python -m pytest tests/

# Run with coverage
docker compose exec saferase-dev python -m pytest --cov=src tests/
```

### **Real Device Testing (Linux)**
```bash
# Test with actual hardware
docker run --rm -v /dev:/dev:ro saferase-pro

# Test specific functionality
docker run --rm -v /dev:/dev:ro saferase-pro python -c "from src.wipe_engine import wipe_device; wipe_device('/dev/sdb')"
```

## 📚 **Documentation**

- **[Team Setup Guide](TEAM_SETUP.md)** - Complete team setup instructions
- **[Development Guide](DEVELOPMENT.md)** - Simple development guide for beginners

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 **Goals**

- **Build user trust** in data wiping
- **Promote safe e-waste disposal**
- **Boost circular economy**
- **Comply with NIST SP 800-88 standards**
- **Open source and auditable**

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/SafeErasePro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/SafeErasePro/discussions)
- **Documentation**: Check the `docs/` folder

## 🙏 **Acknowledgments**

- NIST SP 800-88 guidelines for data sanitization
- Linux disk utilities community
- Python cryptography libraries
- Docker community for containerization

---

**⚠️ Important:** This is a development environment. Always test in a safe, isolated environment first. No actual data wiping operations are performed in development mode.
