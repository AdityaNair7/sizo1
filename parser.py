from bs4 import BeautifulSoup

def get_products(html):

    soup = BeautifulSoup(html, "lxml")

    products = []

    # Find every product card
    cards = soup.find_all("div")

    for card in cards:

        text = card.get_text(" ", strip=True)

        if "₹" not in text:
            continue

        products.append({
            "text": text
        })

    return products
