# Repository Setup Guide

Step-by-step guide to set up this project as a GitHub repository with a virtual environment.

## Initial Setup

### 1. Create Virtual Environment

```bash
# Navigate to your project directory
cd /path/to/research-paper-organizer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install package in development mode (optional, for testing)
pip install -e .
```

### 2. Initialize Git Repository

```bash
# Initialize git repo (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Research paper organization tools"
```

### 3. Create GitHub Repository

**Option A: Using GitHub CLI (if installed)**
```bash
# Create repo and push
gh repo create research-paper-organizer --public --source=. --remote=origin
git push -u origin main
```

**Option B: Manual setup**

1. Go to https://github.com/new
2. Create a new repository named `research-paper-organizer`
3. Don't initialize with README (we already have one)
4. Copy the remote URL
5. Run these commands:

```bash
# Add remote
git remote add origin https://github.com/yourusername/research-paper-organizer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Verify Setup

```bash
# Check that venv is activated (should see (venv) in prompt)
which python

# Verify packages installed
pip list | grep -E "PyPDF2|openpyxl"

# Test scripts
python organize_papers.py --help
python reorganize_folders.py --help
```

## Daily Workflow

### Starting work:
```bash
cd /path/to/research-paper-organizer
source venv/bin/activate
```

### Making changes:
```bash
# Edit files
# Test changes
python organize_papers.py /path/to/test/papers

# Commit changes
git add .
git commit -m "Description of changes"
git push
```

### Ending work session:
```bash
deactivate  # Deactivate virtual environment
```

## Project Structure

```
research-paper-organizer/
├── venv/                          # Virtual environment (not in git)
├── organize_papers.py             # Main scanning script
├── reorganize_folders.py          # Folder reorganization script
├── keyword_map_example.json       # Example keyword mapping
├── README.md                      # Main documentation
├── SETUP_GUIDE.md                 # This file
├── LICENSE                        # MIT License
├── setup.py                       # Package setup file
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── setup.sh                       # Automated setup script

Generated files (not in git):
├── literature_review_*.xlsx       # Generated spreadsheets
└── *.log                          # Log files
```

## Advanced: Development Installation

If you want to modify the code and have changes immediately available:

```bash
# Install in editable mode
pip install -e .

# Now you can use commands from anywhere:
organize-papers ~/Dropbox/Papers
reorganize-folders ~/Dropbox/Papers --by-year
```

## Updating Dependencies

```bash
# Activate venv
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Freeze current versions (optional)
pip freeze > requirements-lock.txt
```

## Sharing with Collaborators

Send them these instructions:

```bash
# Clone the repository
git clone https://github.com/yourusername/research-paper-organizer.git
cd research-paper-organizer

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Ready to use!
python organize_papers.py --help
```

## Troubleshooting

### Virtual environment not activating
- Make sure you're using the correct command for your OS
- Try: `python3 -m venv venv --clear` to recreate

### Import errors even with venv activated
```bash
# Verify venv is active
which python  # Should point to venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

### Git push rejected
```bash
# Pull first if working with others
git pull --rebase origin main
git push
```

### Package installation fails
```bash
# Make sure pip is updated
pip install --upgrade pip

# Try installing packages individually
pip install PyPDF2
pip install openpyxl
```

## Optional: Pre-commit Hooks

To automatically check code before committing:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
# (See example below)

# Install hooks
pre-commit install
```

Example `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]
```

## Notes

- Always activate the virtual environment before working on the project
- Don't commit the `venv/` directory (it's in `.gitignore`)
- Keep `requirements.txt` updated when adding new dependencies
- Test changes with a small sample of papers before running on full collection
- Consider creating a `dev` branch for experimental features

## Getting Help

- Check README.md for usage instructions
- Review script comments for implementation details
- Open an issue on GitHub if you find bugs
- Submit pull requests for improvements!
