import requests
from bs4 import BeautifulSoup

url = "https://www.transfermarkt.fr/kawkab-marrakech/erfolge/verein/4697#google_vignette"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title)