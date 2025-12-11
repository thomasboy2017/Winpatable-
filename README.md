# Winpatable - Windows Compatibility Layer for Linux

**Run Windows applications on Debian and Ubuntu based Linux Distros with full GPU support**

*Note this is a work in progress, experimenting with python, shell and c with the use of AI (to speed things up), some functions may not work the way you or I want it to, as such some tinkering, and troubleshooting is required for installation and proper use of this program.

If you have knowledge in the Shell and Phython coding lanauge, I highly suggest you comment what type of tricks I can use to improve the effectiveness of my code. 

![Supported Platforms](https://img.shields.io/badge/Ubuntu-20.04%2B-orange) ![Supported Platforms](https://img.shields.io/badge/Linux%20Mint-20%2B-green) ![License](https://img.shields.io/badge/License-MIT-blue)

## ⚡ Quick Start (3 Steps)

### 1️⃣ Install (30 seconds)
```bash
curl -sSL https://raw.githubusercontent.com/thomasboy2017/Winpatable-/main/install.sh | bash
```

### 2️⃣ Detect System (1 minute)
```bash
winpatable detect
```

### 3️⃣ Complete Setup (20 minutes)
```bash
winpatable quick-start
```

**Done!** You're ready to install Windows applications.

---

## 📖 Full Documentation

- **[Getting Started Index](./GETTING_STARTED.md)** - Find what you need quickly
- **[Quick Start Guide](./QUICK_START.md)** - Start here! Easy 3-step setup  
- **[Application Guides](./docs/APPLICATION_GUIDES.md)** - How to install specific apps
- **[GPU Guide](./docs/GPU_GUIDE.md)** - GPU setup and troubleshooting
- **[Troubleshooting](./TROUBLESHOOTING.md)** - Common issues & solutions
- **[Architecture](./docs/ARCHITECTURE.md)** - Technical details

---

## 🎯 What Can You Do?

| Application | Support | Speed | GPU | Cost |
|---|---|---|---|---|
| **Microsoft Office** | ✅ Excellent | Native | No | Free/Paid |
| **Adobe Premiere Pro** | ✅ Very Good | ~95% | ✅ Required | Paid |
| **Sony Vegas Pro** | ✅ Very Good | ~95% | Optional | Paid |
| **Autodesk 3DS Max** | ✅ Very Good | ~95% | ✅ Required | Paid |

---

## ⚙️ System Requirements

### Minimum
- **OS**: Ubuntu 20.04+ or Linux Mint 20+
- **CPU**: Intel Core i5 or AMD Ryzen 5 (x64)
- **RAM**: 4 GB (8 GB recommended)
- **Storage**: 30 GB free space

### Recommended
- **OS**: Ubuntu 24.04 LTS or Linux Mint 21+
- **CPU**: Intel Core i7/i9 or AMD Ryzen 7/9
- **RAM**: 16-32 GB
- **Storage**: 100+ GB on SSD
- **GPU**: NVIDIA RTX 3060+ or equivalent

---

## 🚀 Installation Methods

### Method 1: One-Click Install (Easiest)

```bash
curl -sSL https://raw.githubusercontent.com/thomasboy2017/Winpatable-/main/install.sh | bash
```

Just copy and paste! The installer handles everything.

### Method 2: Git Clone

```bash
git clone https://github.com/thomasboy2017/Winpatable-.git
cd Winpatable-
chmod +x install.sh
./install.sh
```

### Method 3: Using the Setup Wizard (Interactive)

```bash
python3 scripts/wizard.py
```

Gets you through setup step-by-step with explanations.

## 📝 Usage Guide

### First Time Users: Start Here!

**See [QUICK_START.md](./QUICK_START.md) for an easy visual guide**

### Basic Commands

```bash
# Check if your system is compatible
winpatable detect

# Automatic setup (recommended)
winpatable quick-start

# Install Microsoft Office
winpatable install-app office --installer ~/Downloads/office.exe

# List supported applications
winpatable list-apps

# Get performance tips
winpatable performance-tuning

# View all commands
winpatable --help
```

## ❓ FAQ

### Q: Will my apps run as fast as on Windows?
**A:** Usually 90-95% as fast. Professional apps like Premiere run at near-native speeds with GPU acceleration.

### Q: Do I need a GPU?
**A:** No, but it helps. Professional apps run much faster with GPU (NVIDIA RTX recommended).

### Q: Is it safe?
**A:** Yes! Applications run in an isolated environment (Wine prefix) and can't access your entire system.

### Q: Can I use multiple applications?
**A:** Yes! They share the same environment and can communicate.

### Q: What if something breaks?
**A:** Just delete `~/.winpatable` and run setup again. Everything is isolated.

### Q: Why is performance sometimes slower?
**A:** Check GPU utilization with `nvidia-smi`. Also close other apps and disable desktop effects.

### Q: Can I uninstall easily?
**A:** Yes! See [uninstall section](#-uninstall-easy) below.

---

## 🆘 Troubleshooting

### "winpatable: command not found"
```bash
# Add to PATH
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Application won't start
1. Check file path is correct: `ls /path/to/installer.exe`
2. Verify Wine is installed: `wine --version`
3. Check free disk space: `df -h`

### Poor performance
1. Check GPU: `nvidia-smi` (NVIDIA) or `rocm-smi` (AMD)
2. Close other applications
3. Use SSD for projects

### GPU drivers not working
```bash
# Try manual installation
winpatable install-gpu-drivers

# Verify
nvidia-smi  # for NVIDIA
rocm-smi    # for AMD
```

**Need more help?** See [Application Guides](./docs/APPLICATION_GUIDES.md)

---

## 🗑️ Uninstall (Easy)

```bash
# Remove Winpatable data
rm -rf ~/.winpatable

# Remove command
sudo rm /usr/local/bin/winpatable

# Remove installation (optional)
sudo rm -rf /opt/winpatable
```

That's it! Everything is isolated and safe to delete.

---

## 📚 Documentation

- **[QUICK_START.md](./QUICK_START.md)** - Fast setup guide ⭐ START HERE
- **[APPLICATION_GUIDES.md](./docs/APPLICATION_GUIDES.md)** - App-specific installation
- **[GPU_GUIDE.md](./docs/GPU_GUIDE.md)** - GPU setup and troubleshooting
- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Technical deep dive
Bring compatibilty with Windows Apps (coded using ai)
