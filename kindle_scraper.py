from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os

def get_highlights(email, password):
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    # Navigate to the webpage
    driver.get('https://read.amazon.in/kp/notebook')

    # Login to the webpage
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ap_email"]'))).send_keys(email)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ap_password"]'))).send_keys(password, Keys.ENTER)

    # Wait for the page to load
    WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "library-section")))

    # Retrieve the books
    books = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'kp-notebook-library-each-book')]")))

    book_highlights = {}
    for book in books:
        # Extract the book details
        title = book.text.splitlines()[0]
        author = book.text.splitlines()[1][4:]
        
        # Click the book
        book.click()

        # Wait for the page to load
        WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@id, 'highlight')]")))

        # Extract the highlights
        highlights = book.find_elements(By.XPATH, "//span[@id='highlight' or @id='note']")
        highlight_text = [(highlight.text, "highlight") if highlight.get_attribute("id") == "highlight" else (highlight.text, "note") for highlight in highlights if highlight.text != ""]

        # Store the book highlights
        book_highlights[title] = {
            "highlights": highlight_text```