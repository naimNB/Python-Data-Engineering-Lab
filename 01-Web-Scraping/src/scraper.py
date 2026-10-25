from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin


import requests
from bs4 import BeautifulSoup


# Configure retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

# Create session with retry support
session = requests.Session()

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)


base_url = "https://books.toscrape.com/catalogue/page-{}.html"

all_books = []


for page in range(1, 6):
    url = base_url.format(page)

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        if not books:
            print(f"Warning: No books found on page {page}")
            continue


        for book in books:
            link = book.find("h3").find("a")

            title = link["title"]

            price_text = book.find(
                "p", class_="price_color"
            ).get_text(strip=True)

            price = float(price_text.replace("£", ""))

            availability = book.find(
                "p", class_="instock availability"
            ).get_text(strip=True)

            rating_tag = book.find("p", class_="star-rating")
            rating = next(
                (r for r in ["One", "Two", "Three", "Four", "Five"]
                if r in rating_tag.get("class", [])),
                "Unknown"
            )

            product_url = urljoin(url, link["href"])

            all_books.append({
                "title": title,
                "price": price,
                "currency": "GBP",
                "availability": availability,
                "rating": rating,
                "page": page,
                "product_url": product_url
            })


        print(f"Page {page}: {len(books)} books collected")

    except requests.exceptions.RequestException as error:
        print(f"Error scraping page {page}: {error}")
        continue

print("-" * 40)
print("Total Books Collected:", len(all_books))



import pandas as pd
from pathlib import Path

# Locate the project directory
project_dir = Path(__file__).resolve().parent.parent

# Create data directory if missing
data_dir = project_dir / "data"
data_dir.mkdir(parents=True, exist_ok=True)

# Convert collected records into a DataFrame
df = pd.DataFrame(all_books)


# Validate collected records
required_columns = ["title", "price", "page"]

if len(df) < 100:
    raise ValueError(
        f"Insufficient records: Expected at least 100, got {len(df)}"
    )

if df[required_columns].isnull().any().any():
    raise ValueError("Dataset contains missing values!")

if df["title"].duplicated().any():
    raise ValueError("Dataset contains duplicate book titles!")

print("Data validation passed!")


# Export records
df.to_csv(data_dir / "books.csv", index=False, encoding="utf-8-sig")
df.to_json(
    data_dir / "books.json",
    orient="records",
    indent=4,
    force_ascii=False
)

print("CSV and JSON files saved successfully!")
print("Dataset Shape:", df.shape)
