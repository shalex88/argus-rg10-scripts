#!/bin/bash

ISP_DIR="/var/nvidia/nvcam/settings"

# Copy the camera overrides file to the ISP directory
sudo cp camera_overrides.isp "$ISP_DIR"/camera_overrides.isp
sudo chown root:root "$ISP_DIR"/camera_overrides.isp

# Reset the ISP settings
cd "$ISP_DIR"
sudo rm -rf nvcam_* serial_*
sudo systemctl restart nvargus-daemon