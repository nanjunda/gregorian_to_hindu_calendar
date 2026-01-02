# Walkthrough: Hindu Panchanga v3.2

This version includes **Rashi/Lagna** calculations, **HTTPS security**, and **Privacy features**.

## New Features
1.  **Rashi (Moon Sign)**: Calculated based on Sidereal Moon Longitude.
2.  **Lagna (Ascendant)**: Calculated based on Horizon/Ecliptic intersection.
3.  **HTTPS**: Auto-generated Self-Signed SSL (Port 443).
4.  **Privacy**: No-logging policy note added.
5.  **Ops**: Hourly log rotation enabled.

## Installation & Upgrade
Run these commands on your Oracle Linux 9 VM:

```bash
# 1. Fetch latest code (v3.2)
git checkout main
git pull origin main

# 2. Run Deployment Script
# This will:
# - Install system python/dependencies
# - Generate SSL certificates
# - Configure Nginx for HTTPS
# - Setup Log Rotation
chmod +x deploy.sh
./deploy.sh
```

## Verification
1.  **Access**: Open `https://<YOUR_VM_IP>` (Accept the security warning).
2.  **Check Results**: Look for "Rashi" and "Lagna" rows in the calculation result.
3.  **Check Footer**: Confirm the "Privacy Note" is visible.
4.  **Check Logs**: Verify `/etc/logrotate.d/panchanga` exists.
