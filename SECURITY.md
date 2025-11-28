# Winpatable Security Hardening Guide

## Overview

Winpatable v1.5.0+ includes comprehensive security measures to protect against malware, unauthorized code execution, and hacking attempts. This guide covers all security features and best practices.

## Security Features

### 1. Code Signing & Verification

**Purpose**: Ensure all code is legitimate and hasn't been tampered with

**Implementation**:
- HMAC-SHA256 signing for all code files
- Automatic signature verification on startup
- Key stored in `~/.winpatable/signing_key` (600 permissions)

**Usage**:
```python
from src.core.security import CodeSigner

signer = CodeSigner()
signature = signer.sign_file('/path/to/file')
verified = signer.verify_signature('/path/to/file', expected_signature)
```

### 2. Malware Detection

**Purpose**: Identify and quarantine malicious files

**Implementation**:
- ClamAV antivirus integration
- Real-time file scanning
- Directory-wide scanning support
- Quarantine reporting

**Installation**:
```bash
winpatable security install-clamav
sudo freshclam  # Update virus definitions
```

**Scanning**:
```bash
winpatable security scan ~/.winpatable
winpatable security scan /path/to/application
```

### 3. Security Sandbox

**Purpose**: Isolate untrusted code execution

**Features**:
- Restricted PATH environment
- Isolated HOME directory
- Removed dangerous env vars (PYTHONPATH, LD_PRELOAD)
- Timeout protection (default 30s)
- Working directory restriction

**Usage**:
```python
from src.core.security import SecuritySandbox

sandbox = SecuritySandbox("app_name")
returncode, stdout, stderr = sandbox.execute_with_restrictions(
    ["./untrusted_app"],
    timeout=30
)
```

### 4. Comprehensive Security Audit

**Purpose**: Verify system security posture

**Checks Performed**:
1. **File Permissions**: Ensure config directory is 700 (owner only)
2. **Code Signatures**: Verify main code integrity
3. **Malware Detection**: Check for known viruses
4. **Unsigned Code**: Verify all code is signed
5. **Dependency Integrity**: Check Python package compatibility

**Running Audit**:
```bash
winpatable security audit
```

**Report Format**:
```
SECURITY AUDIT REPORT

Results: 4/5 checks passed

🟠 HIGH
  ✓ Code Signature: Verified
  ✓ Unsigned Code Protection: Active
  
🟡 MEDIUM
  ⚠ ClamAV: Not installed (optional)
```

## Supported Distributions

### Debian-Based
- ✓ Ubuntu 22.04+ (Jammy, Kinetic, Lunar, Mantic)
- ✓ Linux Mint 21+ (Vanessa, Victoria, Virginia)
- ✓ Debian 12+ (Bookworm)
- ✓ Elementary OS 7+
- ✓ Pop!_OS 22.04+

**Package Manager**: APT
```bash
apt update
apt install wine64-stable winetricks
```

### Fedora-Based
- ✓ Fedora 38+ (latest)
- ✓ RHEL 9+ (if licensed)
- ✓ CentOS Stream 9+
- ✓ Rocky Linux 9+
- ✓ Alma Linux 9+

**Package Manager**: DNF
```bash
dnf update
dnf install wine winetricks
```

## Security Best Practices

### 1. File Permissions

Ensure secure permissions on configuration:
```bash
chmod 700 ~/.winpatable
chmod 600 ~/.winpatable/signing_key
chmod 600 ~/.winpatable/perf_cache.json
```

**Verify**:
```bash
winpatable security audit
```

### 2. Regular Updates

Keep Winpatable and Wine updated:
```bash
winpatable update --check-only  # Check for updates
winpatable update               # Install updates
sudo apt update && sudo apt upgrade  # System updates
```

### 3. Malware Scanning

Scan applications before installation:
```bash
# Scan downloads directory
winpatable security scan ~/Downloads

# Scan application directory
winpatable security scan ~/.winpatable
```

### 4. Dependency Management

Verify Python dependencies:
```bash
pip check
pip install --upgrade pip
winpatable security audit
```

