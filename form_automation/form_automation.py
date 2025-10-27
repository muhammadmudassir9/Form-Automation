#!/usr/bin/env python3
"""
Google Form Automation
Complete automation with form filling, multiple file uploads, and submission
"""

import time
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# ==================== Configuration Constants ====================
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeHFwvq3NzKk9pvVl8CC5Lv8i5q7riXT2Uqcbq-oYyv85uSPQ/viewform"
BROWSER_DATA_DIR = "/home/muhammad.mudassar/Desktop/automation/form_automation/browser_data"
UPLOAD_FOLDER_PATH = "/home/muhammad.mudassar/Documents/upload"
SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.pdf', '.doc', '.docx']
FIELD_NAMES = ['Email', 'Date', 'CNIC', 'Employee ID', 'Name', 'Grade', 'Assigned Limit', 'Amount Claimed']

# ==================== UI Messages ====================
MSG_LOADING_FORM = "🌐 Loading form..."
MSG_LOGIN_REQUIRED = "🔐 Login required - please login manually"
MSG_WAITING_LOGIN = "⏳ Waiting for login completion..."
MSG_LOGIN_SUCCESS = "✅ Login successful!"
MSG_LOGIN_TIMEOUT = "❌ Login timeout"
MSG_FORM_LOADED = "✅ Form loaded successfully!"
MSG_FILLING_FIELDS = "📝 Filling form fields..."
MSG_FOUND_ELEMENTS = "📝 Found {} form elements"
MSG_FIELD_FILLED = "✅ {}: {}"
MSG_FIELD_ERROR = "⚠️ {}: {}"
MSG_FILLED_COUNT = "📝 Filled {} out of {} fields"
MSG_SCANNING_FOLDER = "📁 Scanning folder: {}"
MSG_FOLDER_NOT_FOUND = "❌ Folder not found: {}"
MSG_FOUND_FILE = "📄 Found file: {}"
MSG_TOTAL_FILES = "📁 Total files found: {}"
MSG_ERROR_SCANNING = "⚠️ Error scanning folder: {}"
MSG_HANDLING_UPLOAD = "📎 Handling file uploads..."
MSG_UPLOADING_FILES = "📎 Uploading {} files"
MSG_NO_FILES = "❌ No files found to upload"
MSG_ADD_FILE_CLICKED = "✅ Add file button clicked"
MSG_FILES_UPLOADED = "✅ {} files uploaded!"
MSG_UPLOAD_ERROR = "⚠️ Upload error: {}"
MSG_VALIDATING = "🔍 Validating form..."
MSG_FIELD_VALID = "✅ {}"
MSG_FIELD_INVALID = "❌ {}: Invalid"
MSG_ALL_FIELDS_VALID = "✅ All fields valid"
MSG_VALIDATION_ERROR = "⚠️ Error: {}"
MSG_SUBMITTING = "📤 Submitting form..."
MSG_FORM_VALIDATION_FAILED = "❌ Form validation failed"
MSG_SUBMIT_CLICKED = "✅ Submit clicked"
MSG_SUBMIT_ERROR = "⚠️ Error: {}"
MSG_VERIFYING = "📤 Verifying submission..."
MSG_SUBMISSION_SUCCESS = "🎉 SUBMISSION SUCCESSFUL!"
MSG_SUBMISSION_SUCCESS_SIMPLE = "✅ Submission successful!"
MSG_SUBMISSION_FAILED = "❌ Submission failed"
MSG_STILL_WAITING = "⏳ Still waiting... ({}s)"

# ==================== Selectors ====================
SEL_FORM_INPUTS = 'input:visible, textarea:visible'
SEL_ADD_FILE_BUTTON = '[role="button"]:has-text("Add file")'
SEL_FILE_INPUT = 'input[type="file"]'
SEL_SUBMIT_BUTTON = '[role="button"]:has-text("Submit")'
SEL_SUCCESS_MESSAGE = 'text="Your response has been recorded"'
JS_REMOVE_OVERLAYS = "document.querySelectorAll('div[class*=\"fFW7wc\"], div[class*=\"XKSfm\"]').forEach(el => el.remove());"

