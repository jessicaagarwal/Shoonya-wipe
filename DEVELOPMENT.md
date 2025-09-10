# SafeErasePro - Development Guide

## 🎯 **What We're Building**

SafeErasePro is a data wiping tool that runs on Linux. We develop on Windows/Mac using Docker, and test on a Linux laptop.

## 👥 **Team Setup**

- **Windows/Mac Team:** Develop code in Docker containers
- **Linux Laptop:** Test with real devices (when ready)

## 🚀 **Simple Development Commands**

### **Start Working (Every Day)**
```bash
# 1. Get latest code
git pull

# 2. Start development environment
docker compose up -d

# 3. Test that everything works
docker compose exec saferase-dev python test_device_scan.py
```

### **While Developing**
```bash
# Test your changes
docker compose exec saferase-dev python test_device_scan.py

# Stop when done
docker compose down
```

### **Save Your Work**
```bash
# Add all changes
git add .

# Save with a message
git commit -m "Added new feature"

# Send to team
git push
```

## 📁 **Project Structure**

```
SafeErasePro/
├── src/                    # Your code goes here
├── tests/                  # Test files
├── Dockerfile              # Development environment
├── docker-compose.yml      # Easy container management
└── README.md              # Main project info
```

## 🎯 **What We're Building (Step by Step)**

### **Phase 1: Device Scanner** ✅
- [x] Find all devices on computer
- [x] Show device information
- [ ] Choose which device to wipe

### **Phase 2: Wipe Engine** 🚧
- [ ] Wipe files safely
- [ ] Wipe free space
- [ ] Wipe SSDs properly

### **Phase 3: Certificates** 📋
- [ ] Create PDF certificate
- [ ] Add digital signature
- [ ] Save wipe proof

### **Phase 4: Verification** 📋
- [ ] Check if certificate is real
- [ ] Web portal for recyclers
- [ ] Easy verification

## 🧪 **Testing (Simple)**

### **Development Testing (Windows/Mac)**
```bash
# Test device scanner
docker compose exec saferase-dev python test_device_scan.py
```

### **Real Device Testing (Linux Laptop)**
```bash
# Test with real hardware
docker run --rm -v /dev:/dev:ro saferase-pro
```

## 🔒 **Safety Rules**

- ✅ Always use Docker (never run on your computer directly)
- ✅ Never test on important data
- ✅ Use Linux laptop only for real device testing
- ✅ Ask team before trying new things

## 📞 **Team Communication**

### **Daily Check-in:**
- What did you work on?
- What are you working on today?
- Any problems?

### **When You're Stuck:**
1. Check this guide first
2. Ask in team chat
3. Ask team lead for help

## 🎯 **Current Goals**

1. **This Week:** Make device scanner better
2. **Next Week:** Start building wipe engine
3. **Following Week:** Add certificate system
4. **Final Week:** Test everything together

## 📚 **Helpful Links**

- [Python Basics](https://www.python.org/about/gettingstarted/)
- [Docker Basics](https://docs.docker.com/get-started/)
- [Git Basics](https://git-scm.com/docs/gittutorial)

## 🚨 **Important Notes**

- **Always test in Docker first**
- **Ask questions if unsure**
- **Work together as a team**
- **Have fun building!**
