from playwright.sync_api import sync_playwright
from parser import get_products

URL = "https://www.lenovo.com/in/outletin/en/laptops/"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=["--disable-dev-shm-usage"]
    )

    page = browser.new_page(
        viewport={"width": 1600, "height": 900}
    )

    page.goto(URL, wait_until="domcontentloaded")

    page.wait_for_timeout(10000)

    while True:
        try:
            button = page.locator("text=Load more results")

            if button.count() == 0:
                break

            if not button.is_visible():
                break

            button.click()

            page.wait_for_timeout(3000)

        except Exception:
            break

    html = page.content()

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

    products = get_products(html)

    print("Products found:", len(products))

    for product in products[:10]:
        print("=" * 80)
        print(product["text"][:500])

    browser.close()