### 5. Sandbox Execution

Run untrusted applications in sandbox:
```python
from src.core.security import SecuritySandbox

sandbox = SecuritySandbox("untrusted_app")
returncode, stdout, stderr = sandbox.execute_with_restrictions([
    "/path/to/untrusted/executable"
], timeout=60)

if returncode != 0:
    print(f"Execution failed: {stderr}")
```

## Threat Models

### Addressed Threats

1. **Malware in Downloaded Installers**
   - Mitigation: ClamAV scanning before installation
   - Status: Implemented ✓

2. **Code Tampering**
   - Mitigation: HMAC-SHA256 signatures
   - Status: Implemented ✓

3. **Privilege Escalation**
   - Mitigation: Restricted sandbox environment
   - Status: Implemented ✓

4. **Supply Chain Attacks**
   - Mitigation: Dependency integrity checking
   - Status: Implemented ✓

5. **Unsigned Code Execution**
   - Mitigation: Code signing verification
   - Status: Implemented ✓

### Known Limitations

1. **Kernel-Level Exploits**
   - Not prevented: Requires SELinux/AppArmor hardening
   - Mitigation: Use distribution security updates

2. **Side-Channel Attacks**
   - Not prevented: CPU/memory-based attacks
   - Mitigation: Use hardened kernel (grsecurity)

3. **Zero-Day Exploits**
   - Not prevented: Unknown vulnerabilities
   - Mitigation: Keep system updated

## CLI Security Commands

### Comprehensive Audit
```bash
winpatable security audit
```
Returns detailed report on 5 security checks with severity levels.

### File Scanning
```bash
winpatable security scan [path]
```
Scans specified path (or ~/.winpatable) for malware using ClamAV.

### Install Antivirus
```bash
winpatable security install-clamav
```
Installs ClamAV on Debian/Fedora systems.

## Configuration

### Security Config
Location: `~/.winpatable/`

**Files**:
- `signing_key` - HMAC key (mode 0o600)
- `perf_cache.json` - Performance cache (mode 0o600)
- `config.json` - Main configuration

**Required Permissions**:
```bash
chmod 700 ~/.winpatable
chmod 600 ~/.winpatable/*
```

### Environment Variables

**Safe Variables**:
- `WINPATABLE_PREFIX` - Custom Wine prefix
- `WINPATABLE_CACHE` - Cache directory

**Removed (Sandbox)**:
- `PYTHONPATH` - Path injection prevention
- `LD_LIBRARY_PATH` - Library injection prevention
- `LD_PRELOAD` - Preload injection prevention

## Security Roadmap (v1.5.0+)

### Implemented (v1.5.0)
- ✓ Code signing with HMAC-SHA256
- ✓ ClamAV integration
- ✓ Security sandbox
- ✓ Comprehensive audit
- ✓ Debian/Fedora support

### Planned (v1.6.0)
- [ ] Hardware-backed key storage (TPM)
- [ ] SELinux policy module
- [ ] AppArmor profile
- [ ] Encrypted home directory detection
- [ ] SSL/TLS certificate pinning

### Future (v1.7.0+)
- [ ] Full-disk encryption detection
- [ ] Integrity Measurement Architecture (IMA)
- [ ] Secure Boot verification
- [ ] Hardware attestation

## Reporting Security Issues

Found a security vulnerability? Please report responsibly:

1. **Do not** disclose publicly
2. Email: security@winpatable.example.com
3. Include: description, impact, proof-of-concept
4. Wait: 90 days for patch before disclosure

## References

- ClamAV: https://www.clamav.net/
- OWASP: https://owasp.org/
- Python Security: https://python.readthedocs.io/
- Linux Security: https://www.kernel.org/doc/html/latest/

## Support

- GitHub Issues: https://github.com/thomasboy2017/Winpatable-/issues
- Security Docs: See this file
- Community Help: Coming soon

---

**Last Updated**: November 28, 2025
**Version**: v1.5.0
**Status**: Production Ready
