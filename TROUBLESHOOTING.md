# Common Issues & Solutions

Quick answers to the most common problems users encounter.

## Installation Issues

### "sudo password required multiple times"
The installer may ask for your password several times. This is normal - just enter it each time.

**Tip**: You can allow `sudo` to work without password for a session:
```bash
sudo -v  # Enter password once, valid for 15 minutes
```

---

### "Insufficient disk space"
Winpatable needs ~30GB total:
- Installation: 5GB
- Wine environment: 5GB
- Applications: 10-50GB

**Solution**:
```bash
# Check available space
df -h

# Free up space on your drive
rm -rf ~/Downloads/*.iso  # Remove old ISO files
```

---

### "Internet connection issues"
If installation fails during download:

```bash
# Try again (it will resume)
./install.sh

# Or manually install components
winpatable setup-wine
```

---

## After Installation

### "winpatable command not found"

**Solution 1** - Check PATH:
```bash
# See if command is installed
ls /usr/local/bin/winpatable

# Add to PATH if needed
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Solution 2** - Use full path:
```bash
/usr/local/bin/winpatable detect
```

---

### "System detection shows "unknown" GPU"

This usually means your GPU drivers aren't installed yet.

```bash
# Install GPU drivers
winpatable install-gpu-drivers

# Verify installation worked
nvidia-smi     # for NVIDIA
rocm-smi       # for AMD
glxinfo        # for Intel
```

---

## Application Installation Issues

### "Installer won't run"

**Check 1** - File exists:
```bash
# Verify installer path
ls ~/Downloads/office_installer.exe
```

**Check 2** - Use correct path:
```bash
# Make sure path has no spaces in quotes
winpatable install-app office --installer ~/Downloads/office_installer.exe
```

**Check 3** - Wine is working:
```bash
wine --version  # Should show Wine version
```

---

### "Missing DLLs error"

When an app complains about missing DLLs:

```bash
# Reinstall Wine dependencies
winpatable setup-wine

# Or specific DLLs
WINEPREFIX=~/.winpatable winetricks dotnet48
```

---

### "Application crashes on startup"

**Step 1** - Check logs:
```bash
WINEDEBUG=+all wine "C:\Program Files\App\app.exe" 2>&1 | head -50
```

**Step 2** - Try compatibility mode:
```bash
# In Wine registry
WINEPREFIX=~/.winpatable wine regedit
# Navigate to: HKEY_CURRENT_USER\Software\Wine\AppDefaults\app.exe
# Add: Version = Windows 10
```

**Step 3** - Disable features:
```bash
export STAGING_SHARED_MEMORY=0
export DXVK_HUD=off
```

---

## Performance Issues

### "Application is slow"

**Quick Fix**:
1. Close other applications
2. Disable desktop effects
3. Use SSD instead of HDD

**Check GPU Usage**:
```bash
# NVIDIA - watch GPU load
nvidia-smi dmon

# AMD - watch GPU utilization
watch -n 1 rocm-smi --showuse
```

---

### "Graphics/rendering glitches"

Try different video renderers:

```bash
# Use OpenGL (sometimes more stable)
export PROTON_USE_WINED3D=1

# Or DXVK (usually faster)
export PROTON_USE_WINED3D=0

# Then launch app
wine app.exe
```

---

### "Audio not working"

Check ALSA (sound system):

```bash
# Test audio
aplay /usr/share/sounds/freedesktop/stereo/complete.oga

# In Wine, set audio driver
WINEPREFIX=~/.winpatable wine control.exe
# Multimedia > Audio tab > select correct driver
```

---

## GPU-Specific Issues

### NVIDIA: "CUDA not detected"

```bash
# Check CUDA installation
nvidia-smi

# Should show CUDA capability version

# If not, reinstall CUDA
sudo apt install cuda-toolkit-12-3
```

### AMD: "GPU not detected by application"

```bash
# Check AMD drivers
rocm-smi

# Verify HIP support
hipconfig -full
```

### Intel: "Integrated graphics not working"

```bash
# Check i915 driver
lsmod | grep i915

# Install Intel GPU tools
sudo apt install intel-gpu-tools
```

---

## Data & Backups

### "How do I backup my application data?"

Application data is stored in Wine prefix:

```bash
# Backup entire environment
cp -r ~/.winpatable ~/.winpatable.backup

# Or just application folder
cp -r ~/.winpatable/drive_c/Users ~/backup_users
```

---

### "Can I move Wine prefix to another drive?"

Yes! But it's complex. Better to use symbolic link:

```bash
# Backup current
cp -r ~/.winpatable ~/backup

# Create new location
mkdir /mnt/large-drive/winpatable

# Move data
mv ~/.winpatable/* /mnt/large-drive/winpatable/

# Create symlink
ln -s /mnt/large-drive/winpatable ~/.winpatable
```

---

## Advanced Troubleshooting

### Enable Debug Output

```bash
# Show Wine debug info
export WINE DEBUG=+all

# Show DXVK info
export DXVK_HUD=memory

# Show Proton info
export PROTON_LOG=1

# Run app
wine app.exe
```

### Clean Wine Prefix

**Warning**: This deletes all installed applications

```bash
# Backup first!
cp -r ~/.winpatable ~/.winpatable.backup

# Remove and recreate
rm -rf ~/.winpatable/drive_c
wineboot --init
```

---

## Getting Professional Help

If you're still stuck:

1. **Generate debug info**:
   ```bash
   winpatable detect > ~/winpatable_debug.txt
   ```

2. **Check Wine AppDB**: https://appdb.winehq.org/

3. **Report issue** on GitHub with:
   - Output from `winpatable detect`
   - Error messages
   - Which application
   - What you're trying to do

---

## Quick Command Reference

```bash
# System
winpatable detect                    # Check system
winpatable list-apps                 # See apps

# Setup
winpatable quick-start               # Full setup
winpatable setup-wine               # Just Wine setup
winpatable install-gpu-drivers      # Just GPU setup

# Applications
winpatable install-app office --installer path/to/file.exe

# Information
winpatable performance-tuning        # Tips
winpatable --help                   # All commands
```

---

## Still Having Issues?

**Remember**: Winpatable is stable for the supported applications (Office, Premiere Pro, Vegas, 3DS Max).

For other applications:
1. Check Wine AppDB for compatibility
2. See if there's a Proton config
3. Try older app versions (sometimes more compatible)
4. Ask in Wine/Proton communities

**Most issues are GPU driver related** - make sure your drivers are up to date!

---

**Need more help?** See the full [APPLICATION_GUIDES.md](./docs/APPLICATION_GUIDES.md) or open an issue on GitHub.
