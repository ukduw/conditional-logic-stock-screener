from pathlib import Path
from playwright.sync_api import sync_playwright

from dotenv import load_dotenv
import os

STATE_FILE = "auth_state.json"

URL = "https://www.etf.com/etfanalytics/etf-screener"
LOGIN_URL = "https://www.etf.com/etf/login#block--login"

load_dotenv()
EMAIL = os.environ.get("EMAIL")
PASS = os.environ.get("PASSWORD")


def is_logged_in(page):
    try:
        page.click("class=avatar-button")
        return page.locator("text=Sign Out").count() > 0
    except:
        return False

def login(page):
    page.goto(LOGIN_URL)

    page.get_by_placeholder("Enter your email").nth(1).fill(EMAIL)
    page.get_by_placeholder("Enter your password").nth(1).fill(PASS)
    page.get_by_role("button", name="Sign in").click()

    page.wait_for_load_state("networkidle")

    if not is_logged_in(page):
        raise Exception("Login failed")

def get_auth_context(browser):
    if Path(STATE_FILE).exists():
        context = browser.new_context(storage_state=STATE_FILE)

        page = context.new_page()
        page.goto(URL)

        if is_logged_in(page):
            page.close()
            return context
        
        context.close()


    context = browser.new_context()
    page = context.new_page()

    login(page)
    context.storage_state(path=STATE_FILE)
    page.close()


    return context



def get_etfs_from_etfcom():
    filtered_etfs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = get_auth_context(browser)

        page = context.new_page()
        page.goto(URL)

        page.click("text=Select Filters")
        page.click("text=Saved Screeners")
        page.click("text=activeus1mvol")
        page.click("text=Apply Filters")
        page.click("text=100")
        page.wait_for_load_state("networkidle")

        rows = page.locator("table tbody tr")
        for i in range(rows.count()):
            symbol = rows.nth(i).locator("td").all_inner_texts()
            print(symbol)
            filtered_etfs.append(symbol)


        page.click("text=Next")
        page.wait_for_load_state("networkidle")

        rows = page.locator("table tbody tr")
        for i in range(rows.count()):
            symbol = rows.nth(i).locator("td").all_inner_texts()
            print(symbol)
            filtered_etfs.append(symbol)

    print(filtered_etfs)
    return filtered_etfs


#get_etfs_from_etfcom()