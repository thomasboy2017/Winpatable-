# Winpatable Quick Start Guide

**For the average user, follow these 3 simple steps:**

## Step 1: Install Winpatable (2 minutes)

### Option A: Automatic Installation (Recommended)

Copy and paste this in your terminal:

```bash
curl -sSL https://raw.githubusercontent.com/thomasboy2017/Winpatable-/main/install.sh | bash
```

That's it! The installer will:
- Download Winpatable
- Install dependencies
- Set up everything automatically

### Option B: Manual Installation

If you prefer manual installation:

```bash
# Clone the project
git clone https://github.com/thomasboy2017/Winpatable-.git
cd Winpatable-

# Run installer
chmod +x install.sh
./install.sh
```

## Step 2: Check Your System (1 minute)

After installation, check if your system is compatible:

```bash
winpatable detect
```

You'll see:
- ✓ Your OS version
- ✓ Your CPU (Intel/AMD)
- ✓ Your GPU (NVIDIA/AMD/Intel)
- ✓ Compatibility status

## Step 3: Complete Setup (10-30 minutes)

Run one command to set everything up:

```bash
winpatable quick-start
```

This will automatically:
1. ✓ Detect your system
2. ✓ Install GPU drivers (if you have a compatible GPU)
3. ✓ Configure Wine/Proton
4. ✓ Install Windows support libraries

**Just answer yes/no prompts and wait!**

---

## Install Your First Application (5 minutes)

Once setup is complete, install an application. For example, Microsoft Office:

```bash
winpatable install-app office --installer ~/Downloads/office_installer.exe
```

Replace `~/Downloads/office_installer.exe` with your actual installer path.

### Supported Applications

| App | Command | Notes |
|-----|---------|-------|
| Microsoft Office | `winpatable install-app office` | Easy to use |
| Adobe Premiere Pro | `winpatable install-app premiere` | Needs GPU |
| Sony Vegas Pro | `winpatable install-app vegas` | Good performance |
| Autodesk 3DS Max | `winpatable install-app 3dsmax` | Needs GPU |

---

## Frequently Asked Questions

### Q: Will my applications run as fast as on Windows?
**A:** Usually 90-95% as fast. Professional applications like Premiere Pro run at near-native speeds with GPU acceleration.

### Q: Do I need a powerful computer?
**A:** For light apps like Office/Photoshop: 4GB RAM is enough.
For professional apps like Premiere/Revit: 8-16GB RAM recommended.
Minimum CPU: Intel Core i3 (3rd Gen+) or AMD Ryzen 3.

### Q: What if something goes wrong?
**A:** Run:
```bash
winpatable detect
```

This will help diagnose the issue. Most problems are simple driver issues.

### Q: Can I run multiple applications?
**A:** Yes! They share the same Wine environment and can communicate with each other.

### Q: How much disk space do I need?
**A:** 
- Winpatable itself: 2GB
- Each application: 2-10GB depending on the app

### Q: Do I need a GPU?
**A:** No, but it helps. Professional apps are much faster with a GPU (NVIDIA recommended).

---

## Common Issues & Solutions

### "Command not found: winpatable"
```bash
# Try the full path
~/.local/bin/winpatable detect

# Or add to PATH
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### "GPU drivers not installing"
This is usually fine. You can still use integrated graphics.
```bash
# Force installation
winpatable install-gpu-drivers
```

### "Application won't start"
1. Make sure you have the correct installer (.exe file)
2. Check that you have enough disk space
3. Try installing Office first to verify setup works

### "Poor performance"
1. Check GPU with: `nvidia-smi` (for NVIDIA)
2. Close other applications
3. Make sure you're using SSD for projects

---

## Need More Help?

### View All Commands
```bash
winpatable --help
```

### See Supported Apps
```bash
winpatable list-apps
```

### Performance Tips
```bash
winpatable performance-tuning
```

### GPU-Specific Guide
See: `docs/GPU_GUIDE.md`

### Application-Specific Guides
See: `docs/APPLICATION_GUIDES.md`

---

## What Gets Installed?

When you run `winpatable quick-start`, these are automatically installed:

1. **Wine** - Windows compatibility layer
2. **Proton** - Enhanced Wine from Valve
3. **DXVK** - Better graphics support
4. **GPU Drivers** - For your specific GPU
5. **Windows Libraries** - Required DLLs

**Total size:** ~5-10GB depending on GPU drivers

---

## Uninstall

If you want to remove Winpatable:

```bash
# Remove the application
rm -rf ~/.winpatable

# Remove the command
sudo rm /usr/local/bin/winpatable

# Remove installation
sudo rm -rf /opt/winpatable
```

---

## Next Steps

1. **Install an application:** `winpatable install-app office --installer path/to/installer.exe`
2. **Launch the application:** Just run it like normal (or from application menu)
3. **Optimize performance:** `winpatable performance-tuning`

**That's it! Enjoy Windows apps on Linux!** 🎉

---

## Got Stuck?

1. Make sure you completed all steps
2. Check system compatibility: `winpatable detect`
3. Look for error messages in the output
4. Try running commands with `--help` flag

**Everything should "just work" on modern systems!**
