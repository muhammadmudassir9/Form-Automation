# Google Form Automation

Automated Google Form submission with file upload support using Playwright.

## What This Does

This automation script:
1. Opens your Google Form
2. Clears existing form data (if any)
3. Fills 8 form fields automatically
4. Uploads multiple files from your folder
5. Submits the form
6. Verifies successful submission

## Prerequisites

Before starting, ensure you have:

### Required
- **Python 3.7+** installed
- **Google Account** with access to the target form
- **Internet connection**
- **Terminal/Command Prompt** access

### Check Prerequisites

```bash
# Check Python version
python3 --version
# Should show: Python 3.7.x or higher

# Check if pip is installed
pip3 --version
# Should show: pip version number
```

## Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/muhammadmudassir9/Form-Automation.git

# Navigate to the project directory
cd Form-Automation/form_automation
```

### Step 2: Install Dependencies

#### macOS/Linux

```bash
# Install Playwright
pip3 install playwright

# Install Chromium browser
python3 -m playwright install chromium

# Verify installation
python3 -m playwright --version
```

#### Windows

```bash
# Install Playwright
pip install playwright

# Install Chromium browser
playwright install chromium

# Verify installation
python -m playwright --version
```

### Step 3: Verify Installation

```bash
# Test that everything works
python3 --version
python3 -m playwright --version
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright installed successfully')"
```

**Expected output:** No errors, version numbers displayed

## Configuration

### Step 1: Prepare Upload Folder

Create a folder for files to upload:

```bash
# macOS/Linux
mkdir -p ~/Documents/upload

# Windows
mkdir %USERPROFILE%\Documents\upload
```

### Step 2: Add Your Files

Place your files in the upload folder:
- **Location:** `~/Documents/upload/` (macOS/Linux) or `C:\Users\YourName\Documents\upload\` (Windows)
- **Supported formats:** `.png`, `.jpg`, `.jpeg`, `.pdf`, `.doc`, `.docx`

### Step 3: Configure Form Data

Edit `main.py` file:

**1. Open `main.py` in a text editor**

**2. Find the `FORM_DATA` section (around line 33-42)**

**3. Update with your information:**

```python
FORM_DATA = [
    'your.email@company.com',              # Email - CHANGE THIS
    datetime.now().strftime('%Y-%m-%d'),   # Date - KEEP AS IS (auto-generated)
    '12345-1234567-1',                     # CNIC - CHANGE THIS
    'EMP001',                              # Employee ID - CHANGE THIS
    'Your Full Name',                      # Name - CHANGE THIS
    'Senior Developer',                     # Grade/Position - CHANGE THIS
    '50',                                  # Assigned Limit - CHANGE THIS
    '2500',                                # Amount Claimed - CHANGE THIS
]
```

**4. Save the file**

### Step 4: Verify Configuration

```bash
# Check that main.py exists and is readable
ls -la main.py  # macOS/Linux
# or
dir main.py     # Windows

# Verify Python can read it
python3 -m py_compile main.py
# No output = file is valid Python
```

## Usage

### Basic Usage (Manual Run)

```bash
# Make sure you're in the form_automation directory
cd Form-Automation/form_automation

# Run with default settings
python3 main.py
```

**First Time Run:**
1. Browser window will open automatically
2. You'll be prompted to login to Google (if not already logged in)
3. Login once - session will be saved automatically
4. Script completes the form submission

### Custom Form URL

```bash
# Run with custom form URL
python3 main.py --url "https://docs.google.com/forms/d/e/FORM_ID/viewform"
```


## Expected Output

When running successfully, you should see:

```
🤖 Google Form Automation 
==================================================
🌐 Initializing browser...
✅ Browser initialized
🌐 Loading form...
✅ Form load successful
🧹 Clearing form...
✅ Form clear operation complete: 8 fields cleared
📝 Filling form fields...
✅ Form field population complete: 8/8 fields
📎 Uploading files...
✅ File upload operation successful
📤 Submitting form...
✅ Form submission successful
🎉 AUTOMATION COMPLETED SUCCESSFULLY
```

## n8n Workflow Setup 

For automated scheduling and workflow management:

### Step 1: Install n8n

**Option A: Using npm (Recommended)**
```bash
# Install Node.js first (if not installed)
# macOS: brew install node
# Or download from nodejs.org

