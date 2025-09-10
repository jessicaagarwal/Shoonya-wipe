# SafeErasePro - Team Setup Guide

## 🎯 **Quick Start for Team Members**

**Note:** SafeErasePro is a Linux-hosted application, but you can develop on Windows/Mac using Docker. Use the Linux laptop for testing with real devices.

### **Prerequisites (Install These First)**

#### **Windows Team Members:**
1. **Install Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop/
   - Install and restart computer
   - Start Docker Desktop

2. **Install Git**
   - Download: https://git-scm.com/download/win
   - Install with default settings

#### **Mac Team Members:**
1. **Install Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop/
   - Install and start Docker Desktop

2. **Install Git** (if not already installed)
   ```bash
   # Install Homebrew first (if not installed)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Git
   brew install git
   ```

#### **Linux Team Members (Testing Laptop):**
1. **Install Docker Engine**
   ```bash
   # Update package index
   sudo apt-get update
   
   # Install Docker
   sudo apt-get install docker.io
   
   # Start Docker service
   sudo systemctl start docker
   sudo systemctl enable docker
   
   # Add user to docker group (for running without sudo)
   sudo usermod -aG docker $USER
   # Log out and back in for group changes to take effect
   ```

2. **Install Git**
   ```bash
   sudo apt-get install git
   ```

3. **Verify Installation**
   ```bash
   # Check Docker
   docker --version
   docker ps
   
   # Check Git
   git --version
   ```

**Note:** The Linux laptop is used for testing with real devices. Windows/Mac team members develop in Docker containers.

---

## 🚀 **Setup SafeErasePro (All Team Members)**

### **Step 1: Clone the Repository**
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/SafeErasePro.git
cd SafeErasePro
```

### **Step 2: Build and Test**
```bash
# Build the Docker image
docker build -t saferase-pro .

# Test the setup
docker run --rm saferase-pro
```

**Expected Output:**
```
╭──────────────────────────────────────────────╮
│ SafeErasePro Development Environment         │
│ 🔒 Safe Device Scanner - Docker Sandbox Mode │
╰──────────────────────────────────────────────╯
✅ Running inside Docker container
```

### **Step 3: Start Development Environment**
```bash
# Start development container
docker-compose up --build

# In another terminal, run tests
docker-compose exec saferase-dev python test_device_scan.py
```

---

## 🛠️ **Development Workflow**

### **Daily Development:**
1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Start development environment:**
   ```bash
   docker-compose up -d
   ```

3. **Make your changes** to Python files

4. **Test your changes:**
   ```bash
   docker-compose exec saferase-dev python test_device_scan.py
   ```

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "Your feature description"
   git push origin main
   ```

### **Stopping Development:**
```bash
# Stop containers
docker-compose down

# Or stop and remove everything
docker-compose down --volumes --remove-orphans
```

---

## 📁 **Project Structure**

```
SafeErasePro/
├── Dockerfile              # Docker environment
├── docker-compose.yml      # Container management
├── requirements.txt        # Python dependencies
├── test_device_scan.py     # Test script
├── setup.sh               # Setup script
├── README.md              # Main documentation
├── TEAM_SETUP.md          # This file
└── .gitignore             # Git ignore rules
```

---

## 🔧 **Troubleshooting**

### **Docker Issues:**
```bash
# Check if Docker is running
docker --version
docker ps

# Rebuild if needed
docker build --no-cache -t saferase-pro .

# Clean up if stuck
docker system prune -a
```

### **Permission Issues (Linux):**
```bash
# Run with sudo if needed
sudo docker run --rm saferase-pro
```

### **Git Issues:**
```bash
# Check Git status
git status

# Reset if needed
git reset --hard HEAD
git pull origin main
```

---

## 📞 **Getting Help**

1. **Check this guide first**
2. **Ask in team chat** with error messages
3. **Check GitHub issues** for known problems
4. **Contact team lead** for complex issues

---

## ✅ **Verification Checklist**

- [ ] Docker installed and running
- [ ] Git installed
- [ ] Repository cloned
- [ ] Docker image built successfully
- [ ] Test script runs without errors
- [ ] Docker Compose works
- [ ] Can make changes and test them

**Once all checkboxes are checked, you're ready to develop! 🎉**
