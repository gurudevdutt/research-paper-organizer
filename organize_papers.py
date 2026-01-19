#!/usr/bin/env python3
"""
Research Paper Organization Tool
---------------------------------
Scans a folder of research papers (PDFs), extracts metadata, and generates
a literature review spreadsheet following a specific template format.

Handles Dropbox files that may not be fully downloaded locally.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import re

# PDF metadata extraction
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: PyPDF2 not installed. Install with: pip install PyPDF2")

# Excel writing
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False
    print("Warning: openpyxl not installed. Install with: pip install openpyxl")


class PaperMetadata:
    """Store metadata extracted from a research paper."""
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.filename = self.filepath.name
        self.folder = self.filepath.parent.name
        self.relative_path = None
        
        # Metadata fields
        self.title = None
        self.author = None
        self.year = None
        self.concept = None  # Will be derived from folder structure
        self.journal = None
        self.url = None
        
        # Status
        self.is_downloaded = self.check_if_downloaded()
        self.file_size = self.get_file_size()
        
    def check_if_downloaded(self):
        """Check if Dropbox file is actually downloaded."""
        if not self.filepath.exists():
            return False
        
        # Dropbox placeholder files are typically very small
        # and may have specific attributes
        try:
            size = self.filepath.stat().st_size
            # If file is less than 1KB, it might be a placeholder
            if size < 1024:
                return False
            return True
        except:
            return False
    
    def get_file_size(self):
        """Get file size in MB."""
        try:
            size_bytes = self.filepath.stat().st_size
            return size_bytes / (1024 * 1024)
        except:
            return 0
    
    def extract_metadata_from_pdf(self):
        """Extract metadata from PDF file."""
        if not PDF_SUPPORT or not self.is_downloaded:
            return
        
        try:
            with open(self.filepath, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                
                # Get PDF metadata
                if pdf.metadata:
                    self.title = pdf.metadata.get('/Title', None)
                    self.author = pdf.metadata.get('/Author', None)
                    
                    # Try to extract year from creation date
                    creation_date = pdf.metadata.get('/CreationDate', '')
                    year_match = re.search(r'(\d{4})', str(creation_date))
                    if year_match:
                        self.year = year_match.group(1)
                
                # If title is empty, try to extract from first page
                if not self.title and len(pdf.pages) > 0:
                    first_page = pdf.pages[0].extract_text()
                    lines = first_page.split('\n')
                    # Usually title is in first few lines
                    for line in lines[:10]:
                        line = line.strip()
                        if len(line) > 20 and len(line) < 200:
                            self.title = line
                            break
        
        except Exception as e:
            print(f"  Error extracting PDF metadata from {self.filename}: {e}")
    
    def extract_metadata_from_filename(self):
        """Try to extract year and author from filename."""
        # Common patterns: "Author_Year_Title.pdf" or "Author (Year) Title.pdf"
        filename_no_ext = self.filepath.stem
        
        # Look for year (4 digits)
        year_match = re.search(r'[(\[]?(\d{4})[)\]]?', filename_no_ext)
        if year_match and not self.year:
            self.year = year_match.group(1)
        
        # Try to extract author (usually first part before year or underscore)
        if not self.author:
            # Pattern: "LastName" or "LastName_FirstInitial" before year
            parts = re.split(r'[_\-\s]', filename_no_ext)
            if parts:
                potential_author = parts[0]
                # Clean up common prefixes
                potential_author = re.sub(r'^(the|a|an)\s+', '', potential_author, flags=re.IGNORECASE)
                if len(potential_author) > 2 and potential_author.isalpha():
                    self.author = potential_author
    
    def set_concept_from_folder(self, root_path):
        """Derive concept/topic from folder structure."""
        try:
            # Get relative path from root
            rel_path = self.filepath.relative_to(root_path)
            
            # Use parent folder name(s) as concept
            if len(rel_path.parents) > 1:
                # If nested, use all folder names except root
                folders = [p.name for p in rel_path.parents if p != Path('.')]
                folders.reverse()
                self.concept = ' > '.join(folders)
            else:
                self.concept = self.folder
            
            self.relative_path = str(rel_path)
        except:
            self.concept = "Uncategorized"


class PaperOrganizer:
    """Main class for organizing papers and generating spreadsheet."""
    
    def __init__(self, root_path, output_excel=None):
        self.root_path = Path(root_path)
        self.papers = []
        self.output_excel = output_excel or self.root_path / f"literature_review_{datetime.now().strftime('%Y%m%d')}.xlsx"
        
    def scan_papers(self, extensions=['.pdf']):
        """Recursively scan for paper files."""
        print(f"Scanning folder: {self.root_path}")
        
        for ext in extensions:
            for filepath in self.root_path.rglob(f"*{ext}"):
                # Skip hidden files and system folders
                if any(part.startswith('.') for part in filepath.parts):
                    continue
                
                paper = PaperMetadata(filepath)
                paper.set_concept_from_folder(self.root_path)
                
                # Extract metadata
                if paper.is_downloaded:
                    print(f"  Processing: {paper.filename}")
                    paper.extract_metadata_from_pdf()
                    paper.extract_metadata_from_filename()
                else:
                    print(f"  Skipping (not downloaded): {paper.filename}")
                    paper.extract_metadata_from_filename()
                
                self.papers.append(paper)
        
        print(f"\nFound {len(self.papers)} papers")
        downloaded = sum(1 for p in self.papers if p.is_downloaded)
        print(f"  Downloaded: {downloaded}")
        print(f"  Not downloaded: {len(self.papers) - downloaded}")
    
    def generate_spreadsheet(self):
        """Generate Excel spreadsheet following the template format."""
        if not EXCEL_SUPPORT:
            print("Error: openpyxl not installed. Cannot generate Excel file.")
            return
        
        print(f"\nGenerating spreadsheet: {self.output_excel}")
        
        # Create workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Literature Review"
        
        # Define headers (matching template)
        headers = [
            'Concept', 'Author', 'Year', 'Title', 'Journal', 
            'Main idea', 'Conclusion', 'Notes 1', 'Notes 2', 
            'Cross-ref', 'Excerpts', 'URL'
        ]
        
        # Add filename and download status columns
        headers.extend(['Filename', 'Downloaded', 'File Path'])
        
        # Write headers with formatting
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Sort papers by concept, then year
        sorted_papers = sorted(self.papers, key=lambda p: (
            p.concept or 'ZZZ',  # Put uncategorized at end
            p.year or '9999',
            p.author or 'ZZZ'
        ))
        
        # Write paper data
        current_concept = None
        row = 2
        
        for paper in sorted_papers:
            # Add a blank row between different concepts for readability
            if current_concept and paper.concept != current_concept:
                row += 1
            
            current_concept = paper.concept
            
            # Write data
            ws.cell(row=row, column=1, value=paper.concept)
            ws.cell(row=row, column=2, value=paper.author)
            ws.cell(row=row, column=3, value=paper.year)
            ws.cell(row=row, column=4, value=paper.title or paper.filename)
            ws.cell(row=row, column=5, value=paper.journal)
            # Columns 6-12 (Main idea, Conclusion, Notes, etc.) left empty for manual filling
            ws.cell(row=row, column=12, value=paper.url)
            
            # Additional columns
            ws.cell(row=row, column=13, value=paper.filename)
            ws.cell(row=row, column=14, value='Yes' if paper.is_downloaded else 'No')
            ws.cell(row=row, column=15, value=paper.relative_path)
            
            row += 1
        
        # Adjust column widths
        column_widths = {
            'A': 25,  # Concept
            'B': 20,  # Author
            'C': 8,   # Year
            'D': 50,  # Title
            'E': 20,  # Journal
            'F': 30,  # Main idea
            'G': 30,  # Conclusion
            'H': 25,  # Notes 1
            'I': 25,  # Notes 2
            'J': 15,  # Cross-ref
            'K': 30,  # Excerpts
            'L': 40,  # URL
            'M': 40,  # Filename
            'N': 12,  # Downloaded
            'O': 50,  # File Path
        }
        
        for col, width in column_widths.items():
            ws.column_dimensions[col].width = width
        
        # Freeze top row
        ws.freeze_panes = 'A2'
        
        # Save workbook
        wb.save(self.output_excel)
        print(f"Spreadsheet saved: {self.output_excel}")
    
    def generate_summary_report(self):
        """Generate a text summary of the papers found."""
        print("\n" + "="*80)
        print("SUMMARY REPORT")
        print("="*80)
        
        # Count by concept
        concept_counts = {}
        for paper in self.papers:
            concept = paper.concept or 'Uncategorized'
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        print(f"\nPapers by Concept/Topic:")
        for concept, count in sorted(concept_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {concept}: {count}")
        
        # Count by year
        year_counts = {}
        for paper in self.papers:
            year = paper.year or 'Unknown'
            year_counts[year] = year_counts.get(year, 0) + 1
        
        print(f"\nPapers by Year:")
        for year, count in sorted(year_counts.items()):
            print(f"  {year}: {count}")
        
        # Download status
        downloaded = sum(1 for p in self.papers if p.is_downloaded)
        print(f"\nDownload Status:")
        print(f"  Downloaded: {downloaded}")
        print(f"  Not downloaded: {len(self.papers) - downloaded}")
        
        # Papers without metadata
        no_title = sum(1 for p in self.papers if not p.title)
        no_author = sum(1 for p in self.papers if not p.author)
        no_year = sum(1 for p in self.papers if not p.year)
        
        print(f"\nMetadata Coverage:")
        print(f"  Missing title: {no_title}/{len(self.papers)}")
        print(f"  Missing author: {no_author}/{len(self.papers)}")
        print(f"  Missing year: {no_year}/{len(self.papers)}")


def main():
    parser = argparse.ArgumentParser(
        description='Organize research papers and generate literature review spreadsheet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan current directory
  python organize_papers.py .
  
  # Scan specific Dropbox folder
  python organize_papers.py ~/Dropbox/Research_Papers
  
  # Specify output Excel file
  python organize_papers.py ~/Dropbox/Research_Papers -o my_literature_review.xlsx
  
  # Include multiple file types
  python organize_papers.py ~/Papers -e .pdf .docx
        """
    )
    
    parser.add_argument('folder', type=str,
                       help='Root folder containing research papers')
    parser.add_argument('-o', '--output', type=str,
                       help='Output Excel filename (default: literature_review_YYYYMMDD.xlsx)')
    parser.add_argument('-e', '--extensions', nargs='+', default=['.pdf'],
                       help='File extensions to scan (default: .pdf)')
    
    args = parser.parse_args()
    
    # Validate folder
    root_path = Path(args.folder).expanduser().resolve()
    if not root_path.exists():
        print(f"Error: Folder does not exist: {root_path}")
        sys.exit(1)
    
    # Create organizer
    organizer = PaperOrganizer(root_path, args.output)
    
    # Scan papers
    organizer.scan_papers(extensions=args.extensions)
    
    # Generate outputs
    if organizer.papers:
        organizer.generate_spreadsheet()
        organizer.generate_summary_report()
    else:
        print("No papers found!")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("Done! Next steps:")
    print("  1. Open the Excel file and review the auto-extracted metadata")
    print("  2. For papers not downloaded, download them from Dropbox")
    print("  3. Re-run this script to update metadata for newly downloaded papers")
    print("  4. Fill in the Main idea, Conclusion, Notes, etc. columns manually")
    print("="*80)


if __name__ == '__main__':
    main()
