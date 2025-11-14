#!/usr/bin/env python3
"""
ZenCube Sandbox Test Suite - Cross-Platform
Tests various aspects of the sandbox implementation
Works on Windows, macOS, and Linux
"""

import sys
import os
import subprocess
import platform

# Colors for output
if platform.system() == "Windows":
    try:
        import colorama
        colorama.init()
    except ImportError:
        class colorama:
            class Fore:
                GREEN = ''
                RED = ''
                YELLOW = ''
                BLUE = ''
                RESET = ''
else:
    class colorama:
        class Fore:
            GREEN = '\033[0;32m'
            RED = '\033[0;31m'
            YELLOW = '\033[1;33m'
            BLUE = '\033[0;34m'
            RESET = '\033[0m'

GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
RESET = colorama.Fore.RESET

def get_sandbox_exe():
    """Get the sandbox executable path"""
    if platform.system() == "Windows":
        return "sandbox.exe"
    else:
        return "./sandbox"

def get_test_exe(name):
    """Get test executable path"""
    if platform.system() == "Windows":
        return f"tests\\{name}.exe"
    else:
        return f"./tests/{name}"

def run_command(cmd, capture_output=True, timeout=30):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            timeout=timeout,
            text=True
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def print_header(text):
    """Print a test header"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}  {text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}")

def print_result(test_name, passed):
    """Print test result"""
    if passed:
        print(f"{GREEN}✅ PASS{RESET}: {test_name}")
        return True
    else:
        print(f"{RED}❌ FAIL{RESET}: {test_name}")
        return False

def main():
    sandbox_exe = get_sandbox_exe()
    
    # Check if sandbox exists
    if not os.path.exists(sandbox_exe):
        print(f"{RED}Error: sandbox binary not found. Please build the project first.{RESET}")
        print(f"  Windows: cmake --build build --config Release")
        print(f"  Unix/Mac: cmake -B build && cmake --build build")
        return 1
    
    print(f"{YELLOW}╔═══════════════════════════════════════════════════════════════╗")
    print(f"║        ZenCube Sandbox Test Suite - Cross-Platform           ║")
    print(f"║              Platform: {platform.system():<27} ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Basic command execution
    print_header("Test 1: Basic Command Execution")
    if platform.system() == "Windows":
        cmd = f'{sandbox_exe} cmd /c echo "Hello from ZenCube!"'
    else:
        cmd = f'{sandbox_exe} /bin/echo "Hello from ZenCube!"'
    
    returncode, stdout, stderr = run_command(cmd)
    if print_result("Basic execution", returncode == 0):
        tests_passed += 1
    else:
        tests_failed += 1
        print(f"  Output: {stdout}")
        print(f"  Error: {stderr}")
    
    # Test 2: Command with arguments
    print_header("Test 2: Command with Arguments")
    if platform.system() == "Windows":
        cmd = f'{sandbox_exe} cmd /c dir'
    else:
        cmd = f'{sandbox_exe} /bin/ls -la'
    
    returncode, stdout, stderr = run_command(cmd)
    if print_result("Arguments test", returncode == 0):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 3: Timing functionality
    print_header("Test 3: Timing Functionality")
    if platform.system() == "Windows":
        cmd = f'{sandbox_exe} timeout /t 1 /nobreak'
    else:
        cmd = f'{sandbox_exe} /bin/sleep 1'
    
    returncode, stdout, stderr = run_command(cmd, timeout=5)
    if print_result("Timing test", returncode == 0):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 4: Error handling - invalid command
    print_header("Test 4: Error Handling")
    if platform.system() == "Windows":
        cmd = f'{sandbox_exe} nonexistent_command.exe'
    else:
        cmd = f'{sandbox_exe} /nonexistent/command'
    
    returncode, stdout, stderr = run_command(cmd)
    if print_result("Error handling", returncode != 0):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 5: Help message
    print_header("Test 5: Help and Usage Information")
    cmd = f'{sandbox_exe} --help'
    returncode, stdout, stderr = run_command(cmd)
    if "OPTIONS" in stdout or "cpu" in stdout.lower():
        if print_result("Help message", True):
            tests_passed += 1
    else:
        if print_result("Help message", False):
            tests_failed += 1
    
    # Test 6: No arguments
    print_header("Test 6: No Arguments Error Handling")
    cmd = f'{sandbox_exe}'
    returncode, stdout, stderr = run_command(cmd)
    if print_result("No arguments test", returncode != 0):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Summary
    print(f"\n{YELLOW}{'=' * 60}{RESET}")
    print(f"{YELLOW}                    TEST SUMMARY                       {RESET}")
    print(f"{YELLOW}{'=' * 60}{RESET}")
    print(f"Total Tests:  {BLUE}{tests_passed + tests_failed}{RESET}")
    print(f"Passed:       {GREEN}{tests_passed}{RESET}")
    print(f"Failed:       {RED}{tests_failed}{RESET}")
    print(f"{YELLOW}{'=' * 60}{RESET}\n")
    
    if tests_failed == 0:
        print(f"{GREEN}🎉 All tests passed!{RESET}")
        return 0
    else:
        print(f"{RED}⚠️  Some tests failed.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())












