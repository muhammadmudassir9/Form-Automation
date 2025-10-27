# Google Form Automation - Enterprise Edition

**Zero-configuration automation solution for Google Forms**

## What This Does

Automatically completes Google Form submissions by:
- Clearing existing form data
- Filling all required fields with your data
- Uploading multiple files from your folder
- Submitting the form with verification

## Quick Start

### Step 1: Install Prerequisites
```bash
# Install Python package
pip install playwright

# Install browser
playwright install chromium
```

### Step 2: Configure Your Data (Required)
Edit `main.py` and update the `FORM_DATA` list (lines 33-42):

```python
# Edit these values in main.py
FORM_DATA = [
    'your.email@company.com',    # Your email (CHANGE THIS)
    datetime.now().strftime('%Y-%m-%d'),  # Date (auto-generated)
    '12345-1234567-1',           # Your CNIC (CHANGE THIS)
    'EMP001',                   # Your Employee ID (CHANGE THIS)
    'Muhammad Mudassar',        # Your name (CHANGE THIS)
    'Senior Developer',          # Your grade (CHANGE THIS)
    '50',                       # Your limit (CHANGE THIS)
    '2500',                     # Amount (CHANGE THIS)
]
```

**Note**: 
- **Date** (field 2) is auto-generated - don't change this line
- **All other fields** need your actual data
- Keep the quotes and commas as shown

### Step 3: Add Your Files
```bash
# Create upload folder in your home directory
mkdir -p ~/Documents/upload

# Add your files (images, PDFs, documents)
# Supported formats: .png, .jpg, .jpeg, .pdf, .doc, .docx
```

**File Location**: `~/Documents/upload/` or `$HOME/Documents/upload/`

### Step 4: Run Automation
```bash
# Navigate to automation folder
cd ~/Desktop/automation/form_automation

# Run the automation
python3 main.py
```

**That's it!** The automation will:
1. Open browser (login required first time only)
2. Clear the form
3. Fill your data
4. Upload your files
5. Submit successfully

**Note**: First time requires manual login to your Google account.

## Configuration (Optional)

### Update Your Data
Edit `main.py` lines 25-34 to change form data:

```python
FORM_DATA = [
    'your.email@company.com',    # Your email
    datetime.now().strftime('%Y-%m-%d'),  # Today's date
    '12345-1234567-1',           # Your CNIC
    'EMP001',                    # Your Employee ID
    'Your Full Name',            # Your name
    'Your Position',              # Your grade/position
    '50',                        # Your assigned limit
    '2500',                      # Amount claimed
]
```

### Change Upload Folder
Edit `main.py` line 20:

```python
UPLOAD_FOLDER_PATH = Path.home() / "Documents" / "your_folder"
```

### Auto-Close Browser
Edit `main.py` line 58:

```python
KEEP_BROWSER_OPEN = False  # Browser closes after completion
```

## File Requirements

### Supported File Types
- Images: `.png`, `.jpg`, `.jpeg`
- Documents: `.pdf`, `.doc`, `.docx`

### File Location
Place all files in: `~/Documents/upload/`

### File Naming
- Use any filename
- Avoid special characters
- Keep file sizes reasonable (< 10MB each)

## Troubleshooting

### "Login Required" Every Time
**Solution**: Don't delete the `browser_data` folder - it saves your login session.

### "No Files Found"
**Solution**: Check file location and types:
```bash
ls ~/Documents/upload/
# Should show your files
```

### "Form Not Loading"
**Solution**: Check internet connection and form URL accessibility.

### "Upload Failed"
**Solution**: 
- Verify file types are supported
- Check file sizes (try smaller files)
- Ensure files aren't corrupted

### "Submission Failed"
**Solution**:
- Check all form fields are filled
- Verify internet connection
- Review error screenshots in `browser_data/screenshots/`

## Understanding the Output

### Success Messages
Look for these in the terminal:
```
- Form load successful
- Form clear operation complete: 8 fields cleared
- Form field population complete: 8/8 fields
- File upload operation successful
- Form submission successful
- AUTOMATION COMPLETED SUCCESSFULLY
```

## File Structure

```
form_automation/
├── main.py                    # Main automation script
├── README.md                  # This guide
└── browser_data/              # Auto-created
    ├── automation.log        # Detailed logs
    └── screenshots/          # Error screenshots
```

## Advanced Usage

### Running Multiple Times
The automation can run multiple times in sequence:
1. Each run clears the form first
2. Fills with fresh data
3. Uploads files again
4. Submits successfully

### Batch Processing
To process multiple submissions:
1. Update `FORM_DATA` between runs
2. Or create multiple data sets
3. Run automation for each set

### Error Recovery
If automation fails:
1. Check error screenshots
2. Review log file
3. Fix configuration issues
4. Run again

## Support

### Log Analysis
Check `browser_data/automation.log` for detailed execution information.

### Visual Debugging
Error screenshots saved in `browser_data/screenshots/` show exactly what went wrong.

### Configuration Issues
Most problems are configuration-related:
- Wrong file paths
- Unsupported file types
- Incorrect form data

