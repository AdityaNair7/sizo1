from playwright.sync_api import sync_playwright

URL = "https://www.lenovo.com/in/outletin/en/laptops/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(URL, wait_until="networkidle", timeout=120000)

    page.wait_for_timeout(10000)

    html = page.content()

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Page downloaded successfully.")

    browser.close()
