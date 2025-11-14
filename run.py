#!/usr/bin/env python3
"""
ZenCube - Single Command Runner
Run this file to start everything automatically
"""

import os
import sys
import subprocess
import platform
import time
import argparse
import webbrowser

def remove_quarantine_if_needed(file_path):
    """Remove macOS quarantine attribute if present (on macOS only)"""
    if platform.system() != "Darwin":
        return
    try:
        # Check if quarantine attribute exists
        result = subprocess.run(
            ["xattr", "-l", file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "com.apple.quarantine" in result.stdout:
            # Remove quarantine attribute
            subprocess.run(
                ["xattr", "-d", "com.apple.quarantine", file_path],
                capture_output=True,
                timeout=5
            )
            print(f"🔓 Removed macOS quarantine from {file_path}")
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        # Silently fail if xattr doesn't exist or can't remove
        pass

def check_and_install_dependencies():
    """Check and install Python dependencies"""
    print("📦 Checking dependencies...")
    try:
        import flask
        import flask_socketio
        import psutil
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"⚠️  Missing dependency: {e.name}")
        print("📥 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please run manually: pip3 install -r requirements.txt")
            return False

def check_and_build_sandbox():
    """Check and build sandbox if needed"""
    sandbox_paths = [
        "./sandbox",
        "./build/sandbox",
        "./build/Release/sandbox.exe"
    ]
    
    for path in sandbox_paths:
        if os.path.exists(path):
            remove_quarantine_if_needed(path)
            print(f"✅ Sandbox found: {path}")
            return True
    
    print("🔨 Building sandbox...")
    try:
        # Try Make first
        result = subprocess.run(["make", "sandbox"], capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and os.path.exists("./sandbox"):
            remove_quarantine_if_needed("./sandbox")
            print("✅ Sandbox built successfully")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # Try CMake
        if not os.path.exists("build"):
            subprocess.run(["cmake", "-B", "build", "-DCMAKE_BUILD_TYPE=Release"], 
                         capture_output=True, timeout=60)
        subprocess.run(["cmake", "--build", "build"], capture_output=True, timeout=60)
        if os.path.exists("./build/sandbox"):
            remove_quarantine_if_needed("./build/sandbox")
            print("✅ Sandbox built successfully")
            return True
        if os.path.exists("./build/Release/sandbox.exe"):
            remove_quarantine_if_needed("./build/Release/sandbox.exe")
            print("✅ Sandbox built successfully")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠️  Could not build sandbox automatically")
    print("Please build manually: make  or  cmake -B build && cmake --build build")
    return False

def create_directories():
    """Create necessary directories"""
    dirs = ["templates", "static", "uploads"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Directories created")

def start_web_dashboard():
    """Start the web dashboard"""
    print("\n" + "="*60)
    print("🧊 Starting ZenCube Web Dashboard")
    print("="*60)
    print("\n📊 Server starting...")
    print("🌐 A browser window will open automatically. If it does not:")
    print("   http://127.0.0.1:5000")
    print("   http://localhost:5000")
    print("📁 Tip: Upload examples/hello_python.py for a quick end-to-end demo.")
    print("⏹️  Press Ctrl+C to stop\n")
    
    try:
        # Import after dependencies are checked
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from web_dashboard import app, socketio
        
        # Use 127.0.0.1 instead of 0.0.0.0 to avoid permission issues
        # Try port 5000 first, fallback to 5001
        import socket
        port = 5000
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        if result == 0:
            fallback = port + 1
            print(f"⚠️  Port {port} is in use, switching to {fallback}...")
            port = fallback

        url = f"http://127.0.0.1:{port}"
        print(f"🔗 Dashboard URL: {url}")
        try:
            webbrowser.open(url)
        except Exception:
            print("⚠️  Could not launch browser automatically. Open the link above manually.")

        socketio.run(app, host='127.0.0.1', port=port, debug=False, allow_unsafe_werkzeug=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port 5000 is already in use")
            print("Trying port 5001...")
            try:
                alt_url = "http://127.0.0.1:5001"
                print(f"🔗 Dashboard URL: {alt_url}")
                try:
                    webbrowser.open(alt_url)
                except Exception:
                    print("⚠️  Could not launch browser automatically. Open the link above manually.")
                socketio.run(app, host='127.0.0.1', port=5001, debug=False, allow_unsafe_werkzeug=True)
                print("🌐 Server running on: http://127.0.0.1:5001")
            except:
                print("❌ Could not start server. Please free up a port.")
                sys.exit(1)
        else:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTrying alternative method...")
        subprocess.run([sys.executable, "web_dashboard.py"])

def start_gui():
    """Start the interactive desktop GUI (Tkinter)"""
    print("\n" + "="*60)
    print("🖥️  Starting ZenCube Desktop GUI (Interactive Terminal)")
    print("="*60)
    print("\n📦 Ensuring sandbox is built and ready...")
    # Ensure sandbox is built (best-effort)
    check_and_build_sandbox()
    print("📁 Tip: Try the sample at examples/hello_python.py to see interactive I/O.")
    print('   Use the "Browse File" button inside the GUI to select it.')
    print("⏹️  Close the GUI window to stop\n")
    try:
        subprocess.check_call([sys.executable, "sandbox_test_gui.py"])
    except KeyboardInterrupt:
        print("\n\n👋 GUI closed")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error launching GUI: {e}")
        sys.exit(e.returncode or 1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="ZenCube - Single Command Runner")
    parser.add_argument(
        "--mode",
        choices=["gui", "web"],
        default="web",
        help="Choose how to run ZenCube: 'web' (default) launches the Flask dashboard, 'gui' opens the desktop terminal UI"
    )
    args = parser.parse_args()

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                  ZenCube Sandbox                         ║
    ║         Real-time Monitoring & Code Analysis             ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Create directories (web dashboard uses these; harmless for GUI)
    create_directories()
    
    # Step 2: Check and install dependencies
    if not check_and_install_dependencies():
        print("\n❌ Please install dependencies manually:")
        print("   pip3 install -r requirements.txt")
        sys.exit(1)
    
    if args.mode == "web":
        # Web mode: ensure sandbox then start dashboard
        check_and_build_sandbox()
        print("\n🚀 Starting web dashboard...\n")
        time.sleep(1)
        start_web_dashboard()
    else:
        # Start desktop GUI on demand
        start_gui()

if __name__ == "__main__":
    main()

