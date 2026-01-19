# Contributing to Research Paper Organizer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/research-paper-organizer.git`
3. Create a virtual environment and install dependencies (see SETUP_GUIDE.md)
4. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and reasonably sized
- Comment complex logic

Example:
```python
def extract_metadata_from_pdf(self):
    """
    Extract metadata from PDF file.
    
    Attempts to read PDF metadata fields (title, author, year).
    Falls back to filename parsing if metadata is unavailable.
    """
    # Implementation...
```

## Testing

Before submitting changes:

1. Test with a small sample of papers first
2. Test both dry-run and execute modes for reorganization scripts
3. Verify Excel output format matches template
4. Test with both downloaded and non-downloaded Dropbox files

```bash
# Example test commands
python organize_papers.py test_papers/ -o test_output.xlsx
python reorganize_folders.py test_papers/ --by-year  # dry run first
```

## Adding New Features

### Adding New Reorganization Strategies

Add new methods to the `FolderReorganizer` class in `reorganize_folders.py`:

```python
def reorganize_by_your_strategy(self):
    """Your strategy description."""
    print("\nApplying your strategy...")
    
    for pdf in self.root_path.rglob('*.pdf'):
        # Your logic here
        target_folder = self.root_path / 'new_folder_name'
        self._plan_move(pdf, target_folder)
```

Then add command-line argument in `main()`:
```python
parser.add_argument('--your-strategy', action='store_true',
                   help='Description of your strategy')
```

### Adding New Metadata Fields

1. Add field to `PaperMetadata` class in `organize_papers.py`
2. Add extraction logic in appropriate methods
3. Update spreadsheet generation in `generate_spreadsheet()`
4. Update documentation in README.md

## Commit Guidelines

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add support for .docx file extraction"
git commit -m "Fix year extraction regex for European date formats"
git commit -m "Update README with new command examples"

# Less helpful
git commit -m "Fix bug"
git commit -m "Update"
git commit -m "Changes"
```

Format:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Keep first line under 50 characters
- Add detailed description after blank line if needed

## Submitting Changes

1. Make your changes in a feature branch
2. Test thoroughly
3. Update documentation (README.md, docstrings)
4. Commit with clear messages
5. Push to your fork
6. Open a Pull Request

### Pull Request Template

When opening a PR, please include:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing Done
Describe how you tested the changes

## Related Issues
Closes #issue_number (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## Feature Suggestions

Good candidates for contributions:

### High Priority
- Abstract extraction from PDFs
- DOI lookup and metadata enrichment
- Duplicate paper detection
- Better filename parsing patterns
- Support for more document formats (.docx, .txt)

### Medium Priority
- Citation network visualization
- Integration with Zotero/Mendeley
- Web interface using Flask/Streamlit
- Batch renaming based on metadata
- Export to BibTeX format

### Nice to Have
- Machine learning for topic classification
- Full-text search across papers
- Automatic keyword extraction
- PDF annotation extraction
- Integration with academic databases (arXiv, Google Scholar)

## Documentation

When adding features, update:

1. **README.md** - User-facing documentation
2. **Docstrings** - Inline code documentation
3. **SETUP_GUIDE.md** - If changing setup process
4. **Code comments** - For complex logic

## Bug Reports

When reporting bugs, include:

1. Python version and OS
2. Installed package versions (`pip freeze`)
3. Command you ran
4. Expected behavior
5. Actual behavior
6. Error messages (full traceback)
7. Sample data if possible (anonymized)

## Questions?

- Open an issue for questions
- Check existing issues and documentation first
- Be respectful and constructive

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment
- Respect different viewpoints and experiences

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make research paper organization easier for everyone! 🎓
