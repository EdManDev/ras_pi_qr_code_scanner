#!/bin/bash
# Installation script for QR Scanner dependencies
# For Raspberry Pi 4B running Ubuntu 22.04.5 LTS ARM

echo "===== QR Scanner Installation Script ====="
echo "This script will install all necessary dependencies for the QR code scanner."

# Exit on error
set -e

echo -e "\n[1/5] Updating system packages..."
sudo apt update
sudo apt upgrade -y

echo -e "\n[2/5] Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-opencv \
    v4l-utils \
    libopencv-dev \
    libzbar0 \
    libzbar-dev

echo -e "\n[3/5] Installing Python packages..."
pip3 install opencv-python
pip3 install pyzbar
pip3 install numpy

echo -e "\n[4/5] Setting up camera permissions..."
echo "Adding current user to video group..."
sudo usermod -a -G video $USER
echo "NOTE: You may need to log out and back in for permission changes to take effect."

echo -e "\n[5/5] Verifying camera setup..."
echo "Available video devices:"
ls -la /dev/video* 2>/dev/null || echo "No video devices found!"

echo -e "\nChecking camera details:"
v4l2-ctl --list-devices 2>/dev/null || echo "Could not get camera details. Make sure v4l-utils is installed."

echo -e "\n===== Installation Complete ====="
echo "To run the QR scanner with display:"
echo "python3 qr_scanner.py --show"
echo ""
echo "For troubleshooting:"
echo "python3 qr_scanner.py --debug --show --save-frame debug.jpg"
echo ""
echo "NOTE: If you encounter permission issues, log out and log back in, or reboot the system."
