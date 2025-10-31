# Google Form Automation

Automated Google Form submission with file upload support.

## Installation

```bash
pip install playwright
playwright install chromium
```

## Configuration

Edit `main.py` and update `FORM_DATA` with your information:

```python
FORM_DATA = [
    'your.email@company.com',    # Your email
    datetime.now().strftime('%Y-%m-%d'),  # Date (auto)
    '12345-1234567-1',           # CNIC
    'EMP001',                    # Employee ID
    'Your Name',                 # Name
    'Your Position',             # Grade
    '50',                        # Limit
    '2500',                      # Amount
]
```

## Usage

```bash
# Default form URL
python3 main.py

# Custom form URL
python3 main.py --url "https://docs.google.com/forms/d/e/FORM_ID/viewform"

# Headless mode
python3 main.py --url "FORM_URL" --headless
```

## File Upload

Place files in: `~/Documents/upload/`

Supported formats: `.png`, `.jpg`, `.jpeg`, `.pdf`, `.doc`, `.docx`

## Files

- `main.py` - Main automation script
- `email_monitor.py` - Email monitoring (alternative to n8n)
- `n8n_workflow.json` - n8n workflow definition
- `browser_data/` - Logs and screenshots
