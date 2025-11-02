# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal dotfiles repository focused on configuration management and custom tools, with a primary emphasis on an IME dictionary management system. The repository uses Japanese for documentation and user-facing content.

## Repository Structure

```
dotfiles/
├── configs/               # Configuration files (shell, vim, git, system)
├── tools/                 # Custom tools and applications
│   └── ime-dictionaries/  # IME dictionary management system (primary project)
├── index.html            # GitHub Pages landing page
└── .github/workflows/    # CI/CD for GitHub Pages deployment
```

## IME Dictionary Management System

The main feature of this repository is `tools/ime-dictionaries/`, which provides:

- JSON-based dictionary storage (`data/dictionary.json`)
- Web-based editor (`tools/web-editor/`) with browser-based editing
- Python converter (`tools/converter/convert.py`) for multi-platform export
- Platform-specific outputs: macOS (.plist), Windows (UTF-16LE), CSV, TXT

### Architecture

1. **Data Layer**: JSON schema-validated dictionary storage with categories, words, readings, and metadata
2. **Web Editor**: Vanilla JavaScript app (`app.js` + `index.html`) - no build step required
3. **Converter**: Python CLI tool for format conversion with category filtering
4. **Testing**: Separate test suites for Python and Web components

### Key Design Decisions

- **No Build Tools**: Web editor runs directly in browser via Python HTTP server
- **UTF-16LE BOM**: Windows IME requires specific encoding with BOM for proper import
- **Category System**: Words organized by categories with enable/disable flags
- **Multi-category Export**: Users can select multiple categories to merge into single output file

## Common Commands

### IME Dictionary Development

```bash
# Start web editor locally
cd tools/ime-dictionaries/tools/web-editor
python3 -m http.server 8000
# Open http://localhost:8000 in browser

# Convert dictionary to various formats
cd tools/ime-dictionaries/tools/converter

# List available categories
python3 convert.py ../../data/dictionary.json --list-categories

# Show statistics
python3 convert.py ../../data/dictionary.json --stats

# Export to CSV (with BOM for Excel compatibility)
python3 convert.py ../../data/dictionary.json --csv output.csv

# Export specific categories (merged into one file)
python3 convert.py ../../data/dictionary.json --csv output.csv --categories "記号・マーク,矢印"

# Export to macOS format
python3 convert.py ../../data/dictionary.json --macos dictionary.plist

# Export to Windows format (UTF-16LE with BOM)
python3 convert.py ../../data/dictionary.json --windows windows_dict.txt

# Export all formats at once
python3 convert.py ../../data/dictionary.json --all-formats --output-dir ./output
```

### Testing

```bash
# Run Python converter tests
cd tools/ime-dictionaries/tests
python3 test_converter.py

# Run with coverage report
python3 -m coverage run test_converter.py
python3 -m coverage report
python3 -m coverage html  # Generates htmlcov/index.html

# Web editor tests: Open tests/test_web.html in browser
```

### GitHub Pages Deployment

Automatic deployment occurs on push to `main` branch via GitHub Actions:

```bash
# Manual workflow trigger
gh workflow run deploy-pages.yml

# Check deployment status
gh run list --workflow=deploy-pages.yml
```

Published URLs:
- Main: https://hirotaka42.github.io/dotfiles/
- IME Editor: https://hirotaka42.github.io/dotfiles/tools/ime-dictionaries/tools/web-editor/index.html

## Working with the Codebase

### Code Style

- **Python**: Standard library only (no external dependencies), Python 3.6+ compatible
- **JavaScript**: Vanilla ES6+, no frameworks or build tools
- **Encoding**: UTF-8 for source files, UTF-8-SIG for CSV exports, UTF-16LE for Windows IME

### JSON Dictionary Schema

The dictionary follows this structure:

```json
{
  "辞書情報": {
    "名前": "Dictionary Name",
    "説明": "Description",
    "更新日": "YYYY-MM-DD"
  },
  "カテゴリ": {
    "Category Name": {
      "説明": "Category description",
      "有効": true,
      "単語リスト": [
        {
          "読み": "reading",
          "読み_Windows": "windows-reading (optional)",
          "単語": "word",
          "品詞": "名詞",
          "説明": "description",
          "タグ": ["tag1", "tag2"]
        }
      ]
    }
  }
}
```

Required fields: `読み` (reading) and `単語` (word)

Optional fields:
- `読み_Windows`: Windows-specific reading (recommended when `読み` contains only half-width alphanumeric characters)

### Important Files

- `tools/ime-dictionaries/data/dictionary.json` - Main dictionary data (auto-loads in web editor)
- `tools/ime-dictionaries/data/schema.json` - JSON Schema validation
- `tools/ime-dictionaries/tools/converter/convert.py` - Format conversion logic
- `tools/ime-dictionaries/tools/web-editor/app.js` - Web editor functionality

## Platform-Specific Notes

### macOS IME Export
- Uses Property List (plist) format
- Text encoding: UTF-8
- Part of speech mapping: Japanese → English (e.g., "名詞" → "Noun")
- **Reading field**: Always uses `読み` field

### Windows IME Export
- Requires UTF-16LE encoding with BOM
- Tab-separated format: `読み\t単語\t品詞`
- Part of speech mapping: Japanese → Japanese (e.g., "名詞" → "名詞")
- **Reading field priority**: Uses `読み_Windows` if present, otherwise falls back to `読み`
- **Important**: Half-width alphanumeric readings (e.g., "mem", "meko") don't work in Windows IME, so `読み_Windows` should be set with hiragana equivalents (e.g., "めも", "めーこ")

### CSV Export
- Uses UTF-8-SIG (BOM) for Excel compatibility
- All fields quoted with `csv.QUOTE_ALL`
- Header row: 読み, 単語, 品詞, 説明, タグ, カテゴリ

## Testing Requirements

When modifying converter or web editor:
1. Run Python tests: `python3 test_converter.py`
2. Open and run web tests: `tests/test_web.html`
3. Verify encoding with actual IME import on both macOS and Windows if changing format converters

Test coverage includes:
- Encoding handling (UTF-8, UTF-16LE BOM)
- Category filtering
- Format conversion accuracy
- CSV escaping and special characters
- Part of speech mapping

## Git Workflow

- Main branch: `main`
- Commit messages: Japanese or English acceptable
- Recent commits show pattern: `feat:`, `fix:`, `test:` prefixes
- Deploy to GitHub Pages automatically on push to main

## Privacy and Security

- Personal dictionary data goes in `tools/ime-dictionaries/data/personal/` (gitignored)
- Sample data uses `example@example.com` for email addresses
- No sensitive information should be committed to the repository
