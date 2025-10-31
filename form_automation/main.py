#!/usr/bin/env python3
"""
Google Form Automation - Enterprise Grade
Production-ready automation with enterprise best practices
"""

import logging
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List
from playwright.sync_api import Page, sync_playwright, TimeoutError as PlaywrightTimeoutError


# ==================== Configuration ====================
class Config:
    """Centralized configuration management"""
    
    # URLs
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeHFwvq3NzKk9pvVl8CC5Lv8i5q7riXT2Uqcbq-oYyv85uSPQ/viewform"
    
    # Paths
    BROWSER_DATA_DIR = Path.home() / "Desktop" / "automation" / "form_automation" / "browser_data"
    UPLOAD_FOLDER_PATH = Path.home() / "Documents" / "upload"
    SCREENSHOT_DIR = BROWSER_DATA_DIR / "screenshots"
    LOG_FILE = BROWSER_DATA_DIR / "automation.log"
    
    # File handling
    SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.pdf', '.doc', '.docx']
    
    # Form data
    FIELD_NAMES = ['Email', 'Date', 'CNIC', 'Employee ID', 'Name', 'Grade', 'Assigned Limit', 'Amount Claimed']
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
    
    # Selectors
    SEL_FORM_INPUTS = 'input:visible, textarea:visible'
    SEL_ADD_FILE = '[role="button"]:has-text("Add file")'
    SEL_FILE_INPUT = 'input[type="file"]'
    SEL_SUBMIT = '[role="button"]:has-text("Submit")'
    SEL_SUCCESS = 'text="Your response has been recorded"'
    SEL_REMOVE_FILE = '[aria-label*="Remove"], [aria-label*="Delete"], button:has-text("Remove")'
    SEL_UPLOAD_PROGRESS = '[class*="upload"], [class*="progress"], [class*="spinner"]'
    SEL_FILE_NAMES = 'text=/.*\\.(png|jpg|jpeg|pdf|doc|docx)$/i'
    SEL_SUCCESS_INDICATORS = '[class*="success"], [class*="complete"], [class*="thank"]'
    SEL_ERROR_INDICATORS = 'text=/error|required|invalid|missing/i'
    
    # Timeouts (milliseconds)
    TIMEOUT_FORM_LOAD = 60000
    TIMEOUT_ELEMENT = 10000
    TIMEOUT_LOGIN = 300000
    CAPTCHA_WAIT = 180000  # wait up to 3 minutes if captcha appears
    WAIT_SHORT = 1000
    WAIT_MEDIUM = 2000
    WAIT_LONG = 5000
    UPLOAD_WAIT_MAX = 30
    
    # Retry settings
    MAX_UPLOAD_RETRIES = 5
    MAX_SUBMIT_RETRIES = 3
    
    # Browser settings
    KEEP_BROWSER_OPEN = True
    NOTIFICATION_TITLE = "Action Required: Solve CAPTCHA"
    
    # Success messages
    SUCCESS_MESSAGES = [
        "Your response has been recorded",
        "Response recorded", 
        "Thank you for your response",
        "Form submitted successfully"
    ]
    
    # JavaScript for overlay removal
    JS_REMOVE_OVERLAYS = "document.querySelectorAll('div[class*=\"fFW7wc\"], div[class*=\"XKSfm\"]').forEach(el => el.remove());"


# ==================== Logging Setup ====================
def setup_logging() -> None:
    """Configure enterprise logging system"""
    Config.BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Log startup
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("Google Form Automation - Enterprise Edition")
    logger.info("=" * 60)


