#!/bin/bash

# Quick setup script for research-paper-organizer repository
# This script creates venv, installs dependencies, and initializes git

set -e  # Exit on error

echo "=========================================="
echo "Research Paper Organizer - Quick Setup"
echo "=========================================="
echo

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 not found"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
echo
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  venv directory already exists"
    read -p "Delete and recreate? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Virtual environment recreated"
    else
        echo "Using existing venv"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"

# Install dependencies
echo
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"

# List installed packages
echo
echo "Installed packages:"
pip list | grep -E "PyPDF2|openpyxl"

# Initialize git if not already initialized
echo
if [ -d ".git" ]; then
    echo "✅ Git repository already initialized"
else
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Research paper organization tools"
    echo "✅ Git repository initialized"
fi

# Test scripts
echo
echo "Testing scripts..."
if python organize_papers.py --help >/dev/null 2>&1; then
    echo "✅ organize_papers.py working"
else
    echo "❌ organize_papers.py has errors"
fi

if python reorganize_folders.py --help >/dev/null 2>&1; then
    echo "✅ reorganize_folders.py working"
else
    echo "❌ reorganize_folders.py has errors"
fi

# Final instructions
echo
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo
echo "Virtual environment is currently activated."
echo "The prompt should show: (venv)"
echo
echo "Next steps:"
echo
echo "1. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Create repo named 'research-paper-organizer'"
echo "   - Then run:"
echo "     git remote add origin https://github.com/yourusername/research-paper-organizer.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo
echo "2. OR use GitHub CLI (if installed):"
echo "     gh repo create research-paper-organizer --public --source=. --remote=origin"
echo "     git push -u origin main"
echo
echo "3. Test the scripts:"
echo "     python organize_papers.py ~/path/to/papers"
echo
echo "To deactivate virtual environment later:"
echo "     deactivate"
echo
echo "To reactivate in future sessions:"
echo "     source venv/bin/activate"
echo
