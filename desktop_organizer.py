#!/usr/bin/env python3
"""
Smart File Organizer for macOS
Organizes files by type, date, and size without relying on naming conventions
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import mimetypes

class FileOrganizer:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir).expanduser()
        
        # Your personal info for resume matching
        self.first_name = 'samia'
        self.last_name = 'ibrahim'
        
        # Define category mappings based on file extensions
        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.heic', '.webp', '.tiff', '.ico'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages', '.tex', '.md'],
            'Spreadsheets': ['.xls', '.xlsx', '.csv', '.numbers', '.ods'],
            'Presentations': ['.ppt', '.pptx', '.key', '.odp'],
            'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.aiff'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.dmg', '.iso'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs', '.swift', '.sh', '.json', '.xml', '.yml', '.yaml'],
            'Executables': ['.app', '.exe', '.dmg', '.pkg'],
            'Fonts': ['.ttf', '.otf', '.woff', '.woff2'],
        }
    
    def is_resume(self, filename):
        """Check if file is a resume based on name patterns"""
        name_lower = filename.lower()
        
        # Remove common separators and check for name + resume
        cleaned = name_lower.replace('_', '').replace('-', '').replace(' ', '')
        
        has_resume = 'resume' in name_lower or 'cv' in name_lower
        has_first = self.first_name.lower() in cleaned
        has_last = self.last_name.lower() in cleaned
        
        return has_resume and (has_first or has_last)
    
    def is_tax_document(self, filename):
        """Check if file is a tax document"""
        name_lower = filename.lower()
        
        # Check for year (2020-2030)
        has_year = any(str(year) in name_lower for year in range(2020, 2031))
        
        # Check for state codes
        has_state = 'il' in name_lower or 'mn' in name_lower
        
        # Check for tax keywords
        has_tax_keyword = any(keyword in name_lower for keyword in ['federal', 'state', 'tax', '1040', 'w2', 'w-2'])
        
        return has_year and (has_state or has_tax_keyword)
    
    def is_screenshot(self, filename):
        """Check if file is a screenshot"""
        name_lower = filename.lower()
        
        # macOS screenshot patterns
        screenshot_patterns = [
            'screenshot',
            'screen shot',
            'screen_shot',
            'capture',
            'scr ',  # Some apps use this prefix
        ]
        
        return any(pattern in name_lower for pattern in screenshot_patterns)
    
    def get_category(self, file_path):
        """Determine file category based on patterns and extension"""
        filename = file_path.name
        
        # Check specific patterns first (highest priority)
        if self.is_resume(filename):
            return 'Resumes'
        
        if self.is_tax_document(filename):
            return 'Tax Documents'
        
        if self.is_screenshot(filename):
            return 'Screenshots'
        
        # Then check by extension
        ext = file_path.suffix.lower()
        
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        
        return 'Other'
    
    def get_creation_date(self, file_path):
        """Get file creation date"""
        try:
            timestamp = os.path.getctime(file_path)
            return datetime.fromtimestamp(timestamp)
        except:
            return None
    
    def organize_by_type(self, dry_run=True):
        """Organize files into folders by type"""
        if not self.source_dir.exists():
            print(f"Error: Directory {self.source_dir} does not exist")
            return
        
        moved_files = 0
        skipped_files = 0
        
        print(f"\n{'DRY RUN - ' if dry_run else ''}Organizing files in: {self.source_dir}")
        print("=" * 60)
        
        for item in self.source_dir.iterdir():
            # Skip if it's a directory
            if item.is_dir():
                continue
            
            # Skip hidden files
            if item.name.startswith('.'):
                skipped_files += 1
                continue
            
            # Get category
            category = self.get_category(item)
            
            # Create category folder
            dest_folder = self.source_dir / category
            dest_path = dest_folder / item.name
            
            # Handle duplicate names
            counter = 1
            original_dest = dest_path
            while dest_path.exists():
                stem = original_dest.stem
                suffix = original_dest.suffix
                dest_path = dest_folder / f"{stem}_{counter}{suffix}"
                counter += 1
            
            print(f"  {item.name} → {category}/")
            
            if not dry_run:
                dest_folder.mkdir(exist_ok=True)
                shutil.move(str(item), str(dest_path))
            
            moved_files += 1
        
        print("=" * 60)
        print(f"Files to organize: {moved_files}")
        print(f"Skipped (hidden): {skipped_files}")
        
        if dry_run:
            print("\nThis was a DRY RUN. No files were moved.")
            print("Run with dry_run=False to actually move files.")
    
    def organize_by_date(self, dry_run=True):
        """Organize files into folders by creation year and month"""
        if not self.source_dir.exists():
            print(f"Error: Directory {self.source_dir} does not exist")
            return
        
        moved_files = 0
        
        print(f"\n{'DRY RUN - ' if dry_run else ''}Organizing files by date in: {self.source_dir}")
        print("=" * 60)
        
        for item in self.source_dir.iterdir():
            if item.is_dir() or item.name.startswith('.'):
                continue
            
            creation_date = self.get_creation_date(item)
            if not creation_date:
                continue
            
            # Create year/month folder structure
            year_month = creation_date.strftime("%Y/%Y-%m")
            dest_folder = self.source_dir / year_month
            dest_path = dest_folder / item.name
            
            print(f"  {item.name} → {year_month}/")
            
            if not dry_run:
                dest_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(dest_path))
            
            moved_files += 1
        
        print("=" * 60)
        print(f"Files organized: {moved_files}")


# Example usage
if __name__ == "__main__":
    # Change this to your target directory
    # Examples: 
    # - "~/Downloads"
    # - "~/Desktop"
    # - "~/Documents/Unsorted"
    
    organizer = FileOrganizer("~/Downloads")
    
    # First, do a dry run to see what would happen
    #organizer.organize_by_type(dry_run=True)
    
    # Uncomment the line below to actually organize files
    organizer.organize_by_type(dry_run=False)
    
    # Alternative: organize by date instead
    # organizer.organize_by_date(dry_run=True)
    # organizer.organize_by_date(dry_run=False)