# Install n8n globally
npm install n8n -g

# Start n8n
n8n start
```



### Step 2: Access n8n

Open your browser and go to: **http://localhost:5678**

### Step 3: Set Up Gmail API (Required for Email Monitoring)

The n8n workflow uses Gmail API to monitor emails. Follow these steps:

#### 3.1: Enable Gmail API in Google Cloud Console

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project**
   - Click on project dropdown (top bar)
   - Click **"New Project"**
   - Enter project name: `Form Automation`
   - Click **"Create"**
   - Wait for project to be created

3. **Enable Gmail API**
   - Go to: https://console.cloud.google.com/apis/library
   - Search for **"Gmail API"**
   - Click on **Gmail API** result
   - Click **"Enable"** button
   - Wait for API to be enabled

#### 3.2: Create OAuth 2.0 Credentials

1. **Go to Credentials Page**
   - Visit: https://console.cloud.google.com/apis/credentials
   - Or: Click **"Credentials"** in left sidebar

2. **Create OAuth Consent Screen** (First Time Only)
   - Click **"OAuth consent screen"** tab
   - Select **"External"** user type
   - Click **"Create"**
   - Fill in required fields:
     - **App name**: `Form Automation`
     - **User support email**: Your email
     - **Developer contact**: Your email
   - Click **"Save and Continue"**
   - Click **"Save and Continue"** on Scopes (skip for now)
   - Click **"Save and Continue"** on Test users (skip for now)
   - Click **"Back to Dashboard"**

3. **Create OAuth 2.0 Client ID**
   - Go back to **"Credentials"** tab
   - Click **"+ CREATE CREDENTIALS"**
   - Select **"OAuth client ID"**
   - Select **Application type**: `Web application`
   - Enter **Name**: `n8n Gmail API`
   - Click **"Create"**
   - **Important**: Copy the **Client ID** and **Client Secret** immediately
     - These are shown only once!
   - Click **"OK"**

#### 3.3: Download Client Secret (Optional)

1. In Credentials page, find your OAuth 2.0 Client ID
2. Click the **download icon** (or click on the credential name)
3. Save the JSON file as `client_secret.json`
4. Keep this file secure - don't commit to git!

#### 3.4: Configure Gmail API in n8n

1. **In n8n Interface**
   - Go to http://localhost:5678
   - Click **"Credentials"** in left sidebar
   - Click **"+ Add Credential"**

2. **Select Gmail OAuth2**
   - Search for **"Gmail OAuth2"**
   - Click on it

3. **Enter Credentials**
   - **Credential Name**: `Gmail account` (or any name you prefer)
   - **Client ID**: Paste your Client ID from Google Cloud Console
   - **Client Secret**: Paste your Client Secret from Google Cloud Console

4. **Authorize Connection**
   - Click **"Connect my account"** button
   - A popup will open asking for Google permission
   - Select your Google account
   - Click **"Allow"** to grant permissions
   - Close the popup

5. **Save Credential**
   - Click **"Save"** button
   - Your Gmail credential is now set up!

**Note**: You only need to do this once. The credential will be saved and can be reused in workflows.

### Step 4: Import Workflow

1. In n8n, click **"Workflows"** in the sidebar
2. Click **"+"** button → **"Import from File"**
3. Select `n8n_workflow.json` file from the `form_automation` directory
4. Workflow will appear in your list

### Step 5: Configure Workflow

1. **Select Gmail Credential**
   - Open the imported workflow in n8n
   - Find Gmail nodes (there should be 2-3 Gmail nodes)
   - Click on each Gmail node
   - Under **"Credential"** dropdown, select **"Gmail account"** (the credential you created)
   - Repeat for all Gmail nodes in the workflow

2. **Configure Execute Command Node**
   
   **Find your Python path:**
   ```bash
   # macOS/Linux
   which python3
   # Output: /usr/local/bin/python3 or /usr/bin/python3
   
   # Windows
   where python
   # Output: C:\Python\python.exe
   ```
   
   **Update Execute Command Node:**
   - Click on the **"Execute Command"** node in workflow
   - Update command to:
   
   **macOS/Linux:**
   ```bash
   /usr/local/bin/python3 /full/path/to/Form-Automation/form_automation/main.py
   ```
   
   **Windows:**
   ```cmd
   C:\Python\python.exe C:\full\path\to\Form-Automation\form_automation\main.py
   ```

3. **Save Workflow**
   - Click **"Save"** button (top right)
   - Activate workflow (toggle switch)

### Step 6: Test n8n Workflow

1. Click **"Execute Workflow"** in n8n
2. Check execution log for success
3. Verify form was submitted

## Troubleshooting

### Issue: "python3: command not found"

**Solution:**
```bash
# Check if Python is installed
python3 --version

