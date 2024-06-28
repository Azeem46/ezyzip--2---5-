from playwright.sync_api import Playwright, sync_playwright
from urllib.parse import parse_qs, quote, urlparse
import pyotp
import requests
from Config import *

rurlEncode = quote(RURL, safe="")

AUTH_URL = f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={API_KEY}&redirect_uri={rurlEncode}'

def getAccessToken(code):
    url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json', 
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'code': code,
        'client_id': API_KEY,
        'client_secret': SECRET_KEY,
        'redirect_uri': RURL,
        'grant_type': 'authorization_code',
    }
    response = requests.post(url, headers=headers, data=data)
    json_response = response.json()
    print(json_response)
def run(playwright: Playwright) -> str:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    with page.expect_request(f"**{RURL}?code=**") as request:
         page.goto(AUTH_URL)
         page.locator("#mobileNum").click()
         page.locator("#mobileNum").fill(MOBILE_NO)
         page.get_by_role("button", name="Get OTP").click()
         page.locator("#otpNum").click()
         otp = pyotp.TOTP(TOTP_KEY).now()
         page.locator("#otpNum").fill(otp)
         page.get_by_role("button", name="Continue").click()
         page.get_by_label("Enter 6-digit PIN").click()
         page.get_by_label("Enter 6-digit PIN").fill(PIN)
         res = page.get_by_role("button", name="Continue").click()
         page.wait_for_load_state()
    url=request.value.url
    print(f"Redirect Url with code :{url}")
    parsed=urlparse(url)
    code=parse_qs(parsed.query)['code'][0]
    context.close()
    browser.close()
    return code
    
with sync_playwright() as playwright:
    code=run(playwright)

getAccessToken(code)


 