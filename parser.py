from bs4 import BeautifulSoup

def get_products(html):

    soup = BeautifulSoup(html, "lxml")

    products = []

    cards = soup.select("div.price-stack")

    for card in cards:

        text = card.get_text(" ", strip=True)

        products.append({
            "text": text
        })

    return products
