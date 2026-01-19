# Quick Start: Setting Up Your Research Paper Organizer

This is a streamlined guide to get you up and running quickly.

## Step 1: Download and Extract Files

Download all the files to a folder, for example:
```bash
~/Projects/research-paper-organizer/
```

## Step 2: Run the Quick Setup Script

```bash
cd ~/Projects/research-paper-organizer
bash quick_setup.sh
```

This will:
- Create a Python virtual environment (`venv/`)
- Install all dependencies (PyPDF2, openpyxl)
- Initialize a git repository
- Test that everything works

## Step 3: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to https://github.com/new
2. Repository name: `research-paper-organizer`
3. Description: "Tools for organizing research papers and generating literature review spreadsheets"
4. Choose Public or Private
5. **Don't** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"
7. Follow the commands shown under "push an existing repository from the command line":

```bash
git remote add origin https://github.com/YOUR_USERNAME/research-paper-organizer.git
git branch -M main
git push -u origin main
```

### Option B: Using GitHub CLI (if you have it)

```bash
gh repo create research-paper-organizer --public --source=. --remote=origin
git push -u origin main
```

## Step 4: Customize for Your Research

Edit `keyword_map_example.json` to match your research areas. I've pre-populated it with:
- Quantum Mechanics
- Quantum Optics
- Levitated Optomechanics
- NV Diamond Magnetometry
- Neutrino Physics (RENP)
- Statistical Mechanics
- Precision Measurements
- Vacuum Technology

Add or modify categories as needed.

## Step 5: First Run

Test with your papers:

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Scan papers and generate spreadsheet
python organize_papers.py ~/Dropbox/Research_Papers

# This creates: literature_review_YYYYMMDD.xlsx
```

## Step 6: Reorganize Folders (Optional)

Preview reorganization first (dry run):
```bash
# Preview organizing by year
python reorganize_folders.py ~/Dropbox/Research_Papers --by-year

# Preview organizing by topic
python reorganize_folders.py ~/Dropbox/Research_Papers --by-keywords keyword_map_example.json

# Preview consolidating small folders
python reorganize_folders.py ~/Dropbox/Research_Papers --consolidate
```

If you like the preview, add `--execute`:
```bash
python reorganize_folders.py ~/Dropbox/Research_Papers --by-year --execute
```

## Daily Usage

```bash
# Start working
cd ~/Projects/research-paper-organizer
source venv/bin/activate

# Use the tools
python organize_papers.py ~/Dropbox/Papers

# When done
deactivate
```

## File Overview

```
research-paper-organizer/
├── organize_papers.py         ← Main script: scan papers, generate Excel
├── reorganize_folders.py      ← Reorganize folder structure
├── keyword_map_example.json   ← Customize your topics here
├── README.md                  ← Full documentation
├── SETUP_GUIDE.md            ← Detailed setup instructions
├── GETTING_STARTED.md        ← This file
├── requirements.txt          ← Python dependencies
├── setup.py                  ← Package installation config
├── LICENSE                   ← MIT License
├── .gitignore               ← Git ignore rules
├── quick_setup.sh           ← Automated setup script
└── CONTRIBUTING.md          ← Guidelines for contributions

After setup:
├── venv/                    ← Virtual environment (not in git)
└── literature_review_*.xlsx ← Generated spreadsheets (not in git)
```

## Common Commands Reference

```bash
# Activate venv (do this first each session)
source venv/bin/activate

# Generate spreadsheet
python organize_papers.py /path/to/papers
python organize_papers.py /path/to/papers -o custom_name.xlsx

# Preview reorganization (safe, no changes made)
python reorganize_folders.py /path/to/papers --by-year
python reorganize_folders.py /path/to/papers --by-keywords keyword_map_example.json

# Actually reorganize (after previewing)
python reorganize_folders.py /path/to/papers --by-year --execute

# Commit changes to git
git add .
git commit -m "Your commit message"
git push

# Update Python packages
pip install --upgrade -r requirements.txt

# Deactivate venv when done
deactivate
```

## Tips

1. **Always test with a small folder first** before running on your entire collection
2. **Use dry-run mode** for reorganization to preview changes
3. **Back up your papers** before reorganizing (or rely on Dropbox version history)
4. **Download Dropbox files** before scanning for best metadata extraction
5. **Run the scan multiple times** as you download more papers from Dropbox
6. **Commit to git regularly** to track changes to your scripts

## Troubleshooting

### "command not found: python3"
Use `python` instead of `python3`:
```bash
python -m venv venv
```

### "venv/bin/activate: No such file"
On Windows, use:
```bash
venv\Scripts\activate
```

### "Permission denied" when running scripts
Make them executable:
```bash
chmod +x organize_papers.py reorganize_folders.py quick_setup.sh
```

### Scripts don't find PyPDF2 or openpyxl
Make sure virtual environment is activated (should see `(venv)` in prompt):
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### No papers found
Check that you're pointing to the right directory:
```bash
ls ~/Dropbox/Research_Papers/*.pdf  # Should list PDF files
```

## Next Steps

Once comfortable with the basics:

1. Read the full README.md for advanced features
2. Customize keyword_map_example.json for your specific research areas
3. Modify the Python scripts to add custom features
4. Set up pre-commit hooks for code quality (see CONTRIBUTING.md)
5. Share with colleagues or make it public!

## Getting Help

- Check README.md for detailed documentation
- Review SETUP_GUIDE.md for setup troubleshooting
- Look at the code comments in the Python files
- Open an issue on GitHub if you find bugs

---

**Have fun organizing your papers!** 📚🔬
