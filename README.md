# Google Form Automation

Automated Google Form submission with file upload support using Playwright.

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/muhammadmudassir9/Form-Automation.git
cd Form-Automation/form_automation
```

### 2. Install Dependencies
```bash
pip3 install playwright
python3 -m playwright install chromium
```

### 3. Configure Your Data
Edit `form_automation/main.py` and update the `FORM_DATA` section with your information:
```python
FORM_DATA = [
    'your.email@company.com',    # Your email
    datetime.now().strftime('%Y-%m-%d'),  # Date (auto)
    '12345-1234567-1',           # Your CNIC
    'EMP001',                    # Employee ID
    'Your Full Name',            # Your name
    'Senior Developer',          # Position
    '50',                        # Assigned limit
    '2500',                      # Amount claimed
]
```

### 4. Prepare Files
Create upload folder and add your files:
```bash
mkdir -p ~/Documents/upload
# Add files (.png, .jpg, .pdf, etc.) to ~/Documents/upload/
```

### 5. Run
```bash
python3 main.py
```
---

## What It Does

- Opens Google Form in browser
- Clears existing form data and files
- Fills 8 form fields automatically
- Uploads files from your folder
- Handles CAPTCHA (notifies you if needed)
- Submits form and verifies success

---

## Usage Options

**Custom Form URL:**
```bash
python3 main.py --url "https://docs.google.com/forms/d/e/FORM_ID/viewform"
```

**Headless Mode (no browser window):**
```bash
python3 main.py --headless
```

---

## Requirements

- Python 3.7+
- Google Account with form access
---

## Troubleshooting

**Python not found:**
```bash
python3 --version  # Check if installed
# Install: macOS: brew install python3, Linux: sudo apt install python3
```

**Playwright not found:**
```bash
pip3 install playwright
python3 -m playwright install chromium
```

**No files found:**
- Check files exist in `~/Documents/upload/`
- Supported: `.png`, `.jpg`, `.jpeg`, `.pdf`, `.doc`, `.docx`

**Login every time:**
- Don't delete `browser_data/` folder (saves your session)

**CAPTCHA appears:**
- Desktop notification will appear
- Script waits up to 3 minutes for you to solve it
- Check `browser_data/captcha_alert.txt` for alerts

---

## File Structure

```
Form-Automation/
├── README.md                      # This file
├── form_automation/
│   ├── main.py                   # Main script
│   ├── n8n_workflow.json        # n8n workflow (optional)
│   └── browser_data/            # Auto-created (saves login)
└── .gitignore
```

---

## n8n Setup (Optional - For Email Automation)

n8n can monitor Gmail and automatically run the script when emails arrive.

### Setup Steps

1. **Install n8n:**
   ```bash
   npm install n8n -g
   n8n start
   ```
   Open http://localhost:5678

2. **Enable Gmail API:**
   - Go to https://console.cloud.google.com/
   - Create project → Enable Gmail API
   - Create OAuth 2.0 credentials (Client ID & Secret)

3. **Configure n8n:**
   - Add Gmail OAuth2 credential with Client ID/Secret
   - Import `form_automation/n8n_workflow.json`
   - Update Execute Command node with your Python path
   - Configure Gmail nodes with your credential

4. **Test workflow:**
   - Execute workflow in n8n
   - Verify form submission

For detailed n8n setup, see `form_automation/README.md`

---

## Notes

- Login session saved in `browser_data/` - don't delete it
- CAPTCHA handling: Script notifies you and waits for manual resolution
- Logs: Check `browser_data/automation.log` for execution details
- Screenshots: Saved in `browser_data/screenshots/` for debugging
