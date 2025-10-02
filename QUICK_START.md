# Shoonya Wipe Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Start the Application
```bash
# Clone the repository
git clone https://github.com/jessicaagarwal/shoonya-wipe.git
cd shoonya-wipe

# Start with Docker (recommended)
docker compose up -d
```

### Step 2: Access the Web Interface
- Open your browser to: **http://localhost:5000**
- You'll see the Shoonya Wipe web interface

### Step 3: Run a Test Wipe
1. **Select Device** - Choose VDISK0 (virtual test disk)
2. **Continue to Method** - System will auto-select NIST Clear method
3. **Start Wipe** - Click "Start Wipe" to begin
4. **Watch Progress** - See real-time progress simulation
5. **Download Certificates** - Get your NIST-compliant certificates

### Step 4: Verify Results
- **wipelog.json** - Detailed wipe log
- **wipelog_signed.json** - Digitally signed log
- **nist_certificate.pdf** - NIST-compliant PDF certificate

## 🎯 What You'll See

### Web Interface Features
- **Device Selection** - Choose from available virtual disks
- **NIST Compliance** - Automatic method selection based on device type
- **Progress Tracking** - Real-time progress with realistic timing
- **Certificate Generation** - Automatic PDF and JSON certificate creation
- **File Download** - Easy download of generated certificates

### Generated Certificates
- **NIST SP 800-88r2 Compliant** - Meets all NIST requirements
- **Digitally Signed** - Cryptographically secure and tamper-proof
- **Complete Audit Trail** - Full documentation of the wipe process
- **Professional Format** - Ready for compliance reporting

## 🛡️ Safety Features

### Docker Sandboxing
- **No Real Drive Access** - Cannot accidentally wipe real drives
- **Virtual Media Only** - Uses 2GB virtual disk images for testing
- **Isolated Environment** - All operations run in Docker containers
- **Safe Testing** - Full functionality without risk

### NIST Compliance
- **Clear Method** - Single-pass overwrite for magnetic media
- **Purge Method** - SSD secure erase and cryptographic erase
- **AI Decision Flow** - Intelligent method selection
- **Verification** - Comprehensive compliance checking

## 🔧 Troubleshooting

### Common Issues

#### "Cannot access web interface"
```bash
# Check if Docker is running
docker ps

# Restart if needed
docker compose restart
```

#### "No devices found"
- Virtual disks are created automatically
- Check Docker container logs: `docker logs safeerase-pro-web`

#### "Wipe process stuck"
- Refresh the page and try again
- Check container logs for errors

### Getting Help
- Check the logs: `docker logs safeerase-pro-web -f`
- Review the API documentation: `API_DOCUMENTATION.md`
- See the development guide: `DEVELOPMENT_GUIDE.md`

## 📋 Next Steps

### For Testing
1. Try different device types (VDISK0, VDISK1)
2. Test the verification process
3. Download and examine certificates
4. Try the CLI interface: `docker compose exec shoonya-wipe-web python main.py cli`

### For Development
1. Read the development guide: `DEVELOPMENT_GUIDE.md`
2. Explore the code structure
3. Make modifications and test
4. Contribute back to the project

### For Production
1. Review security considerations
2. Add authentication if needed
3. Deploy with proper monitoring
4. Follow NIST guidelines for real devices

## 🎉 Success!

You've successfully:
- ✅ Set up Shoonya Wipe
- ✅ Run a test wipe process
- ✅ Generated NIST-compliant certificates
- ✅ Verified the system works

**Shoonya Wipe is now ready for use!** 🌱
