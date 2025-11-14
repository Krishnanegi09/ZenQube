#!/usr/bin/env python3
"""
Code Analysis and Vulnerability Detection Module
Analyzes code for common security vulnerabilities and issues
"""

import re
import os
import json
from typing import List, Dict, Tuple
from pathlib import Path

class CodeAnalyzer:
    def __init__(self):
        self.vulnerabilities = []
        self.warnings = []
        self.info = []
        
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a code file for vulnerabilities"""
        self.vulnerabilities = []
        self.warnings = []
        self.info = []
        
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.c' or file_ext == '.cpp' or file_ext in ['.cc', '.cxx']:
            return self._analyze_c_cpp(file_path)
        elif file_ext == '.py':
            return self._analyze_python(file_path)
        elif file_ext == '.java':
            return self._analyze_java(file_path)
        else:
            return {"error": f"Unsupported file type: {file_ext}"}
    
    def _analyze_c_cpp(self, file_path: str) -> Dict:
        """Analyze C/C++ code"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for buffer overflow vulnerabilities
        self._check_buffer_overflow(content, lines)
        
        # Check for memory leaks
        self._check_memory_leaks(content, lines)
        
        # Check for unsafe functions
        self._check_unsafe_functions(content, lines)
        
        # Check for format string vulnerabilities
        self._check_format_strings(content, lines)
        
        # Check for integer overflow
        self._check_integer_overflow(content, lines)
        
        # Check for command injection
        self._check_command_injection(content, lines)
        
        # Check for race conditions
        self._check_race_conditions(content, lines)
        
        return self._generate_report(file_path)
    
    def _analyze_python(self, file_path: str) -> Dict:
        """Analyze Python code"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for eval/exec usage
        self._check_eval_exec(content, lines)
        
        # Check for SQL injection
        self._check_sql_injection(content, lines)
        
        # Check for command injection
        self._check_command_injection(content, lines)
        
        # Check for hardcoded secrets
        self._check_hardcoded_secrets(content, lines)
        
        # Check for unsafe deserialization
        self._check_unsafe_deserialization(content, lines)
        
        return self._generate_report(file_path)
    
    def _analyze_java(self, file_path: str) -> Dict:
        """Analyze Java code"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for SQL injection
        self._check_sql_injection(content, lines)
        
        # Check for command injection
        self._check_command_injection(content, lines)
        
        # Check for XSS vulnerabilities
        self._check_xss(content, lines)
        
        return self._generate_report(file_path)
    
    def _check_buffer_overflow(self, content: str, lines: List[str]):
        """Check for buffer overflow vulnerabilities"""
        # Check for unsafe string functions
        unsafe_funcs = [
            (r'\bstrcpy\s*\(', 'HIGH', 'Use of strcpy() can cause buffer overflow. Use strncpy() or strcpy_s() instead.'),
            (r'\bstrcat\s*\(', 'HIGH', 'Use of strcat() can cause buffer overflow. Use strncat() instead.'),
            (r'\bsprintf\s*\(', 'MEDIUM', 'Use of sprintf() can cause buffer overflow. Use snprintf() instead.'),
            (r'\bgets\s*\(', 'CRITICAL', 'Use of gets() is dangerous. Use fgets() instead.'),
        ]
        
        for pattern, severity, message in unsafe_funcs:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    self.vulnerabilities.append({
                        'type': 'Buffer Overflow',
                        'severity': severity,
                        'line': i,
                        'message': message,
                        'code': line.strip()
                    })
    
    def _check_memory_leaks(self, content: str, lines: List[str]):
        """Check for potential memory leaks"""
        malloc_lines = {}
        free_lines = {}
        
        for i, line in enumerate(lines, 1):
            # Find malloc/calloc/realloc
            if re.search(r'\bmalloc\s*\(|\bcalloc\s*\(|\brealloc\s*\(', line):
                # Try to extract variable name
                match = re.search(r'(\w+)\s*=\s*(?:\([^)]+\))?\s*(?:malloc|calloc|realloc)', line)
                if match:
                    var_name = match.group(1)
                    malloc_lines[var_name] = i
            
            # Find free
            if re.search(r'\bfree\s*\(', line):
                match = re.search(r'free\s*\(\s*(\w+)', line)
                if match:
                    var_name = match.group(1)
                    free_lines[var_name] = i
        
        # Check for malloc without corresponding free
        for var, line_num in malloc_lines.items():
            if var not in free_lines:
                self.warnings.append({
                    'type': 'Potential Memory Leak',
                    'severity': 'MEDIUM',
                    'line': line_num,
                    'message': f'Variable {var} allocated but may not be freed.',
                    'code': lines[line_num - 1].strip()
                })
    
    def _check_unsafe_functions(self, content: str, lines: List[str]):
        """Check for unsafe function usage"""
        unsafe = [
            (r'\bsystem\s*\(', 'HIGH', 'Use of system() can lead to command injection.'),
            (r'\bpopen\s*\(', 'MEDIUM', 'Use of popen() can be unsafe.'),
        ]
        
        for pattern, severity, message in unsafe:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    self.warnings.append({
                        'type': 'Unsafe Function',
                        'severity': severity,
                        'line': i,
                        'message': message,
                        'code': line.strip()
                    })
    
    def _check_format_strings(self, content: str, lines: List[str]):
        """Check for format string vulnerabilities"""
        for i, line in enumerate(lines, 1):
            # Check printf with user input
            if re.search(r'\bprintf\s*\([^,)]+\w+[^,)]*\)', line):
                if re.search(r'%[sdifx]', line):
                    self.vulnerabilities.append({
                        'type': 'Format String Vulnerability',
                        'severity': 'HIGH',
                        'line': i,
                        'message': 'Potential format string vulnerability. Validate user input.',
                        'code': line.strip()
                    })
    
    def _check_integer_overflow(self, content: str, lines: List[str]):
        """Check for integer overflow"""
        for i, line in enumerate(lines, 1):
            # Check for arithmetic without bounds checking
            if re.search(r'\+\+|--|\+\s*[0-9]|\*\s*[0-9]', line):
                if 'int' in line or 'long' in line:
                    self.warnings.append({
                        'type': 'Potential Integer Overflow',
                        'severity': 'MEDIUM',
                        'line': i,
                        'message': 'Check for integer overflow in arithmetic operations.',
                        'code': line.strip()
                    })
    
    def _check_command_injection(self, content: str, lines: List[str]):
        """Check for command injection vulnerabilities"""
        dangerous_patterns = [
            (r'os\.system\s*\(', 'Python'),
            (r'subprocess\.call\s*\(', 'Python'),
            (r'Runtime\.getRuntime\(\)\.exec', 'Java'),
            (r'ProcessBuilder', 'Java'),
        ]
        
        for pattern, lang in dangerous_patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    # Check if user input is used
                    if 'input(' in line or 'argv' in line or 'args' in line:
                        self.vulnerabilities.append({
                            'type': 'Command Injection',
                            'severity': 'CRITICAL',
                            'line': i,
                            'message': f'Potential command injection in {lang}. Validate and sanitize user input.',
                            'code': line.strip()
                        })
    
    def _check_eval_exec(self, content: str, lines: List[str]):
        """Check for eval/exec usage in Python"""
        for i, line in enumerate(lines, 1):
            if re.search(r'\beval\s*\(|\bexec\s*\(', line):
                self.vulnerabilities.append({
                    'type': 'Code Injection',
                    'severity': 'CRITICAL',
                    'line': i,
                    'message': 'Use of eval() or exec() is dangerous. Avoid if possible.',
                    'code': line.strip()
                })
    
    def _check_sql_injection(self, content: str, lines: List[str]):
        """Check for SQL injection vulnerabilities"""
        sql_patterns = [
            r'execute\s*\([^)]*\+',
            r'query\s*\([^)]*\+',
            r'SELECT.*\+.*FROM',
            r'INSERT.*\+.*INTO',
        ]
        
        for pattern in sql_patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self.vulnerabilities.append({
                        'type': 'SQL Injection',
                        'severity': 'CRITICAL',
                        'line': i,
                        'message': 'Potential SQL injection. Use parameterized queries.',
                        'code': line.strip()
                    })
    
    def _check_hardcoded_secrets(self, content: str, lines: List[str]):
        """Check for hardcoded secrets"""
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret'),
        ]
        
        for pattern, msg in secret_patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self.vulnerabilities.append({
                        'type': 'Hardcoded Secret',
                        'severity': 'HIGH',
                        'line': i,
                        'message': msg + '. Use environment variables or secure storage.',
                        'code': line.strip()
                    })
    
    def _check_unsafe_deserialization(self, content: str, lines: List[str]):
        """Check for unsafe deserialization"""
        for i, line in enumerate(lines, 1):
            if re.search(r'pickle\.loads|yaml\.load|marshal\.loads', line):
                self.vulnerabilities.append({
                    'type': 'Unsafe Deserialization',
                    'severity': 'HIGH',
                    'line': i,
                    'message': 'Unsafe deserialization can lead to code execution.',
                    'code': line.strip()
                })
    
    def _check_race_conditions(self, content: str, lines: List[str]):
        """Check for potential race conditions"""
        for i, line in enumerate(lines, 1):
            if re.search(r'access\s*\(|stat\s*\(|open\s*\(', line):
                # Check if file operation is followed by another file operation
                if i < len(lines) - 1:
                    next_line = lines[i]
                    if re.search(r'open\s*\(|read\s*\(|write\s*\(', next_line):
                        self.warnings.append({
                            'type': 'Potential Race Condition',
                            'severity': 'MEDIUM',
                            'line': i,
                            'message': 'Potential race condition in file operations.',
                            'code': line.strip()
                        })
    
    def _check_xss(self, content: str, lines: List[str]):
        """Check for XSS vulnerabilities in Java"""
        for i, line in enumerate(lines, 1):
            if re.search(r'response\.getWriter\(\)\.print|out\.print', line):
                if 'request.getParameter' in line or 'request.getAttribute' in line:
                    self.vulnerabilities.append({
                        'type': 'XSS Vulnerability',
                        'severity': 'HIGH',
                        'line': i,
                        'message': 'Potential XSS. Sanitize user input before output.',
                        'code': line.strip()
                    })
    
    def _generate_report(self, file_path: str) -> Dict:
        """Generate analysis report"""
        total_issues = len(self.vulnerabilities) + len(self.warnings)
        critical = sum(1 for v in self.vulnerabilities if v['severity'] == 'CRITICAL')
        high = sum(1 for v in self.vulnerabilities if v['severity'] == 'HIGH')
        medium = sum(1 for v in self.vulnerabilities + self.warnings if v['severity'] == 'MEDIUM')
        
        return {
            'file': file_path,
            'total_issues': total_issues,
            'critical': critical,
            'high': high,
            'medium': medium,
            'vulnerabilities': self.vulnerabilities,
            'warnings': self.warnings,
            'info': self.info
        }

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: code_analyzer.py <file_path>")
        sys.exit(1)
    
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file(sys.argv[1])
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()