# ==================== Timing Constants ====================
TIMEOUT_FORM_LOAD = 60000
WAIT_AFTER_PAGE_LOAD = 5
WAIT_FIELD_CLICK = 0.5
WAIT_FIELD_CLEAR = 0.5
WAIT_FIELD_FILL = 0.5
WAIT_ADD_FILE = 5
WAIT_DRIVE_PICKER = 5
WAIT_UPLOAD_RETRY = 2
MAX_UPLOAD_ATTEMPTS = 5
WAIT_AFTER_UPLOAD = 5
WAIT_BEFORE_SUBMIT = 8
WAIT_AFTER_OVERLAY_REMOVE = 2
WAIT_AFTER_SUBMIT = 10
WAIT_VERIFY = 3
LOGIN_CHECK_INTERVAL = 2
LOGIN_STATUS_INTERVAL = 30
MAX_LOGIN_WAIT = 300
SCROLL_TIME = 3

# ==================== URL Patterns ====================
URL_ACCOUNTS_GOOGLE = "accounts.google.com"
URL_SIGNIN = "signin"
URL_DOCS_FORMS = "docs.google.com/forms"
URL_VIEWFORM = "viewform"

# ==================== Form Data ====================
FORM_DATA = [
    'muhammad.mudassar@rolustech.com',
    datetime.now().strftime('%Y-%m-%d'),
    '12345-1234567-1',
    'EMP001',
    'Muhammad Mudassar',
    'Senior Developer',
    '50',
    '2500',
]

def load_form(page):
    """Load Google Form and handle authentication"""
    print(MSG_LOADING_FORM)
    page.goto(FORM_URL, timeout=TIMEOUT_FORM_LOAD)
    time.sleep(WAIT_AFTER_PAGE_LOAD)
    
    if URL_ACCOUNTS_GOOGLE in page.url or URL_SIGNIN in page.url:
        print(MSG_LOGIN_REQUIRED)
        print(MSG_WAITING_LOGIN)
        
        for wait_time in range(0, MAX_LOGIN_WAIT, LOGIN_CHECK_INTERVAL):
            if URL_DOCS_FORMS in page.url and URL_VIEWFORM in page.url:
                print(MSG_LOGIN_SUCCESS)
                return True
            time.sleep(LOGIN_CHECK_INTERVAL)
            if wait_time % LOGIN_STATUS_INTERVAL == 0:
                print(MSG_STILL_WAITING.format(wait_time))
        
        print(MSG_LOGIN_TIMEOUT)
        return False
    
    print(MSG_FORM_LOADED)
    return True

def fill_form_fields(page):
    """Fill all form fields sequentially"""
    print(MSG_FILLING_FIELDS)
    
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(SCROLL_TIME)
    
    form_elements = page.locator(SEL_FORM_INPUTS)
    element_count = form_elements.count()
    print(MSG_FOUND_ELEMENTS.format(element_count))
    
    filled_count = 0
    for i, (field_name, value) in enumerate(zip(FIELD_NAMES, FORM_DATA)):
        if i < element_count:
            try:
                field = form_elements.nth(i)
                field.click()
                time.sleep(WAIT_FIELD_CLICK)
                field.clear()
                time.sleep(WAIT_FIELD_CLEAR)
                field.fill(value)
                time.sleep(WAIT_FIELD_FILL)
                print(MSG_FIELD_FILLED.format(field_name, value))
                filled_count += 1
            except Exception as e:
                print(MSG_FIELD_ERROR.format(field_name, e))
    
    print(MSG_FILLED_COUNT.format(filled_count, len(FORM_DATA)))
    return filled_count

def get_files_from_folder():
    """Get all supported files from upload folder"""
    print(MSG_SCANNING_FOLDER.format(UPLOAD_FOLDER_PATH))
    
    if not os.path.exists(UPLOAD_FOLDER_PATH):
        print(MSG_FOLDER_NOT_FOUND.format(UPLOAD_FOLDER_PATH))
        return []
    
    files = []
    try:
        for filename in os.listdir(UPLOAD_FOLDER_PATH):
            file_path = os.path.join(UPLOAD_FOLDER_PATH, filename)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename.lower())
                if ext in SUPPORTED_EXTENSIONS:
                    files.append(file_path)
                    print(MSG_FOUND_FILE.format(filename))
        
        print(MSG_TOTAL_FILES.format(len(files)))
        return files
        
    except Exception as e:
        print(MSG_ERROR_SCANNING.format(e))
        return []

