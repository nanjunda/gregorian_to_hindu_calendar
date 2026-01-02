#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Hindu Panchanga v3.0 SIMPLIFIED Deployment..."
echo "ℹ️  Mode: Gunicorn Only (No Nginx)"

APP_NAME="panchanga"
APP_PATH=$(pwd)
CURRENT_USER=$(whoami)

# Detect Package Manager
if command -v dnf &> /dev/null; then
    PKG_MGR="dnf"
    # Group for Gunicorn? stick to user for simplified execution
    HTTP_GROUP=$CURRENT_USER 
elif command -v apt-get &> /dev/null; then
    PKG_MGR="apt-get"
    HTTP_GROUP=$CURRENT_USER
else
    echo "❌ Unsupported package manager. Please install manually."
    exit 1
fi

echo "📦 Detected package manager: $PKG_MGR"

# 1. Install dependencies (Python Only)
echo "📦 Installing system dependencies..."
if [ "$PKG_MGR" == "dnf" ]; then
    sudo dnf install -y python3-pip git-core curl
    
    # Disable Nginx if present to free up ports/confusion
    if systemctl is-active --quiet nginx; then
        echo "🛑 Stopping Nginx to avoid conflicts..."
        sudo systemctl stop nginx
        sudo systemctl disable nginx
    fi

    # Open firewall for Oracle Linux
    if command -v firewall-cmd &> /dev/null; then
        echo "🔥 Opening firewall port 5080..."
        sudo firewall-cmd --permanent --add-port=5080/tcp
        sudo firewall-cmd --reload
    fi
else
    sudo apt-get update -y
    sudo apt-get install -y python3-pip python3-venv git curl
    # Disable Nginx on Debian too if simplifying
    sudo systemctl stop nginx || true
    sudo systemctl disable nginx || true
fi

# 2. Setup Virtual Environment
if [ ! -d "venv" ]; then
    echo "🏗️ Creating virtual environment..."
    python3 -m venv venv
fi

echo "🐍 Installing Python packages..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 3. Configure systemd service
echo "⚙️ Configuring systemd service..."
# Note: Using CURRENT_USER for Group as well to avoid permission issues
sed -e "s|{{USER}}|$CURRENT_USER|g" \
    -e "s|{{GROUP}}|$CURRENT_USER|g" \
    -e "s|{{APP_PATH}}|$APP_PATH|g" \
    panchanga.service.template | sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null

sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl restart $APP_NAME

# 4. Verification Check
echo "⏳ Waiting for service to start..."
sleep 3
if systemctl is-active --quiet $APP_NAME; then
    echo "✅ Service is RUNNING."
else
    echo "❌ Service failed to start. Check logs: journalctl -u $APP_NAME"
fi

PUBLIC_IP=$(curl -s ifconfig.me || echo "localhost")
echo "🎉 Deployment complete!"
echo "App accessible directly at: http://$PUBLIC_IP:5080"
