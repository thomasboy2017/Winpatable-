# Winpatable - Getting Started Index

Welcome to Winpatable! 🎉 Here's where to go based on what you want to do.

## 🚀 I Just Installed - What Now?

**[👉 Start Here: QUICK_START.md](./QUICK_START.md)**

This is the fastest way to get Winpatable working. Just 3 steps!

---

## 🎯 I Want To...

### Install Microsoft Office
👉 See [APPLICATION_GUIDES.md - Microsoft Office section](./docs/APPLICATION_GUIDES.md#microsoft-office)

### Install Adobe Premiere Pro
👉 See [APPLICATION_GUIDES.md - Adobe Premiere section](./docs/APPLICATION_GUIDES.md#adobe-premiere-pro)

### Install Sony Vegas Pro
👉 See [APPLICATION_GUIDES.md - Sony Vegas section](./docs/APPLICATION_GUIDES.md#sony-vegas-pro)

### Install Autodesk 3DS Max
👉 See [APPLICATION_GUIDES.md - 3DS Max section](./docs/APPLICATION_GUIDES.md#autodesk-3ds-max)

### Set Up My GPU (NVIDIA/AMD/Intel)
👉 See [GPU_GUIDE.md](./docs/GPU_GUIDE.md)

### Improve Performance
👉 Run: `winpatable performance-tuning`

### Fix an Issue
👉 See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

### Understand How It Works
👉 See [ARCHITECTURE.md](./docs/ARCHITECTURE.md)

---

## 📚 Documentation Files

| File | Purpose | For Whom |
|------|---------|----------|
| [QUICK_START.md](./QUICK_START.md) | Fast setup guide | Everyone - start here! |
| [README.md](./README.md) | Overview & features | People wanting to learn more |
| [APPLICATION_GUIDES.md](./docs/APPLICATION_GUIDES.md) | How to install each app | App-specific setup |
| [GPU_GUIDE.md](./docs/GPU_GUIDE.md) | GPU configuration | GPU setup & troubleshooting |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Fix common issues | Troubleshooting help |
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Technical details | Developers & advanced users |

---

## ⌨️ Command Cheat Sheet

```bash
# First time setup
winpatable quick-start           # Full automatic setup
python3 scripts/wizard.py        # Interactive setup wizard

# Check your system
winpatable detect               # See what you have

# Install applications
winpatable list-apps            # See what's supported
winpatable install-app office --installer ~/Downloads/office.exe

# Get help
winpatable --help               # View all commands
winpatable performance-tuning   # Get optimization tips
```

---

## 🎮 Workflow Example

Here's a typical workflow from start to finish:

```bash
# 1. Install (30 sec)
curl -sSL https://raw.githubusercontent.com/thomasboy2017/Winpatable-/main/install.sh | bash

# 2. Check system (1 min)
winpatable detect

# 3. Complete setup (20 min)
winpatable quick-start

# 4. Install an app (5 min)
winpatable install-app office --installer ~/Downloads/office.exe

# 5. Use the app!
# Find it in your application menu or launch directly
```

Done! 🎉

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] `winpatable --version` shows version
- [ ] `winpatable detect` shows your system info
- [ ] GPU drivers installed (if you have a GPU)
- [ ] Wine environment set up at `~/.winpatable`
- [ ] At least one application installed

If all checked, you're ready to go!

---

## 🆘 Quick Troubleshooting

**Problem: "winpatable: command not found"**
```bash
source ~/.bashrc
# or use: /usr/local/bin/winpatable
```

**Problem: "GPU not detected"**
```bash
# Install GPU drivers
winpatable install-gpu-drivers
```

**Problem: "Application won't start"**
```bash
# Verify Wine works
wine --version
```

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for more help.

---

## 🤔 Common Questions

**Q: Is it really that easy?**
A: Yes! The whole setup is automated. Just follow QUICK_START.md.

**Q: Will my apps work?**
A: Microsoft Office, Premiere Pro, Vegas, and 3DS Max work great. Other apps may work too.

**Q: Is it safe?**
A: Yes! Apps run in an isolated environment. Very safe.

**Q: How fast will apps run?**
A: Usually 90-95% as fast as Windows. Professional apps run at near-native speeds.

**Q: Can I uninstall easily?**
A: Yes! Just delete `~/.winpatable` and you're done.

See [QUICK_START.md - FAQ](./QUICK_START.md#frequently-asked-questions) for more.

---

## 🎓 Learning Path

**Beginner**: 
1. Read [QUICK_START.md](./QUICK_START.md)
2. Run installation
3. Install an application

**Intermediate**:
1. Read [APPLICATION_GUIDES.md](./docs/APPLICATION_GUIDES.md)
2. Read [GPU_GUIDE.md](./docs/GPU_GUIDE.md)
3. Optimize performance

**Advanced**:
1. Read [ARCHITECTURE.md](./docs/ARCHITECTURE.md)
2. Explore source code
3. Contribute improvements

---

## 📞 Need Help?

1. **Quick answers**: Check [QUICK_START.md](./QUICK_START.md)
2. **App-specific help**: Check [APPLICATION_GUIDES.md](./docs/APPLICATION_GUIDES.md)
3. **Troubleshooting**: Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
4. **Technical questions**: Check [ARCHITECTURE.md](./docs/ARCHITECTURE.md)
5. **Still stuck?** Open an issue on GitHub

---

## 🚀 You're Ready!

Choose what to do:

- **[👉 QUICK_START.md](./QUICK_START.md)** - Fast setup
- **[👉 README.md](./README.md)** - Learn more
- **[👉 Run winpatable quick-start](./README.md#-usage-guide)** - Start setup

**Let's get those Windows apps running!** 🎉

---

Made with ❤️ for Linux users who need Windows applications