# ==================== Utility Functions ====================
def take_screenshot(page: Page, name: str) -> None:
    """Capture screenshot with enterprise naming convention"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = Config.SCREENSHOT_DIR / f"{name}_{timestamp}.png"
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot_path))
        logging.info(f"Screenshot captured: {screenshot_path.name}")
    except Exception as e:
        logging.error(f"Screenshot capture failed: {e}")


def notify_user(message: str) -> None:
    """Send a desktop notification if possible and log the message.

    - On Linux, uses `notify-send` when available.
    - Also writes a marker file under browser_data so external watchers can react.
    """
    logger = logging.getLogger(__name__)
    logger.warning(message)
    try:
        # Marker file for external hooks/cron or user checks
        marker = Config.BROWSER_DATA_DIR / "captcha_alert.txt"
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(f"{datetime.now().isoformat()} - {message}\n", encoding="utf-8")
    except Exception:
        pass

    try:
        if shutil.which("notify-send"):
            subprocess.Popen(["notify-send", Config.NOTIFICATION_TITLE, message])
    except Exception:
        # Best-effort; logging already covers visibility
        pass

def get_files_from_folder() -> List[str]:
    """Get supported files with enterprise error handling"""
    logger = logging.getLogger(__name__)
    logger.info(f"Scanning upload directory: {Config.UPLOAD_FOLDER_PATH}")
    
    if not Config.UPLOAD_FOLDER_PATH.exists():
        logger.error(f"Upload directory not found: {Config.UPLOAD_FOLDER_PATH}")
        return []
    
    files = []
    try:
        for filename in os.listdir(Config.UPLOAD_FOLDER_PATH):
            file_path = Config.UPLOAD_FOLDER_PATH / filename
            if file_path.is_file() and file_path.suffix.lower() in Config.SUPPORTED_EXTENSIONS:
                files.append(str(file_path))
                logger.debug(f"File discovered: {filename}")
        
        logger.info(f"File discovery complete: {len(files)} files found")
        return files
        
    except Exception as e:
        logger.error(f"File discovery failed: {e}")
        return []


# ==================== Core Automation Functions ====================
def load_form(page: Page) -> bool:
    """Load form with enterprise error handling"""
    logger = logging.getLogger(__name__)
    logger.info("Initializing form load process")
    
    try:
        page.goto(Config.FORM_URL, timeout=Config.TIMEOUT_FORM_LOAD)
        page.wait_for_load_state('networkidle')
        
        # Authentication handling
        if "accounts.google.com" in page.url or "signin" in page.url:
            logger.info("Authentication required - awaiting user login")
            page.wait_for_url(
                lambda url: "docs.google.com/forms" in url and "viewform" in url,
                timeout=Config.TIMEOUT_LOGIN
            )
            logger.info("Authentication successful")
            return True
        
        logger.info("Form load successful")
        return True
        
    except PlaywrightTimeoutError:
        logger.error("Authentication timeout exceeded")
        take_screenshot(page, "auth_timeout")
        return False
    except Exception as e:
        logger.error(f"Form load failure: {e}")
        take_screenshot(page, "load_error")
        return False


def clear_form(page: Page) -> bool:
    """Clear form by clicking the built-in Clear form action and confirming."""
    logger = logging.getLogger(__name__)
    logger.info("Initiating form clear operation")
    
    try:
        # Scroll near the bottom where Clear form usually lives
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(Config.WAIT_SHORT)

        # Candidate selectors for Clear form action
        clear_selectors = [
            '[role="button"]:has-text("Clear form")',
            'button:has-text("Clear form")',
            'text="Clear form"',
        ]

        # Attempt to locate and click Clear form
        clear_clicked = False
        for sel in clear_selectors:
            try:
                loc = page.locator(sel)
                if loc.count() > 0:
                    logger.info("Clicking Clear form")
                    loc.first.click(timeout=Config.TIMEOUT_ELEMENT)
                    clear_clicked = True
                    break
            except Exception:
                continue

        if not clear_clicked:
            # Fallback: sometimes the control is above; scroll up and try again
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(Config.WAIT_MEDIUM)
            for sel in clear_selectors:
                try:
                    loc = page.locator(sel)
                    if loc.count() > 0:
                        logger.info("Clicking Clear form (fallback)")
                        loc.first.click(timeout=Config.TIMEOUT_ELEMENT)
                        clear_clicked = True
                        break
                except Exception:
                    continue

        if not clear_clicked:
            logger.warning("Clear form control not found; skipping clear step")
            return True

        # Confirm in dialog
        confirmed = False
        try:
            dialog = page.locator('[role="dialog"], [role="alertdialog"]')
            # Wait for dialog to appear
            try:
                dialog.wait_for(state='visible', timeout=Config.TIMEOUT_ELEMENT)
            except Exception:
                page.wait_for_timeout(Config.WAIT_SHORT)
            if dialog.count() > 0:
                # Prefer the exact label "Clear form" shown in Google Forms
                confirm_variants = [
                    '[role="dialog"] [role="button"]:has-text("Clear form")',
                    '[role="alertdialog"] [role="button"]:has-text("Clear form")',
                    '[role="dialog"] button:has-text("Clear form")',
                    '[role="alertdialog"] button:has-text("Clear form")',
                    'role=button[name="Clear form"]',
                    '[role="dialog"] [role="button"]:has-text("Clear")',
                    '[role="alertdialog"] [role="button"]:has-text("Clear")',
                    '[role="dialog"] button:has-text("Clear")',
                    '[role="alertdialog"] button:has-text("Clear")',
                    '[role="dialog"] [data-mdc-dialog-action="accept"]',
                    '[role="alertdialog"] [data-mdc-dialog-action="accept"]',
                ]
                for variant in confirm_variants:
                    try:
                        btn = page.locator(variant)
                        if btn.count() > 0:
                            logger.info("Confirming Clear form in dialog")
                            btn.first.click(timeout=Config.TIMEOUT_ELEMENT)
                            confirmed = True
                            break
                    except Exception:
                        continue
                if not confirmed:
                    # Fallback to pressing Enter to accept
                    try:
                        page.keyboard.press('Enter')
                        confirmed = True
                    except Exception:
                        pass
            # Wait for dialog to disappear so we don't stall
            try:
                dialog.wait_for(state='hidden', timeout=Config.TIMEOUT_ELEMENT)
            except Exception:
                pass
        except Exception:
            pass

        if not confirmed:
            logger.info("No confirmation dialog detected; proceeding")

        # Give the form a moment to reset
        page.wait_for_timeout(Config.WAIT_LONG)
        logger.info("Form clear operation complete")
        return True
        
    except Exception as e:
        logger.error(f"Form clear operation failed: {e}")
        take_screenshot(page, "clear_error")
        return False


def fill_form_fields(page: Page) -> int:
    """Fill form fields with enterprise validation"""
    logger = logging.getLogger(__name__)
    logger.info("Initiating form field population")
    
    try:
        elements = page.locator(Config.SEL_FORM_INPUTS)
        filled_count = 0
        
        for i, (field_name, field_value) in enumerate(zip(Config.FIELD_NAMES, Config.FORM_DATA)):
            if i < elements.count():
                try:
                    field = elements.nth(i)
                    field.click()
                    field.clear()
                    field.fill(field_value)
                    logger.debug(f"Field populated: {field_name}")
                    filled_count += 1
                except Exception as e:
                    logger.warning(f"Field population failed: {field_name} - {e}")
        
        logger.info(f"Form field population complete: {filled_count}/{len(Config.FORM_DATA)} fields")
        return filled_count
        
    except Exception as e:
        logger.error(f"Form field population failed: {e}")
        take_screenshot(page, "fill_error")
        return 0


def wait_for_upload_completion(page: Page, expected_files: int) -> bool:
    """Wait for upload completion with enterprise monitoring"""
    logger = logging.getLogger(__name__)
    logger.info("Monitoring upload progress")
    
    for wait_time in range(Config.UPLOAD_WAIT_MAX):
        try:
            # Monitor upload indicators
            progress_indicators = page.locator(Config.SEL_UPLOAD_PROGRESS).count()
            visible_files = page.locator(Config.SEL_FILE_NAMES).count()
            
            # Upload completion criteria
            if progress_indicators == 0 and visible_files >= expected_files:
                logger.info(f"Upload completion confirmed: {visible_files} files visible")
                page.wait_for_timeout(Config.WAIT_MEDIUM)
                return True
            
            page.wait_for_timeout(Config.WAIT_SHORT)
            
        except Exception:
            page.wait_for_timeout(Config.WAIT_SHORT)
    
    logger.warning(f"Upload completion timeout: {Config.UPLOAD_WAIT_MAX}s exceeded")
    return False


def upload_files(page: Page, files: List[str]) -> bool:
    """Upload files with enterprise retry logic"""
    logger = logging.getLogger(__name__)
    
    if not files:
        logger.warning("No files available for upload")
        return False
    
    logger.info(f"Initiating file upload: {len(files)} files")
    
    try:
        # Trigger file upload dialog
        page.locator(Config.SEL_ADD_FILE).first.click()
        page.wait_for_timeout(Config.WAIT_MEDIUM)
        
        # File input discovery with retry
        upload_success = False
        for attempt in range(Config.MAX_UPLOAD_RETRIES):
            for frame in page.frames:
                try:
                    inputs = frame.locator(Config.SEL_FILE_INPUT)
                    if inputs.count() > 0:
                        inputs.first.set_input_files(files)
                        logger.info("File upload initiated")
                        upload_success = True
                        break
                except Exception:
                    continue
            
            if upload_success:
                break
                
            if attempt < Config.MAX_UPLOAD_RETRIES - 1:
                page.wait_for_timeout(Config.WAIT_MEDIUM)
        
        # Fallback: Direct input method
        if not upload_success:
            inputs = page.locator(Config.SEL_FILE_INPUT)
            if inputs.count() > 0:
                inputs.first.set_input_files(files)
                logger.info("File upload initiated via direct method")
                upload_success = True
        
        if not upload_success:
            logger.error("File input discovery failed")
            return False
        
        # Wait for upload completion
        if wait_for_upload_completion(page, len(files)):
            logger.info("File upload operation successful")
            return True
        else:
            logger.warning("Upload completion timeout - proceeding")
            return True
            
    except Exception as e:
        logger.error(f"File upload operation failed: {e}")
        take_screenshot(page, "upload_error")
        return False


def validate_form(page: Page) -> bool:
    """Validate form with enterprise error reporting"""
    logger = logging.getLogger(__name__)
    logger.info("Initiating form validation")
    
    try:
        elements = page.locator(Config.SEL_FORM_INPUTS)
        
        for i, field_name in enumerate(Config.FIELD_NAMES):
            if i < elements.count():
                field_value = elements.nth(i).input_value()
                if not field_value or not field_value.strip():
                    logger.error(f"Validation failure: {field_name} field empty")
                    return False
                logger.debug(f"Validation passed: {field_name}")
        
        logger.info("Form validation successful")
        return True
        
    except Exception as e:
        logger.error(f"Form validation failed: {e}")
        return False


def is_form_submitted(page: Page) -> bool:
    """Check submission status with enterprise validation"""
    try:
        # Success message detection
        if page.locator(Config.SEL_SUCCESS).count() > 0:
            return True
        
        # URL change validation
        current_url = page.url.lower()
        if "viewform" not in current_url and "docs.google.com" in current_url:
            return True
        
        # Success message patterns
        for message in Config.SUCCESS_MESSAGES:
            if page.locator(f'text="{message}"').count() > 0:
                return True
        
        # Submit button state + completion indicators
        submit_count = page.locator(Config.SEL_SUBMIT).count()
        if submit_count == 0:
            completion_count = page.locator(Config.SEL_SUCCESS_INDICATORS).count()
            if completion_count > 0:
                return True
        
        # Error detection
        error_count = page.locator(Config.SEL_ERROR_INDICATORS).count()
        if error_count > 0:
            return False
        
        return False
        
    except Exception:
        return False


def submit_form(page: Page) -> bool:
    """Submit form with enterprise retry strategy"""
    logger = logging.getLogger(__name__)
    
    if not validate_form(page):
        return False
    
    logger.info("Initiating form submission")
    
    # Pre-submission wait
    logger.info("Ensuring upload completion before submission")
    page.wait_for_timeout(Config.WAIT_LONG)
    
    for attempt in range(Config.MAX_SUBMIT_RETRIES):
        try:
            logger.info(f"Submission attempt {attempt + 1}/{Config.MAX_SUBMIT_RETRIES}")
            
            # Remove overlays
            page.evaluate(Config.JS_REMOVE_OVERLAYS)
            page.wait_for_timeout(Config.WAIT_SHORT)
            
            # Submit button interaction
            submit_button = page.locator(Config.SEL_SUBMIT)
            if submit_button.count() > 0:
                logger.info("Executing submit button click")
                submit_button.click(force=True, timeout=Config.TIMEOUT_ELEMENT)
                page.wait_for_timeout(Config.WAIT_LONG)
                
                # Immediate success check
                if is_form_submitted(page):
                    logger.info("Form submission successful")
                    return True
            else:
                logger.warning("Submit button not found")
            
            # If captcha appears, wait and allow manual solve
            try:
                captcha_present = False
                # quick detection heuristics
                if page.locator('iframe[title*="captcha" i], iframe[src*="recaptcha" i], div.g-recaptcha').count() > 0:
                    captcha_present = True
                else:
                    for fr in page.frames:
                        if 'recaptcha' in (fr.url or '').lower():
                            captcha_present = True
                            break
                if captcha_present:
                    notify_user("Google Forms challenged the automation. Please solve the CAPTCHA in the open browser window.")
                    try:
                        page.bring_to_front()
                    except Exception:
                        pass
                    logger.warning("Captcha detected. Waiting for manual completion (up to 3 minutes)...")
                    waited = 0
                    step = 2000
                    while waited < Config.CAPTCHA_WAIT:
                        page.wait_for_timeout(step)
                        waited += step
                        # break early if submission succeeded
                        if is_form_submitted(page):
                            break
                        # or captcha elements disappeared
                        if page.locator('iframe[title*="captcha" i], iframe[src*="recaptcha" i], div.g-recaptcha').count() == 0:
                            break
            except Exception:
                pass

            # Post-submission verification
            for wait_attempt in range(3):
                page.wait_for_timeout(Config.WAIT_MEDIUM)
                if is_form_submitted(page):
                    logger.info("Form submission successful")
                    return True
            
            if attempt < Config.MAX_SUBMIT_RETRIES - 1:
                logger.warning(f"Submission attempt {attempt + 1} failed - retrying")
                
        except Exception as e:
            logger.error(f"Submission attempt {attempt + 1} failed: {e}")
            if is_form_submitted(page):
                logger.info("Form submission successful (despite error)")
                return True
            
            if attempt == Config.MAX_SUBMIT_RETRIES - 1:
                take_screenshot(page, "submit_failed")
    
    logger.error("Form submission failed after all retry attempts")
    return False


# ==================== Main Function ====================
def main() -> None:
    """Enterprise automation orchestration"""
    logger = logging.getLogger(__name__)
    setup_logging()
    
    try:
        with sync_playwright() as playwright:
            context = playwright.chromium.launch_persistent_context(
                user_data_dir=str(Config.BROWSER_DATA_DIR),
                headless=False,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            page = context.new_page()
            
            # Automation workflow
            if load_form(page):
                if clear_form(page):
                    logger.info("Form clear operation successful")
                    
                    filled_count = fill_form_fields(page)
                    
                    if filled_count == len(Config.FORM_DATA):
                        files = get_files_from_folder()
                        
                        if files and upload_files(page, files):
                            if submit_form(page):
                                logger.info("AUTOMATION COMPLETED SUCCESSFULLY")
                            else:
                                logger.error("Form submission failed")
                        else:
                            logger.error("File upload operation failed")
                    else:
                        logger.error(f"Form population incomplete: {filled_count}/{len(Config.FORM_DATA)} fields")
                else:
                    logger.error("Form clear operation failed")
            
            # Resource cleanup
            if Config.KEEP_BROWSER_OPEN:
                logger.info("Browser session maintained for inspection")
            else:
                context.close()
                logger.info("Browser session terminated")
            
    except Exception as e:
        logger.error(f"Automation execution failed: {e}", exc_info=True)
    
    finally:
        logger.info("=" * 60)
        logger.info("Automation process completed")
        if Config.KEEP_BROWSER_OPEN:
            logger.info("Browser remains active for manual inspection")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()