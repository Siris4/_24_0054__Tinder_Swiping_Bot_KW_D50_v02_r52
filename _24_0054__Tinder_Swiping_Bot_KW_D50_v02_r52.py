from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

# Constants
EMAIL = "YOUR_EMAIL"

# Function to log messages
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{timestamp} - {message}")

def click_big_main_login_button(driver):
    try:
        big_main_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.l17p5q9z"))
        )
        big_main_login_button.click()
        log_message("big main login button clicked successfully using CSS Selector.")
        # after successful click, attempt to press the english button again if needed:
        click_english_option(driver)
        click_additional_login_button(driver)  # new step added
    except TimeoutException:
        log_message("Attempt with CSS Selector failed. Trying XPath.")
    try:
        big_main_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'c1p6lbu0') and .//div[contains(text(), 'Log in')]]"))
        )
        big_main_login_button.click()
        log_message("big main login button clicked successfully using XPath.")
        # after successful click, attempt to press the english button again if needed:
        click_english_option(driver)
        click_additional_login_button(driver)  # new step added
    except TimeoutException:
        log_message("Attempt with XPath failed. Trying class name.")
    try:
        big_main_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "l17p5q9z"))
        )
        big_main_login_button.click()
        log_message("big main login button clicked successfully using Class Name.")
        # after successful click, attempt to press the english button again if needed:
        click_english_option(driver)
        click_additional_login_button(driver)  # new step added
    except TimeoutException:
        log_message("All attempts to click the big main login button have failed.")

def click_english_option(driver):
    try:
        english_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'English')]"))
        )
        english_option.click()
        log_message("Selected English from the selection.")
    except TimeoutException:
        log_message("English option not found or not clickable; might not be needed at this moment.")

def click_additional_login_button(driver):
    try:
        additional_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='c1p6lbu0 Miw(120px)'] div[class='l17p5q9z']"))
        )
        additional_login_button.click()
        log_message("Additional login button clicked successfully.")
    except TimeoutException:
        log_message("Failed to click on the additional login button.")

def find_decline_button(driver):
    try:
        decline_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'l17p5q9z') and contains(text(), 'I decline')]"))
        )
        decline_button.click()
        log_message("Decline button clicked.")
        click_english_option(driver)
        click_additional_login_button(driver)
        click_big_main_login_button(driver)
        return True
    except TimeoutException:
        log_message("Decline button not found within 3 seconds.")
        return False

def click_login_button(driver):
    try:
        login_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Log in')]"))
        )
        login_button.click()
        log_message("Login button clicked.")
    except TimeoutException:
        log_message(f"Error clicking login button: {e}")

def click_login_button_2(driver):
    try:
        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log in')]/ancestor::a"))
        )
        login_button.click()
        log_message("Backup login button clicked.")
    except TimeoutException:
        log_message(f"Error clicking backup login button: {e}")

def continue_with_google_login_spanish_then_english(attempts=2):
    while attempts > 0:
        try:
            continue_with_google_spanish = WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'nsm7Bb-HzV7m-LgbsSe-BPrWId') and contains(text(), 'Continuar con Google')]"))
            )
            continue_with_google_spanish.click()
            log_message("Clicked on 'Continuar con Google' button successfully.")
            break
        except TimeoutException:
            log_message("'Continuar con Google' button not found, attempting in English.")
            try:
                continue_with_google = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.nsm7Bb-HzV7m-LgbsSe-BPrWId"))
                )
                continue_with_google.click()
                log_message("Clicked on 'Continue with Google' button successfully.")
                break
            except TimeoutException as e:
                log_message(f"Error clicking 'Continue with Google' button: {e}")
                attempts -= 1
                if attempts <= 0:
                    log_message("Failed to click on Google login button after multiple attempts, trying Login button.")
                    click_login_button(driver)
                else:
                    log_message("Retrying Google login after clicking on Login button.")
                    time.sleep(2)

chrome_options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
log_message("WebDriver initialized.")
driver.get("https://tinder.com/")
log_message("Navigated to Tinder's login page.")
if find_decline_button(driver):
    click_additional_login_button(driver)  # Ensuring the additional login button is clicked before Google login
    continue_with_google_login_spanish_then_english()

try:
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    log_message("Confirmed page is fully loaded and ready for email interaction.")
except TimeoutException:
    log_message("Page did not load within expected time.")

try:
    email_input_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    email_input_field.clear()
    email_input_field.send_keys(EMAIL + Keys.ENTER)
    log_message("Directly typed in the email and sent the Enter key.")
except TimeoutException:
    log_message("Failed to directly type in the email within the timeout period.")

input("Press Enter to exit...\n")
# driver.quit()
