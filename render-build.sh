#!/usr/bin/env bash
# exit on error
set -o errexit

# Install FFmpeg
apt-get -y update
apt-get -y install ffmpeg

# Install Python dependencies
pip install -r requirements.txt