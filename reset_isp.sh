#!/bin/bash

cd /var/nvidia/nvcam/settings/
sudo rm -rf nvcam_* serial_*

sudo systemctl restart nvargus-daemon