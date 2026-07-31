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

    print("Opening Lenovo Outlet...")

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=120000
    )

    page.wait_for_timeout(10000)

    previous_count = 0

    while True:

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)

        cards = page.locator("div.price-stack")
        current_count = cards.count()

        print(f"Current cards: {current_count}")

        if current_count == previous_count:
            print("No new cards detected.")
        else:
            previous_count = current_count

        button = page.locator("text=Load more results")

        if button.count() == 0:
            print("Load More button not found.")
            break

        try:
            button.first.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)

            if button.first.is_visible():
                print("Clicking Load More...")
                button.first.click(force=True)
                page.wait_for_timeout(6000)
            else:
                print("Button not visible.")
                break

        except Exception as e:
            print("Finished loading.")
            print(e)
            break

    html = page.content()

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

    products = get_products(html)

    print("\n")
    print("=" * 80)
    print("Products found:", len(products))
    print("=" * 80)

    for i, product in enumerate(products, start=1):
        print(f"\nPRODUCT {i}")
        print("-" * 80)
        print(product["text"][:700])

    browser.close()
