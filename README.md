# ZenCube 🧊

**Advanced Sandbox with Real-time Monitoring, Code Analysis & Web Dashboard**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://www.linux.org/)
[![Language](https://img.shields.io/badge/language-C%20%7C%20Python-orange.svg)](https://en.wikipedia.org/wiki/C_(programming_language))

---

## 🎯 Overview

**ZenCube** is an advanced educational sandbox project that demonstrates process isolation, resource management, and security concepts. It features:

- ✅ **Real-time Resource Monitoring** - Live CPU, memory, and performance tracking
- ✅ **Code Analysis & Vulnerability Detection** - Static analysis for security issues
- ✅ **Web Dashboard** - Beautiful Flask-based interface with live charts
- ✅ **Enhanced CLI** - Command-line interface with all features
- ✅ **Cross-Platform** - Works on Windows, macOS, and Linux
- ✅ **Multi-Language Support** - Test Python, Java, C, C++ files

---

## ✨ Unique Features

### 1. Real-time Resource Monitoring
- Live CPU and memory usage graphs
- Real-time performance metrics
- Process thread and file descriptor tracking
- Visual resource consumption timeline

### 2. Code Analysis & Vulnerability Detection
- Static code analysis for C/C++, Python, and Java
- Detects buffer overflows, memory leaks, SQL injection
- Identifies unsafe functions and security vulnerabilities
- Detailed reports with line numbers and recommendations

### 3. Web Dashboard
- Modern, responsive web interface
- Real-time WebSocket updates
- Interactive resource charts (Chart.js)
- Code analysis integration
- Beautiful gradient UI design

### 4. Enhanced CLI
- Analyze code from command line
- Monitor running processes
- Run programs in sandbox with limits
- JSON output support

---

## 📦 Installation

### 1. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Build the sandbox executable

```bash
make               # macOS / Linux
# or
cmake -B build && cmake --build build
```

### 3. Optional (Windows)

Use CMake or Visual Studio to produce `sandbox.exe` next to the project files.

---

## ⚡ Quick Start

```bash
# Launch the desktop sandbox GUI (interactive terminal)
python3 run.py

# Launch the Flask web dashboard
python3 run.py --mode web

# Quick CLI demo (after building the sandbox)
./sandbox python3 examples/hello_python.py
```

1. **GUI workflow** – Click “📁 Browse File”, adjust limits if needed, then hit **Analyze & Run in Sandbox**.
2. **Web dashboard** – Upload a file, analyze it, and run with live monitoring.
3. **Command line** – Use the sandbox binary directly or the CLI helpers.

---

## 🚀 Usage

### Desktop GUI (default `python3 run.py`)

1. Press **📁 Browse File** and pick the program you want to test (supports executables, `.py`, `.java`, `.c`, `.cpp`, `.sh`, `.js`, `.rb`, `.pl`, …).
2. (Optional) Toggle CPU time, memory, process-count, or file-size limits.
3. Click **Analyze & Run in Sandbox** to see vulnerability findings followed by interactive program output. Type directly into the terminal when your program prompts for input.
4. Use **⏹ Stop** to terminate the program or **🧹 Clear** to reset the terminal with instructions.

### Web Dashboard

1. Start the server:
   ```bash
   python3 run.py --mode web
   ```
2. Open your browser at `http://localhost:5000`.
3. Upload files, trigger vulnerability scans, run programs with limits, and watch resource charts update live.

### CLI & Direct Sandbox

```bash
# Analyze code for vulnerabilities
python3 cli.py analyze examples/hello_python.py

# Run a program with limits via the CLI
python3 cli.py run --cpu=10 --memory=256 python3 examples/hello_python.py

# Monitor a running process
python3 cli.py monitor 12345

# Direct sandbox usage
./sandbox python3 examples/hello_python.py
./sandbox --cpu=5 --mem=100 python3 examples/hello_python.py
```

---

## 📊 Features in Detail

### Real-time Monitoring
- Tracks CPU usage percentage
- Monitors memory consumption (RSS and virtual)
- Counts threads and file descriptors
- Updates every 500ms via WebSocket

### Code Analysis
Detects:
- Buffer overflows (strcpy, gets, etc.)
- Memory leaks
- SQL injection
- Command injection
- Format string vulnerabilities
- Hardcoded secrets
- Unsafe deserialization
- XSS vulnerabilities

### Web Dashboard
- **Code Analysis Tab**: Upload and analyze files
- **Run Sandbox Tab**: Execute programs with limits
- **Real-time Charts**: Live resource usage graphs
- **Output Viewer**: Real-time program output
- **Vulnerability Reports**: Detailed security findings

---

## 🛠️ Project Structure

```
demo/
├── sandbox.c              # Core sandbox implementation
├── sandbox                # Compiled sandbox executable
├── web_dashboard.py       # Flask web server
├── sandbox_test_gui.py    # Tkinter desktop GUI
├── cli.py                 # Enhanced CLI
├── code_analyzer.py       # Vulnerability detection
├── run.py                 # One-command launcher (GUI / web)
├── examples/              # Ready-to-run demo programs
├── templates/
│   └── dashboard.html     # Web UI
├── static/                # CSS/JS assets for web dashboard
├── requirements.txt       # Python dependencies
└── tests/                 # Limit stress tests
```

---

## 🎓 Educational Value

This project demonstrates:
- **Process Management**: fork(), execvp(), waitpid()
- **Resource Limits**: setrlimit(), RLIMIT_*
- **System Monitoring**: /proc filesystem, psutil
- **Web Development**: Flask, WebSockets, real-time updates
- **Security**: Static analysis, vulnerability detection
- **Cross-platform**: Windows, macOS, Linux support

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👥 Authors

**Systems Programming Team** - 2025

---

**ZenCube** - *Advanced Sandbox with Real-time Monitoring & Security Analysis* 🧊
