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

## Email Automation with n8n

n8n can monitor your Gmail and automatically run the script when emails with form links arrive.

### Step-by-Step n8n Setup

**Step 1: Install n8n**
```bash
npm install n8n -g
n8n start
```
Open http://localhost:5678 in your browser

**Step 2: Enable Gmail API**
1. Go to https://console.cloud.google.com/
2. Click "New Project" → Enter name: `Form Automation` → Create
3. Go to https://console.cloud.google.com/apis/library
4. Search "Gmail API" → Click it → Click "Enable"

**Step 3: Create OAuth Credentials**
1. Go to https://console.cloud.google.com/apis/credentials
2. Click "OAuth consent screen" → Select "External" → Create
3. Fill app name: `Form Automation`, your email → Save and Continue (3 times)
4. Go to "Credentials" tab → Click "Create Credentials" → "OAuth client ID"
5. Select "Web application" → Name: `n8n Gmail API` → Create
6. **Copy Client ID and Client Secret** (save them)

**Step 4: Add Gmail Credential in n8n**
1. In n8n (http://localhost:5678), click "Credentials" in sidebar
2. Click "+ Add Credential" → Search "Gmail OAuth2"
3. Enter:
   - Credential Name: `Gmail account`
   - Client ID: (paste from Step 3)
   - Client Secret: (paste from Step 3)
4. Click "Connect my account" → Allow Google permissions
5. Click "Save"

**Step 5: Import Workflow**
1. In n8n, click "Workflows" in sidebar
2. Click "+" → "Import from File"
3. Select `form_automation/n8n_workflow.json`

**Step 6: Configure Workflow**
1. Open the imported workflow
2. Click on each Gmail node → Select "Gmail account" credential
3. Click "Execute Command" node → Update command:
   ```bash
   cd /full/path/to/Form-Automation/form_automation && python3 main.py --url="{{ $json.body }}"
   ```
   (Replace with your actual path - find it with `which python3` and `pwd`)
4. Click "Save" → Toggle workflow to "Active"

**Step 7: Test**
1. Send yourself an email with a Google Form link
2. n8n should detect it and run the script automatically
3. Check n8n execution logs to verify

---

## Notes

- Login session saved in `browser_data/` - don't delete it
- CAPTCHA handling: Script notifies you and waits for manual resolution
- Logs: Check `browser_data/automation.log` for execution details
- Screenshots: Saved in `browser_data/screenshots/` for debugging
