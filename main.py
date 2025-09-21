#!/usr/bin/env python3
"""
SafeErasePro - Main Entry Point

This is the main entry point for SafeErasePro.
It provides access to all the different modes and interfaces.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def show_help():
    """Show help information."""
    print("🔒 SafeErasePro - Secure Data Wiping Tool")
    print("==========================================")
    print()
    print("Usage: python main.py [command]")
    print()
    print("Commands:")
    print("  cli         - Run CLI interface (safeerase.py)")
    print("  web         - Run web GUI interface")
    print("  verify      - Run verification tool")
    print("  portable    - Create portable package")
    print("  help        - Show this help")
    print()
    print("Examples:")
    print("  python main.py cli      # Start CLI interface")
    print("  python main.py web      # Start web GUI")
    print("  python main.py verify   # Run verification")
    print("  python main.py portable # Create portable package")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return 1
    
    command = sys.argv[1].lower()
    
    if command == "cli":
        # Call the core CLI directly
        from core.safeerase import main as cli_main
        return cli_main()
    
    elif command == "web":
        from web.web_gui import app
        print("🌐 Starting SafeErasePro Web GUI...")
        print("📱 Open your browser to: http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
        return 0
    
    elif command == "verify":
        from core.verify import main as verify_main
        return verify_main()
    
    elif command == "portable":
        from scripts.offline_mode import main as portable_main
        return portable_main()
    
    elif command == "help":
        show_help()
        return 0
    
    elif command == "engine":
        # Minimal one-click engine run (for testing)
        from core.engine.dispatcher import execute
        from core.engine.utils import Device
        dev = Device(name="VDISK0", path=os.environ.get("SANDBOX_DEVICE", "/app/virtual_media/vdisk0.img"), model="Sandbox VDisk", transport="file", media_type="Flash Memory", size="2G")
        out = execute(dev, operator_name=os.environ.get("OP_NAME", "Operator"), operator_title=os.environ.get("OP_TITLE", "Tester"), always_encrypted=False)
        print(out)
        return 0
    
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
