from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    for browser_type in [p.chromium,p.firefox,p.webkit]:    
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto("http://playwright.dev")
        page.screenshot(path=f'example-{browser_type.name}.png')
        browser.close()


import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://login.upstox.com/login/v2/oauth/authorize?redirect_uri=https://api-v2.upstox.com/login/authorization/redirect&response_type=code&client_id=IND-nyjv70u9xcg2t8e3hkrpdm5b&user_id=4oK5R9iqbsD89AxVfB3amw&user_type=individual")
    page.goto("https://login.upstox.com/")
    page.locator("#mobileNum").click()
    page.locator("#mobileNum").fill("7620295908")
    page.get_by_role("button",name="Get OTP").click()
    page.locator("#otpNum").fill("262-801")
    page.get_by_role("button",name="Continue").click()
    page.get_by_label("Enter 6-digit PIN").fill("154605")
    page.get_by_role("button",name="Continue").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

