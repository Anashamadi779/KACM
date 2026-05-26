"""
STEP 1 - scrape_kacm.py
Scrapes KACM data from Wikipedia + other sources and saves to kacm_data.json
Run: python scrape_kacm.py
"""

import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; KACMBot/1.0)"}

def scrape_wikipedia(url: str, label: str) -> list[dict]:
    """Scrape paragraphs from a Wikipedia page."""
    chunks = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return chunks
        paragraphs = content_div.find_all("p")
        for p in paragraphs:
            text = p.get_text(separator=" ", strip=True)
            if len(text) > 80:  # skip short/empty paragraphs
                chunks.append({"source": url, "label": label, "text": text})
    except Exception as e:
        print(f"  [!] Failed to scrape {url}: {e}")
    return chunks


def scrape_transfermarkt(url: str, label: str) -> list[dict]:
    """Scrape squad/info table from Transfermarkt."""
    chunks = []
    try:
        headers = {**HEADERS, "Accept-Language": "en-US,en;q=0.9"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        # Grab all visible text blocks
        for tag in soup.find_all(["p", "td", "h2", "h3"]):
            text = tag.get_text(separator=" ", strip=True)
            if len(text) > 60:
                chunks.append({"source": url, "label": label, "text": text})
    except Exception as e:
        print(f"  [!] Failed to scrape {url}: {e}")
    return chunks


# ── Static facts (always reliable even if scraping fails) ─────────────────────
STATIC_FACTS = [
    "Kawkab Athletic Club Marrakech, commonly known as KACM, is a Moroccan football club based in Marrakech.",
    "KACM was founded in 1946 and plays in the Botola Pro, the top division of Moroccan football.",
    "The club's full name is Kawkab Athletic Club Marrakech. KACM stands for Kawkab Athletic Club Marrakech.",
    "KACM plays their home matches at the Stade El Harti in Marrakech, Morocco.",
    "The club's colors are green and white.",
    "KACM has won the Botola Pro title once, in the 1996–97 season.",
    "The club has also won the Coupe du Trône (Moroccan Cup) multiple times.",
    "KACM is one of the historic clubs of Moroccan football, representing the city of Marrakech.",
    "The club's nickname is 'Al Kawkab' which means 'The Star' in Arabic.",
    "KACM competes in the Botola Pro Inwi, the first division of the Moroccan football league system.",
    "Marrakech is located in the Marrakech-Safi region of Morocco, and KACM is the city's main football club.",
    "KACM's stadium, Stade El Harti, has a capacity of approximately 12,000 spectators.",
    "The club was founded in 1946, making it one of the older football clubs in Morocco.",
    "KACM has had several notable players over the years who have also represented the Moroccan national team.",
    "The club's main rivals are other Moroccan clubs competing in the Botola Pro league.",
    "KACM's greatest achievement was winning the national championship title in 1996-97.",
    "The green and white colors of KACM represent the club's identity in Moroccan football.",
    "KACM's fans are known as passionate supporters of Marrakech football.",
    "The club participates annually in Moroccan football competitions including the league and the cup.",
    "KACM has experienced promotions and relegations throughout its history in Moroccan football.",
]


def main():
    all_chunks = []

    # ── Add static facts first ────────────────────────────────────────────────
    print("✅ Adding static facts...")
    for fact in STATIC_FACTS:
        all_chunks.append({
            "source": "static",
            "label": "KACM General Facts",
            "text": fact
        })

    # ── Scrape Wikipedia ──────────────────────────────────────────────────────
    sources = [
        ("https://en.wikipedia.org/wiki/Kawkab_Athletic_Club_Marrakech", "KACM Wikipedia EN"),
        ("https://fr.wikipedia.org/wiki/Kawkab_Athletic_Club_de_Marrakech", "KACM Wikipedia FR"),
        ("https://en.wikipedia.org/wiki/Botola", "Botola Pro Wikipedia"),
        ("https://en.wikipedia.org/wiki/Stade_El_Harti", "Stade El Harti Wikipedia"),
        ("https://www.transfermarkt.fr/kawkab-marrakech/erfolge/verein/4697#google_vignette", "Transfermarkt")
    ]

    for url, label in sources:
        print(f"🌐 Scraping: {label}")
        chunks = scrape_wikipedia(url, label)
        print(f"   → {len(chunks)} chunks found")
        all_chunks.extend(chunks)
        time.sleep(1)  # be polite to Wikipedia

    # ── Save to JSON ──────────────────────────────────────────────────────────
    output = {"total": len(all_chunks), "chunks": all_chunks}
    with open("kacm_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! Saved {len(all_chunks)} text chunks to kacm_data.json")


if __name__ == "__main__":
    main()
