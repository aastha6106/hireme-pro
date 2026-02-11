#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Try to install wkhtmltopdf
apt-get update -y 2>/dev/null && apt-get install -y wkhtmltopdf 2>/dev/null || echo "wkhtmltopdf: system install not available, skipping"