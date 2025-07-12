#!/bin/bash

# Move into your project directory
cd ~/greatness_portfolio

# Fetch the latest changes from GitHub and reset local files to match main branch
git fetch && git reset origin/main --hard

# Activate your virtual environment
source python3-virtualenv/bin/activate

# Install any new Python dependencies
pip install -r requirements.txt

# Restart your systemd service to apply new changes
sudo systemctl restart myportfolio.service

# Optionally, print status
sudo systemctl status myportfolio.service --no-pager