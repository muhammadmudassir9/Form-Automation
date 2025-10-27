# Form Automation

Automated Google Forms submission with file upload support.

## Quick Start

```bash
# Clone repository
git clone https://github.com/muhammadmudassir9/Form-Automation.git
cd Form-Automation/form_automation

# Install dependencies
pip install playwright
playwright install chromium

# Configure and run
# Edit form_automation.py with your settings
python3 form_automation.py
```

## What It Does

1. Opens Google Form automatically
2. Fills 8 form fields
3. Uploads multiple files from folder
4. Submits form

## Prerequisites

- Python 3.7+
- Playwright library
- Chrome/Chromium browser

## Installation

```bash
# Install Python dependencies
pip install playwright

# Install browser
playwright install chromium
```

## Configuration

Edit `form_automation/form_automation.py`:

```python
FORM_URL = "https://docs.google.com/forms/d/YOUR_FORM_ID/viewform"
UPLOAD_FOLDER_PATH = "/path/to/upload/folder"
```

## Usage

```bash
# Prepare upload files
mkdir -p /path/to/uploads
cp *.png *.pdf /path/to/uploads/

# Run automation
python3 form_automation.py
```

## Project Structure

```
Form-Automation/
├── form_automation/
│   ├── form_automation.py
│   ├── README.md
│   └── browser_data/
├── README.md
└── .gitignore
```

## Documentation

For detailed instructions, see [form_automation/README.md](form_automation/README.md)

## License

MIT License

---

**Created by [Muhammad Mudassar](https://github.com/muhammadmudassir9)**