def upload_files(page):
    """Upload all files from folder"""
    print(MSG_HANDLING_UPLOAD)
    
    files = get_files_from_folder()
    if not files:
        print(MSG_NO_FILES)
        return False
    
    print(MSG_UPLOADING_FILES.format(len(files)))
    
    try:
        page.locator(SEL_ADD_FILE_BUTTON).first.click()
        time.sleep(WAIT_ADD_FILE)
        print(MSG_ADD_FILE_CLICKED)
        time.sleep(WAIT_DRIVE_PICKER)
        
        # Retry search for file input
        for attempt in range(MAX_UPLOAD_ATTEMPTS):
            for frame in page.frames:
                try:
                    inputs = frame.locator(SEL_FILE_INPUT)
                    if inputs.count() > 0:
                        inputs.first.set_input_files(files)
                        print(MSG_FILES_UPLOADED.format(len(files)))
                        time.sleep(WAIT_AFTER_UPLOAD)
                        return True
                except Exception:
                    continue
            
            if attempt < MAX_UPLOAD_ATTEMPTS - 1:
                time.sleep(WAIT_UPLOAD_RETRY)
        
        # Try direct input
        inputs = page.locator(SEL_FILE_INPUT)
        if inputs.count() > 0:
            inputs.first.set_input_files(files)
            print(MSG_FILES_UPLOADED.format(len(files)))
            time.sleep(WAIT_AFTER_UPLOAD)
            return True
        
        return False
        
    except Exception as e:
        print(MSG_UPLOAD_ERROR.format(e))
        return False

def validate_form(page):
    """Validate all form fields"""
    print(MSG_VALIDATING)
    
    try:
        elements = page.locator(SEL_FORM_INPUTS)
        
        for i, name in enumerate(FIELD_NAMES):
            if i < elements.count():
                value = elements.nth(i).input_value()
                if not value or not value.strip():
                    print(MSG_FIELD_INVALID.format(name))
                    return False
                print(MSG_FIELD_VALID.format(name))
        
        print(MSG_ALL_FIELDS_VALID)
        return True
        
    except Exception as e:
        print(MSG_VALIDATION_ERROR.format(e))
        return False

def submit_form(page):
    """Submit form"""
    print(MSG_SUBMITTING)
    
    if not validate_form(page):
        print(MSG_FORM_VALIDATION_FAILED)
        return False
    
    try:
        time.sleep(WAIT_BEFORE_SUBMIT)
        
        # Remove overlays
        page.evaluate(JS_REMOVE_OVERLAYS)
        time.sleep(WAIT_AFTER_OVERLAY_REMOVE)
        
        # Click submit
        page.locator(SEL_SUBMIT_BUTTON).click(force=True)
        print(MSG_SUBMIT_CLICKED)
        time.sleep(WAIT_AFTER_SUBMIT)
        
        return verify_submission(page)
        
    except Exception as e:
        print(MSG_SUBMIT_ERROR.format(e))
        return False

def verify_submission(page):
    """Verify submission success"""
    time.sleep(WAIT_VERIFY)
    print(MSG_VERIFYING)
    
    # Check for success message
    if page.locator(SEL_SUCCESS_MESSAGE).count() > 0:
        print(MSG_SUBMISSION_SUCCESS)
        return True
    
    # Check URL
    if URL_VIEWFORM not in page.url.lower():
        print(MSG_SUBMISSION_SUCCESS_SIMPLE)
        return True
    
    print(MSG_SUBMISSION_FAILED)
    return False

def main():
    
    print("🤖 Google Form Automation")
    print("=" * 50)

    os.makedirs(BROWSER_DATA_DIR, exist_ok=True)

    try:
        with sync_playwright() as p:
            print("🌐 Launching browser...")
            context = p.chromium.launch_persistent_context(
                user_data_dir=BROWSER_DATA_DIR,
                headless=False,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            page = context.new_page()

            if load_form(page):
                filled_count = fill_form_fields(page)
                
                print(f"\n📊 FORM FILLING: {filled_count}/8 fields")
                
                if filled_count == 8:
                    print("✅ Form filling completed!")
                    
                    if upload_files(page):
                        print("✅ File upload completed!")
                        
                        if submit_form(page):
                            print("🎉 AUTOMATION SUCCESSFUL!")
                            print("✅ Form filled, files uploaded, and submitted!")
                        else:
                            print("❌ Form submission failed")
                    else:
                        print("❌ File upload failed")
                else:
                    print(f"❌ Form filling incomplete: {8 - filled_count} fields missing")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("✅ Automation completed!")

if __name__ == "__main__":
    main()