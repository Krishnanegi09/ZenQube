#!/usr/bin/env python3
"""
ZenCube Build Script - Cross-Platform
Builds the sandbox on Windows, macOS, and Linux
"""

import sys
import os
import platform
import subprocess
import shutil

def print_status(message):
    """Print status message"""
    print(f"▶ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ Error: {message}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def check_cmake():
    """Check if CMake is available"""
    try:
        result = subprocess.run(["cmake", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print_status(f"Found {version}")
            return True
    except FileNotFoundError:
        pass
    return False

def check_compiler():
    """Check if a suitable C compiler is available"""
    system = platform.system()
    
    if system == "Windows":
        # Check for MSVC or MinGW
        try:
            result = subprocess.run(["cl"], capture_output=True, text=True)
            if result.returncode == 0 or result.returncode == 9009:  # MSVC
                print_status("Found MSVC compiler")
                return True
        except FileNotFoundError:
            pass
        
        try:
            result = subprocess.run(["gcc", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print_status("Found MinGW/GCC compiler")
                return True
        except FileNotFoundError:
            pass
    else:
        # Check for GCC or Clang
        compilers = ["gcc", "clang"]
        for compiler in compilers:
            try:
                result = subprocess.run([compiler, "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.split('\n')[0]
                    print_status(f"Found {version}")
                    return True
            except FileNotFoundError:
                continue
    
    return False

def build_with_cmake(build_dir="build", config="Release"):
    """Build using CMake"""
    system = platform.system()
    
    print_status("Configuring CMake...")
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    if system == "Windows":
        cmake_cmd = ["cmake", "-B", build_dir, "-S", ".", "-DCMAKE_BUILD_TYPE=" + config]
    else:
        cmake_cmd = ["cmake", "-B", build_dir, "-S", ".", "-DCMAKE_BUILD_TYPE=" + config]
    
    result = subprocess.run(cmake_cmd)
    if result.returncode != 0:
        print_error("CMake configuration failed")
        return False
    
    print_status("Building project...")
    if system == "Windows":
        build_cmd = ["cmake", "--build", build_dir, "--config", config]
    else:
        build_cmd = ["cmake", "--build", build_dir]
    
    result = subprocess.run(build_cmd)
    if result.returncode != 0:
        print_error("Build failed")
        return False
    
    print_success("Build completed successfully!")
    
    # Show where binaries are located
    if system == "Windows":
        exe_path = os.path.join(build_dir, config, "sandbox.exe")
    else:
        exe_path = os.path.join(build_dir, "sandbox")
    
    if os.path.exists(exe_path):
        print_status(f"Binary created: {exe_path}")
    
    return True

def build_with_make():
    """Build using Make (Unix systems only)"""
    print_status("Building with Make...")
    result = subprocess.run(["make", "all"])
    if result.returncode != 0:
        print_error("Make build failed")
        return False
    
    print_success("Build completed successfully!")
    if os.path.exists("./sandbox"):
        print_status("Binary created: ./sandbox")
    
    return True

def main():
    system = platform.system()
    print(f"╔═══════════════════════════════════════════════════════════════╗")
    print(f"║              ZenCube Build System                           ║")
    print(f"║              Platform: {system:<29} ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝\n")
    
    # Check for CMake
    has_cmake = check_cmake()
    
    if not has_cmake:
        print_error("CMake not found")
        print_status("Attempting to install CMake...")
        print_status("Please install CMake from https://cmake.org/download/")
        
        if system == "Windows":
            print("  Or use: winget install Kitware.CMake")
        elif system == "Darwin":
            print("  Or use: brew install cmake")
        else:
            print("  Or use: sudo apt-get install cmake (Ubuntu/Debian)")
            print("  Or use: sudo dnf install cmake (Fedora/RHEL)")
        
        return 1
    
    # Check for compiler
    if not check_compiler():
        print_error("No suitable C compiler found")
        print_status("Please install a C compiler:")
        if system == "Windows":
            print("  - MSVC: Install Visual Studio")
            print("  - MinGW: Install MSYS2 or MinGW-w64")
        elif system == "Darwin":
            print("  - Xcode Command Line Tools: xcode-select --install")
        else:
            print("  - GCC: sudo apt-get install build-essential")
        
        return 1
    
    # Build using CMake (preferred method)
    if has_cmake:
        success = build_with_cmake()
        if success:
            return 0
    
    # Fallback to Make on Unix systems
    if system != "Windows":
        print_status("Falling back to Make...")
        if os.path.exists("Makefile"):
            success = build_with_make()
            if success:
                return 0
    
    print_error("Build failed")
    return 1

if __name__ == "__main__":
    sys.exit(main())












