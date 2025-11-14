# ZenCube Deployment Guide

## 🚀 One-Command Run (Local)

Simply run:

```bash
python3 run.py
```

This will:
- ✅ Check and install dependencies automatically
- ✅ Build sandbox if needed
- ✅ Start web dashboard
- ✅ Open http://localhost:5000

---

## 🔧 Local Development

### Quick Start
```bash
python3 run.py
```

### Manual Start
```bash
# Install dependencies
pip3 install -r requirements.txt

# Build sandbox
make

# Start server
python3 web_dashboard.py
```

---

## 🌐 Remote Deployment

Cloud deployment templates are not bundled at the moment. When you are ready to deploy, you can:

- Create a Docker image for any VPS/cloud provider.
- Use Railway, Render, or your own server to run `python3 run.py`.
- Ensure the native `sandbox` binary is built on the target machine before starting the dashboard.

> 💡 Need a specific deployment recipe? Let us know the target platform (Docker, Railway, etc.) and we can generate one quickly.

---

## 🎯 Production Checklist

- [ ] Test locally: `python3 run.py`
- [ ] Install dependencies: `pip3 install -r requirements.txt`
- [ ] Build sandbox: `make` (for local use)
- [ ] Configure remote environment (optional)
- [ ] Test deployed app

---

**One Command to Rule Them All: `python3 run.py`** 🧊

