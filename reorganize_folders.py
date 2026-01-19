#!/usr/bin/env python3
"""
Research Paper Folder Reorganization Tool
-----------------------------------------
Reorganizes research papers into a cleaner folder structure based on
extracted metadata or user-defined categorization rules.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime
import re
import json


class FolderReorganizer:
    """Reorganize papers into better folder structure."""
    
    def __init__(self, root_path, dry_run=True):
        self.root_path = Path(root_path)
        self.dry_run = dry_run
        self.moves = []  # Track all planned moves
        
    def suggest_reorganization(self):
        """Analyze current structure and suggest improvements."""
        print("Analyzing current folder structure...")
        
        # Get all PDF files
        all_pdfs = list(self.root_path.rglob('*.pdf'))
        
        # Analyze current organization
        folder_counts = {}
        for pdf in all_pdfs:
            folder = pdf.parent.relative_to(self.root_path)
            folder_str = str(folder) if folder != Path('.') else 'ROOT'
            folder_counts[folder_str] = folder_counts.get(folder_str, 0) + 1
        
        print(f"\nCurrent structure ({len(all_pdfs)} papers):")
        for folder, count in sorted(folder_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {folder}: {count} papers")
        
        # Identify issues
        print("\nPotential issues:")
        
        # Too many papers in root
        root_count = folder_counts.get('ROOT', 0)
        if root_count > 10:
            print(f"  ⚠️  {root_count} papers in root folder (consider categorizing)")
        
        # Folders with only 1-2 papers
        small_folders = {f: c for f, c in folder_counts.items() if c <= 2 and f != 'ROOT'}
        if small_folders:
            print(f"  ⚠️  {len(small_folders)} folders with ≤2 papers (consider consolidating)")
            for folder in list(small_folders.keys())[:5]:
                print(f"      - {folder}")
        
        # Deep nesting
        max_depth = max(len(Path(f).parts) for f in folder_counts.keys() if f != 'ROOT')
        if max_depth > 3:
            print(f"  ⚠️  Folders nested up to {max_depth} levels deep (consider flattening)")
    
    def reorganize_by_year(self, start_year=2000, end_year=None):
        """Reorganize papers into folders by publication year."""
        if end_year is None:
            end_year = datetime.now().year
        
        print(f"\nReorganizing by year ({start_year}-{end_year})...")
        
        for pdf in self.root_path.rglob('*.pdf'):
            # Skip if already in a year folder
            if re.match(r'\d{4}', pdf.parent.name):
                continue
            
            # Try to extract year from filename
            year_match = re.search(r'[(\[]?(\d{4})[)\]]?', pdf.stem)
            if year_match:
                year = int(year_match.group(1))
                if start_year <= year <= end_year:
                    target_folder = self.root_path / str(year)
                    self._plan_move(pdf, target_folder)
    
    def reorganize_by_keyword(self, keyword_map):
        """
        Reorganize papers based on keywords in filename or content.
        
        keyword_map: dict mapping folder names to lists of keywords
        Example: {
            'Quantum_Mechanics': ['quantum', 'entanglement', 'superposition'],
            'Statistical_Mechanics': ['statistical', 'thermodynamics', 'entropy'],
            'Optics': ['optical', 'laser', 'photon']
        }
        """
        print("\nReorganizing by keywords...")
        
        for pdf in self.root_path.rglob('*.pdf'):
            filename_lower = pdf.stem.lower()
            
            # Check each category
            for folder_name, keywords in keyword_map.items():
                if any(keyword.lower() in filename_lower for keyword in keywords):
                    target_folder = self.root_path / folder_name
                    self._plan_move(pdf, target_folder)
                    break  # Only move to first matching category
    
    def reorganize_by_author(self):
        """Reorganize papers into author-based folders."""
        print("\nReorganizing by author...")
        
        for pdf in self.root_path.rglob('*.pdf'):
            # Try to extract author from filename (assumes Author_Year_Title format)
            parts = re.split(r'[_\-]', pdf.stem)
            if parts:
                potential_author = parts[0]
                # Clean up
                potential_author = re.sub(r'[^a-zA-Z]', '', potential_author)
                
                if len(potential_author) > 2 and potential_author.isalpha():
                    # Organize by first letter for large collections
                    first_letter = potential_author[0].upper()
                    target_folder = self.root_path / 'By_Author' / first_letter / potential_author
                    self._plan_move(pdf, target_folder)
    
    def consolidate_small_folders(self, min_papers=3):
        """Move papers from small folders into an 'Other' folder."""
        print(f"\nConsolidating folders with <{min_papers} papers...")
        
        # Count papers in each folder
        folder_counts = {}
        for pdf in self.root_path.rglob('*.pdf'):
            folder = pdf.parent
            folder_counts[folder] = folder_counts.get(folder, 0) + 1
        
        # Move papers from small folders
        for folder, count in folder_counts.items():
            if count < min_papers and folder != self.root_path:
                # Get category from parent folder if nested
                category = folder.parent.name if folder.parent != self.root_path else 'Miscellaneous'
                target_folder = self.root_path / 'Other' / category
                
                for pdf in folder.glob('*.pdf'):
                    self._plan_move(pdf, target_folder)
    
    def flatten_structure(self, max_depth=2):
        """Reduce folder nesting depth."""
        print(f"\nFlattening folder structure (max depth: {max_depth})...")
        
        for pdf in self.root_path.rglob('*.pdf'):
            rel_path = pdf.relative_to(self.root_path)
            depth = len(rel_path.parents) - 1
            
            if depth > max_depth:
                # Create flattened path using underscores
                folder_names = [p.name for p in rel_path.parents if p != self.root_path]
                folder_names.reverse()
                new_folder_name = '_'.join(folder_names[:max_depth])
                target_folder = self.root_path / new_folder_name
                self._plan_move(pdf, target_folder)
    
    def _plan_move(self, source, target_folder):
        """Plan a file move (track for dry-run or execution)."""
        target_path = target_folder / source.name
        
        # Avoid moving file to same location
        if source.parent == target_folder:
            return
        
        # Handle filename conflicts
        if target_path.exists():
            counter = 1
            while target_path.exists():
                stem = source.stem
                target_path = target_folder / f"{stem}_{counter}{source.suffix}"
                counter += 1
        
        self.moves.append((source, target_path))
    
    def execute_moves(self):
        """Execute planned moves."""
        if not self.moves:
            print("No moves planned!")
            return
        
        print(f"\n{'DRY RUN: ' if self.dry_run else ''}Planning to move {len(self.moves)} files...")
        
        # Show sample of moves
        print("\nSample moves:")
        for source, target in self.moves[:10]:
            rel_source = source.relative_to(self.root_path)
            rel_target = target.relative_to(self.root_path)
            print(f"  {rel_source}")
            print(f"    → {rel_target}")
        
        if len(self.moves) > 10:
            print(f"  ... and {len(self.moves) - 10} more")
        
        if self.dry_run:
            print("\nDRY RUN MODE: No files were actually moved.")
            print("Run with --execute flag to perform the moves.")
            return
        
        # Confirm before proceeding
        response = input("\nProceed with moves? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
        
        # Execute moves
        moved_count = 0
        error_count = 0
        
        for source, target in self.moves:
            try:
                # Create target directory
                target.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file
                shutil.move(str(source), str(target))
                moved_count += 1
                
            except Exception as e:
                print(f"  Error moving {source.name}: {e}")
                error_count += 1
        
        print(f"\nCompleted: {moved_count} moved, {error_count} errors")
        
        # Clean up empty folders
        self._remove_empty_folders()
    
    def _remove_empty_folders(self):
        """Remove empty folders after reorganization."""
        print("\nCleaning up empty folders...")
        removed = 0
        
        for folder in sorted(self.root_path.rglob('*'), reverse=True):
            if folder.is_dir() and not any(folder.iterdir()):
                try:
                    folder.rmdir()
                    removed += 1
                except:
                    pass
        
        if removed:
            print(f"Removed {removed} empty folders")


def load_keyword_map(json_file):
    """Load keyword mapping from JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description='Reorganize research paper folders',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Reorganization strategies:
  --by-year              Organize into folders by publication year
  --by-author            Organize by author name (creates Author folders)
  --by-keywords FILE     Organize by keywords (provide JSON mapping file)
  --consolidate          Consolidate small folders into 'Other'
  --flatten              Reduce folder nesting depth

