from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
import json
import re


def driver_init():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=options)
    driver.get('https://www.google.com/?gl=us&hl=en&gws_rd=cr&pws=0')

    def check_jsaction():
        try:
            body_locator = (By.XPATH, "//body[@jsaction]")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(body_locator))
            print("The jsaction attribute exists in the <body> tag")
            return True
        except TimeoutException:
            print("The jsaction attribute NOT exists in the <body> tag")
            return False

    if check_jsaction():
        return driver

    try:
        element_locator = (By.XPATH, "//div[text()='Reject all']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator)).click()
    except TimeoutException:
        input("init could not find Reject div")

    if check_jsaction():
        return driver

    raise Exception("The jsaction attribute still does not exist in the <body> tag after clicking 'Reject all'!")


def driver_search(driver, query):
    driver.get(query)


def driver_extract_links(driver):
    page_source = driver.page_source
    pattern = r'\["(https?:\/\/[^"]+)",\d+,\d+\]'
    matches = re.findall(pattern, page_source)

    original_image_urls = []
    for match in matches:
        decoded_url = json.loads(f'"{match}"')
        if 'gstatic.com' not in decoded_url:
            original_image_urls.append(decoded_url)

    return original_image_urls


def wait_for_script_tag(driver, timeout=10):
    element_locator = (By.CSS_SELECTOR, "script#_ij")
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_locator))
