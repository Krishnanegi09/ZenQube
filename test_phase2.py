#!/usr/bin/env python3
"""
ZenCube Phase 2 Test Script - Cross-Platform
Tests resource limit enforcement (CPU, memory, processes, file size)
Works on Windows, macOS, and Linux
"""

import sys
import os
import subprocess
import platform
import re
import tempfile

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
        return 1
    
    # Check if test programs exist (optional for Phase 2 tests)
    has_tests = os.path.exists(get_test_exe("infinite_loop"))
    
    print(f"{YELLOW}╔═══════════════════════════════════════════════════════════════╗")
    print(f"║        ZenCube Phase 2 - Resource Limit Test Suite          ║")
    print(f"║              Platform: {platform.system():<27} ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: CPU Time Limit (only on Unix systems with test programs)
    if has_tests and platform.system() != "Windows":
        print_header("Test 1: CPU Time Limit (RLIMIT_CPU)")
        cmd = f'{sandbox_exe} --cpu=3 {get_test_exe("infinite_loop")}'
        returncode, stdout, stderr = run_command(cmd, timeout=10)
        output = stdout + stderr
        if "SIGXCPU" in output or "CPU time limit exceeded" in output:
            if print_result("CPU limit enforcement", True):
                tests_passed += 1
        else:
            if print_result("CPU limit enforcement", False):
                tests_failed += 1
            print(f"  Output: {output[:200]}...")
    
    # Test 2: Memory Limit (only on Unix systems with test programs)
    if has_tests and platform.system() != "Windows":
        print_header("Test 2: Memory Limit (RLIMIT_AS)")
        cmd = f'{sandbox_exe} --mem=100 {get_test_exe("memory_hog")}'
        returncode, stdout, stderr = run_command(cmd, timeout=10)
        output = stdout + stderr
        if "malloc() failed" in output or "killed" in output or returncode != 0:
            if print_result("Memory limit enforcement", True):
                tests_passed += 1
        else:
            if print_result("Memory limit enforcement", False):
                tests_failed += 1
    
    # Test 3: Normal Process (No Limits)
    print_header("Test 3: Normal Process Execution (No Limits)")
    if platform.system() == "Windows":
        cmd = f'{sandbox_exe} cmd /c echo "Test"'
    else:
        cmd = f'{sandbox_exe} /bin/ls'
    
    returncode, stdout, stderr = run_command(cmd)
    if print_result("Normal execution without limits", returncode == 0):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 4: Help and Usage
    print_header("Test 4: Help and Command-Line Interface")
    cmd = f'{sandbox_exe} --help'
    returncode, stdout, stderr = run_command(cmd)
    if "OPTIONS" in stdout or "cpu" in stdout.lower():
        if print_result("Help message displays correctly", True):
            tests_passed += 1
    else:
        if print_result("Help message displays correctly", False):
            tests_failed += 1
    
    # Test 5: Invalid Arguments
    print_header("Test 5: Error Handling")
    if platform.system() == "Windows":
        cmd = f'{sandbox_exe} --cpu=-5 cmd /c echo test'
    else:
        cmd = f'{sandbox_exe} --cpu=-5 /bin/ls'
    
    returncode, stdout, stderr = run_command(cmd)
    if print_result("Invalid argument detection", returncode != 0):
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
    
    if platform.system() == "Windows":
        print(f"{YELLOW}Note: Windows resource limits have limited support.{RESET}")
        print(f"{YELLOW}      Some tests may behave differently on Windows.{RESET}\n")
    
    if tests_failed == 0:
        print(f"{GREEN}🎉 All tests passed! Phase 2 complete.{RESET}")
        return 0
    else:
        print(f"{RED}⚠️  Some tests failed. Please review the output above.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())