Examples:
  # Dry run (preview changes)
  python reorganize_folders.py ~/Dropbox/Papers --by-year
  
  # Actually execute the reorganization
  python reorganize_folders.py ~/Dropbox/Papers --by-year --execute
  
  # Multiple strategies
  python reorganize_folders.py ~/Papers --consolidate --flatten --execute
  
  # Use keyword map
  python reorganize_folders.py ~/Papers --by-keywords keywords.json --execute
        """
    )
    
    parser.add_argument('folder', type=str,
                       help='Root folder containing research papers')
    parser.add_argument('--by-year', action='store_true',
                       help='Organize papers by publication year')
    parser.add_argument('--by-author', action='store_true',
                       help='Organize papers by author')
    parser.add_argument('--by-keywords', type=str,
                       help='Organize by keywords (JSON file with folder→keywords mapping)')
    parser.add_argument('--consolidate', action='store_true',
                       help='Consolidate small folders')
    parser.add_argument('--flatten', action='store_true',
                       help='Flatten deep folder structures')
    parser.add_argument('--execute', action='store_true',
                       help='Actually perform the moves (default is dry-run)')
    
    args = parser.parse_args()
    
    # Validate folder
    root_path = Path(args.folder).expanduser().resolve()
    if not root_path.exists():
        print(f"Error: Folder does not exist: {root_path}")
        sys.exit(1)
    
    # Create reorganizer
    reorganizer = FolderReorganizer(root_path, dry_run=not args.execute)
    
    # Show current structure
    reorganizer.suggest_reorganization()
    
    # Apply reorganization strategies
    if args.by_year:
        reorganizer.reorganize_by_year()
    
    if args.by_author:
        reorganizer.reorganize_by_author()
    
    if args.by_keywords:
        keyword_map = load_keyword_map(args.by_keywords)
        reorganizer.reorganize_by_keyword(keyword_map)
    
    if args.consolidate:
        reorganizer.consolidate_small_folders()
    
    if args.flatten:
        reorganizer.flatten_structure()
    
    # Execute moves
    reorganizer.execute_moves()


if __name__ == '__main__':
    main()
