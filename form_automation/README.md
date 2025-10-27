# Google Form Automation

**Automated Google Forms submission with file upload**

## What It Does

1. Opens Google Form
2. Fills 8 form fields automatically
3. Uploads multiple files from folder
4. Submits form

## Prerequisites

- Python 3.7+
- Playwright library
- Chrome/Chromium browser


## 🚀 Installation

**1. Clone Repository**
```bash
git clone https://github.com/muhammadmudassir9/Form-Automation.git
cd Form-Automation/form_automation
```

**2. Install Python Dependencies**
```bash
pip install playwright
playwright install chromium
```

**3. Verify Installation**
```bash
python3 --version
python3 -m playwright --version
```


## Configuration

Edit `form_automation.py`:

```python
# Form URL
FORM_URL = "https://docs.google.com/forms/d/YOUR_FORM_ID/viewform"

# Upload folder path
UPLOAD_FOLDER_PATH = "/path/to/upload/folder"

# Form data (8 fields)
FORM_DATA = [
    'your-email@example.com',           # Email
    datetime.now().strftime('%Y-%m-%d'), # Date
    '12345-1234567-1',                 # CNIC
    'EMP001',                          # Employee ID
    'Your Name',                        # Name
    'Senior Developer',                 # Grade
    '50',                              # Assigned Limit
    '2500',                            # Amount Claimed
]
```

## Usage

```bash
# Prepare files
mkdir -p /path/to/uploads
cp *.png *.pdf /path/to/uploads/

# Run automation
python3 form_automation.py
```

**First time:** Browser opens → Login to Google → Session saved

## File Structure

```
form_automation/
├── form_automation.py    # Main script
├── README.md            # Documentation
└── browser_data/        # Session data (auto-created)
```

## Troubleshooting

**Browser won't open:**
```bash
python3 -m playwright install chromium --force
```

**Login required every time:**
```bash
rm -rf browser_data/
python3 form_automation.py
```

**Files not uploading:**
- Check folder path exists
- Verify file permissions
- Ensure supported extensions: `.png`, `.jpg`, `.jpeg`, `.pdf`, `.doc`, `.docx`
