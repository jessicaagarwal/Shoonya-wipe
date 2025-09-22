#!/usr/bin/env python3
"""
Shoonya Wipe - Main Entry Point

This is the main entry point for Shoonya Wipe.
It provides access to all the different modes and interfaces.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def show_help():
    """Show help information."""
    print("🔒 Shoonya Wipe - Secure Data Wiping Tool")
    print("==========================================")
    print()
    print("Usage: python main.py [command]")
    print()
    print("Commands:")
    print("  cli         - Run CLI interface (safe mode)")
    print("  web         - Run web GUI interface (safe mode)")
    print("  verify      - Run verification tool")
    print("  engine      - One-click wipe engine (safe mode)")
    print("  production  - Production mode (real device erasing)")
    print("  portable    - Create portable package")
    print("  help        - Show this help")
    print()
    print("Examples:")
    print("  python main.py cli                    # Start CLI interface (safe)")
    print("  python main.py web                    # Start web GUI (safe)")
    print("  python main.py engine                 # One-click wipe (safe)")
    print("  python main.py verify                 # Run verification")
    print("  sudo SHOONYA_PRODUCTION_MODE=1 python main.py production  # Production mode")
    print("  python main.py portable               # Create portable package")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return 1
    
    command = sys.argv[1].lower()
    
    if command == "cli":
        # Call the core CLI directly
        from core.safe.safeerase import main as cli_main
        return cli_main()
    
    elif command == "web":
        from web.web_gui import app
        print("🌐 Starting Shoonya Wipe Web GUI...")
        print("📱 Open your browser to: http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
        return 0
    
    elif command == "verify":
        from core.safe.verify import main as verify_main
        return verify_main()
    
    elif command == "portable":
        from scripts.offline_mode import main as portable_main
        return portable_main()
    
    elif command == "production":
        from core.production.production_mode import production_manager
        from core.shared.device_detection import DeviceDetector
        from engine.production.real_dispatcher import RealDispatcher
        
        # Check if production mode is enabled
        if not production_manager.enable_production_mode():
            print("❌ Production mode not enabled or not running as root")
            print("   Set SHOONYA_PRODUCTION_MODE=1 and run as root")
            return 1
        
        print("🔒 Shoonya Wipe - Production Mode")
        print("⚠️  WARNING: This mode will erase REAL devices!")
        print("=" * 50)
        
        # Detect devices
        detector = DeviceDetector()
        devices = detector.detect_devices()
        
        if not devices:
            print("❌ No devices found")
            return 1
        
        # Show available devices
        print("\nAvailable devices:")
        for i, device in enumerate(devices):
            print(f"  {i+1}. {device.name} - {device.path} ({device.size})")
        
        # Get device selection
        try:
            choice = int(input("\nSelect device (number): ")) - 1
            if choice < 0 or choice >= len(devices):
                print("❌ Invalid device selection")
                return 1
            
            selected_device = devices[choice]
            print(f"\nSelected: {selected_device.name} - {selected_device.path}")
            
            # Execute wipe
            dispatcher = RealDispatcher()
            success = dispatcher.run_one_click_wipe(selected_device)
            
            if success:
                print("✅ Wipe completed successfully")
                return 0
            else:
                print("❌ Wipe failed")
                return 1
                
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Operation cancelled")
            return 1
    
    elif command == "help":
        show_help()
        return 0
    
    elif command == "engine":
        # Safe mode one-click engine
        from engine.safe.dispatcher import execute
        from engine.safe.utils import Device
        import os
        
        # Create a test device
        device = Device(
            name="VDISK0", 
            path=os.environ.get("SANDBOX_DEVICE", "/app/virtual_media/vdisk0.img"), 
            model="Sandbox VDisk", 
            transport="file", 
            media_type="Flash Memory", 
            size="2G"
        )
        
        # Execute wipe
        result = execute(device, "Test Operator", "Tester", False)
        print("✅ Engine test completed successfully")
        print(f"Method: {result['choice']['method']}")
        print(f"Technique: {result['choice']['technique']}")
        return 0
    
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
