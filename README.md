# desktop-organizer (macOS)

A small Python utility that organizes files in a folder (like `~/Downloads`) **without relying on naming conventions**—primarily by **file type**, with a few **smart, high-priority pattern rules** (Resumes, Tax Documents, Screenshots). It can also organize by **creation date (year/month)**.

**Use carefully:** Always run a dry run first.

---

## Features

### Organize by type (default)
Moves files into category folders such as:

- `Images/` (`.jpg`, `.png`, `.heic`, …)
- `Documents/` (`.pdf`, `.docx`, `.md`, …)
- `Spreadsheets/` (`.xlsx`, `.csv`, …)
- `Presentations/` (`.pptx`, `.key`, …)
- `Videos/`, `Audio/`, `Archives/`, `Code/`, `Fonts/`, `Executables/`
- `Other/` for anything unmatched

### Smart “special cases” (higher priority than extension)
The script checks these before normal file-type rules:

- **Resumes** → `Resumes/`  
  Detects `resume`/`cv` plus your name patterns.
- **Tax Documents** → `Tax Documents/`  
  Looks for years (2020–2030) plus state codes (`ca`, `mn`) or tax keywords (`1040`, `w2`, `tax`, etc.).
- **Screenshots** → `Screenshots/`  
  Matches common macOS screenshot naming patterns (e.g., “Screenshot”, “Screen Shot”, “capture”, etc.).

### Duplicate filename handling
If a destination filename already exists, it will create a new name like:
`file.pdf` → `file_1.pdf`, `file_2.pdf`, etc.

### Skips hidden files
Anything starting with `.` is ignored.

---

## Requirements

- Python 3.8+ (recommended)
- macOS (designed for macOS file patterns, but works on other OSes too)

No external dependencies.

---

## Installation

1. Save the script as something like:
   `desktop_organizer.py`

2. (Optional) Make it executable:
   ```bash
   chmod +x file_organizer.py
