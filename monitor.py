from playwright.sync_api import sync_playwright

URL = "https://www.lenovo.com/in/outletin/en/laptops/"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-dev-shm-usage"]
    )

    page = browser.new_page()

    print("Opening Lenovo...")

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=120000
    )

    print("Waiting for JavaScript...")

    page.wait_for_timeout(20000)

    html = page.content()

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Saved output.html")

    browser.close()
