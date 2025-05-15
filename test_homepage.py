import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# Constants
BASE_URL = "https://www.selenium.dev/"
WAIT_TIMEOUT = 10


# Fixtures before test runs
@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        yield driver
    finally:
        driver.quit()


def test_page_content(browser):
    browser.get(BASE_URL)

    # Content verification
    content_to_check = [
        ('title', 'Selenium'),
        ('source', 'News'),
        ('source', 'Selenium automates browsers.'),
        ('source', 'Tune in for the Selenium Community Live scheduled for May 21st, 2025.'),
        ('source', 'Getting Started'),
        ('source', 'Development Partners'),
        ('source', 'Selenium Level Sponsors')
    ]

    for i, content in content_to_check:
        if i == 'title':
            assert content in browser.title
        else:
            try:
                assert content in browser.page_source
            except AssertionError:
                with open("sourceCheckerError.txt", "w", encoding="utf-8") as f:
                    f.write(browser.page_source)
                raise AssertionError(f"Content '{content}' not found in page source")


def test_navigation_links(browser):
    browser.get(BASE_URL)

    navigation_links = [
        'a.nav-link[href="/downloads"]',
        'a.nav-link[href="/documentation"]',
        'a.nav-link[href="/projects"]',
        'a.nav-link[href="/support"]',
        'a.nav-link[href="/blog"]'
    ]

    for link_selector in navigation_links:
        WebDriverWait(browser, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, link_selector))
        ).click()
        time.sleep(2)  # verify page has been reached and viewable
        browser.back()
        time.sleep(1)  # Brief pause to ensure page stability


def test_about_dropdown(browser):
    browser.get(BASE_URL)

    about_items = [
        'About Selenium',
        'Structure and Governance',
        'Ecosystem',
        'History',
        'Get Involved',
        'Sponsors',
        'Sponsor Us'
    ]

    for item in about_items:
        WebDriverWait(browser, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "navbarDropdown"))
        ).click()

        WebDriverWait(browser, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, item))
        ).click()
        browser.back()


def test_homepage_links(browser):
    browser.get(BASE_URL)

    main_links = [
        'a[href="/documentation/webdriver/"]',
        'a[href="https://selenium.dev/selenium-ide/"]',
        'a[href="/documentation/grid/"]'
    ]

    for link_selector in main_links:
        try:
            element = WebDriverWait(browser, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, link_selector))
            )
            element.click()

            # Page interaction
            browser.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            browser.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
            browser.get(BASE_URL)

        except NoSuchElementException as e:
            print(f"Element not found: {link_selector}")
            with open("homepage_links.txt", "w", encoding="utf-8") as f:
                f.write(link_selector)
            continue

    # Partner and sponsor links
    partner_links = [
        'a[href*="browserstack.com"]',
        'a[href*="saucelabs.com"]',
        'a[href*="lambdatest.com/selenium-automation"]'
    ]

    sponsor_links = [
        'a[href*="brightdata.com"]',
        'a[href*="applitools.com"]'
    ]

    for link_selector in partner_links + sponsor_links:
        try:
            element = WebDriverWait(browser, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, link_selector))
            )
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            element.click()
            time.sleep(2)
            browser.get(BASE_URL)
        except NoSuchElementException as e:
            print(f"Partner/Sponsor link not found: {link_selector}")
            with open("links_error.txt", "w", encoding="utf-8") as f:
                f.write(link_selector)  # match this with link you are looking for, could be DOM issue


            # prev issue: Fixed browser didn't have enough time to locate the elements - so it was not clickable