# If not installed:
# macOS: brew install python3
# Linux: sudo apt install python3
# Windows: Download from python.org
```

### Issue: "playwright: command not found"

**Solution:**
```bash
# Reinstall Playwright
pip3 install playwright
python3 -m playwright install chromium
```

### Issue: Browser won't open

**Solution:**
```bash
# Reinstall browser binaries
python3 -m playwright install chromium --force

# Check system dependencies (Linux)
python3 -m playwright install-deps chromium
```

### Issue: "No files found to upload"

**Solution:**
```bash
# Check upload folder exists
ls ~/Documents/upload/  # macOS/Linux
dir %USERPROFILE%\Documents\upload  # Windows

# Verify files are in the folder
# Check file extensions are supported (.png, .jpg, .pdf, etc.)
```

### Issue: Login required every time

**Solution:**
- Don't delete the `browser_data` folder - it saves your session
- Ensure browser_data directory has write permissions:
  ```bash
  chmod 755 browser_data/
  ```


### Issue: "Permission denied" errors

**Solution:**
```bash
# Make script executable
chmod +x main.py

# Check directory permissions
ls -la ./
```

### Issue: Gmail API "Access Denied" or "Invalid Credentials"

**Solution:**
1. **Check Gmail API is enabled**
   - Go to: https://console.cloud.google.com/apis/library
   - Search for "Gmail API"
   - Ensure it shows "Enabled"

2. **Verify OAuth Credentials**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Check your OAuth 2.0 Client ID exists
   - If missing, create new credentials (see Step 3 above)

3. **Re-authorize in n8n**
   - Go to n8n → Credentials
   - Click on your Gmail credential
   - Click **"Connect my account"** again
   - Re-authenticate with Google

4. **Check OAuth Consent Screen**
   - Go to: https://console.cloud.google.com/apis/credentials/consent
   - Ensure consent screen is configured
   - If in testing mode, add your email as a test user

### Issue: "Gmail API not enabled for this project"

**Solution:**
```bash
# Enable Gmail API:
1. Go to: https://console.cloud.google.com/apis/library
2. Search "Gmail API"
3. Click on it
4. Click "Enable" button
5. Wait 1-2 minutes for activation
```

### Issue: n8n Gmail nodes show "Credential not found"

**Solution:**
1. Ensure you created the Gmail credential in n8n (Step 3.4)
2. In workflow, click on Gmail node
3. Select your credential from dropdown
4. Save the workflow

## File Structure

```
Form-Automation/
├── form_automation/
│   ├── main.py                  # Main automation script
│   ├── n8n_workflow.json       # n8n workflow definition
│   ├── README.md               # This file
│   └── browser_data/           # Auto-created (don't commit)
│       ├── automation.log     # Execution logs
│       └── screenshots/       # Error screenshots
```

Before running, verify:

**Basic Setup:**
- [ ] Python 3.7+ is installed
- [ ] Playwright is installed (`pip3 install playwright`)
- [ ] Chromium browser is installed (`playwright install chromium`)
- [ ] Repository is cloned
- [ ] Upload folder exists (`~/Documents/upload/`)
- [ ] Files are in upload folder
- [ ] `FORM_DATA` in `main.py` is updated with your information
- [ ] Google account has access to the form

**For n8n Workflow:**
- [ ] n8n is installed and running
- [ ] Gmail API is enabled in Google Cloud Console
- [ ] OAuth 2.0 credentials are created (Client ID & Secret)
- [ ] Gmail credential is configured in n8n
- [ ] Workflow is imported (`n8n_workflow.json`)
- [ ] Gmail nodes have credential selected
- [ ] Execute Command node has correct Python path




