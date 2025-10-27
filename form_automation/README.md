# 🤖 Google Form Automation

**Automated Form Filling with File Upload**

Complete automation solution for Google Forms that fills 8 fields, uploads multiple files, and submits automatically without any manual intervention.

---

## 🎯 Features

- ✅ **Automatically fills 8 form fields** (Email, Date, CNIC, Employee ID, Name, Grade, Assigned Limit, Amount Claimed)
- ✅ **Uploads multiple files** from a designated folder (images and PDFs)
- ✅ **100% automated submission** - no manual intervention required
- ✅ **Handles Google authentication** with persistent session
- ✅ **Robust error handling** and retry mechanisms

---

## 📋 Prerequisites

- Python 3.7+
- Playwright library
- Chrome/Chromium browser

---

## 🚀 Installation

### 1. Install Python Dependencies

```bash
pip install playwright
playwright install chromium
```

### 2. Verify Installation

```bash
python3 --version
python3 -m playwright --version
```

---

## ⚙️ Configuration

Edit the constants at the top of `form_automation.py`:

```python
# Form Configuration
FORM_URL = "https://docs.google.com/forms/d/.../viewform"
BROWSER_DATA_DIR = "/path/to/browser_data"
UPLOAD_FOLDER_PATH = "/path/to/upload/folder"

# Form Data (update as needed)
FORM_DATA = [
    'your-email@example.com',      # Email
    datetime.now().strftime('%Y-%m-%d'),  # Date (auto)
    '12345-1234567-1',             # CNIC
    'EMP001',                      # Employee ID
    'Your Name',                   # Name
    'Senior Developer',            # Grade
    '50',                          # Assigned Limit
    '2500',                        # Amount Claimed
]

# Supported File Extensions
SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.pdf', '.doc', '.docx']
```

---

## 📁 File Structure

```
form_automation/
├── form_automation.py    # Main automation script (340 lines)
├── README.md            # This file
└── browser_data/        # Browser session (auto-created)
```

---

## 🚀 Usage

### Basic Usage

```bash
cd /home/muhammad.mudassar/Desktop/automation/form_automation
python3 form_automation.py
```

### Prepare Files for Upload

Place your files in the configured upload folder:

```bash
mkdir -p /path/to/upload/folder
cp slip.png /path/to/upload/folder/
cp document.pdf /path/to/upload/folder/
```

---



## 📊 Workflow Diagram

```
User Runs Script
      ↓
┌─────────────────────┐
│ Load Form           │ ← Login if needed
└─────────────────────┘
      ↓
┌─────────────────────┐
│ Fill 8 Fields       │ ← Email, Date, CNIC, etc.
└─────────────────────┘
      ↓
┌─────────────────────┐
│ Upload Files        │ ← Images, PDFs
└─────────────────────┘
      ↓
┌─────────────────────┐
│ Validate Form       │ ← Check all fields
└─────────────────────┘
      ↓
┌─────────────────────┐
│ Submit Form         │ ← Automatic submission
└─────────────────────┘
      ↓
┌─────────────────────┐
│ Verify Success      │ ← Check confirmation
└─────────────────────┘
      ↓
    ✅ DONE
```

---

## 📝 Supported File Types

- **Images**: `.png`, `.jpg`, `.jpeg`
- **Documents**: `.pdf`, `.doc`, `.docx`

Add or remove extensions in `SUPPORTED_EXTENSIONS` constant.

---

## 🛠️ Troubleshooting

### Browser Not Opening

```bash
# Check Playwright installation
python3 -m playwright install chromium --force

# Check permissions
chmod +x form_automation.py
```

### Login Required Every Time

```bash
# Delete browser session data
rm -rf browser_data/

# Run again and login manually once
python3 form_automation.py
```

### File Upload Fails

```bash
# Check folder path
ls /path/to/upload/folder

# Check file permissions
chmod 644 /path/to/upload/folder/*.png

# Verify supported extensions
```

### Form URL Changed

Update the `FORM_URL` constant in the script:

```python
FORM_URL = "https://docs.google.com/forms/d/NEW_FORM_ID/viewform"
```



## 🔍 Code Structure

### Functions

- `load_form(page)` - Load Google Form and authenticate
- `fill_form_fields(page)` - Fill 8 form fields
- `get_files_from_folder()` - Scan upload folder
- `upload_files(page)` - Upload multiple files
- `validate_form(page)` - Validate all fields
- `submit_form(page)` - Submit the form
- `verify_submission(page)` - Verify success
- `main()` - Orchestrate the entire process

### Constants

- **Configuration**: URLs, paths, supported extensions
- **Messages**: All UI messages centralized
- **Selectors**: CSS selectors for form elements
- **Timing**: Wait times and timeouts
- **URL Patterns**: URL matching patterns
- **Form Data**: Field values

---



---

## 📝 License

This code is provided as-is for automation purposes.

---
