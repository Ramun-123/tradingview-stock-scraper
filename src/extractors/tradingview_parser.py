import logging
import requests
from bs4 import BeautifulSoup
from .utils_format import clean_text

class TradingViewParser:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def fetch_html(self, url: str):
        response = self.session.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.text

    def parse(self, url: str):
        html = self.fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")

        def safe_select(selector, attr=None):
            element = soup.select_one(selector)
            if not element:
                return None
            return clean_text(element.get(attr) if attr else element.text)

        data = {
            "url": url,
            "symbol": safe_select("span.tv-symbol-header__second-line"),
            "logoUrl": safe_select("img.tv-profile__logo", "src"),
            "ticker": safe_select("h1.tv-symbol-header__name"),
            "description": safe_select("div.tv-profile__description"),
            "price": safe_select("div.tv-symbol-price-quote__value"),
            "change": safe_select("span.tv-symbol-price-quote__change-value"),
            "volume": safe_select("span.tv-widget-field--volume"),
            "volumeChange": safe_select("span.tv-widget-field--volume-change"),
            "marketCapitalization": safe_select("span.tv-widget-field--marketCap"),
            "priceToEarningsRatio": safe_select("span.tv-widget-field--peRatio"),
            "earningsPerShareDiluted": safe_select("span.tv-widget-field--eps"),
            "sector": safe_select("span.tv-widget-field--sector"),
            "news": []
        }

        news_items = soup.select("div.tv-feed__item")
        for item in news_items:
            title_el = item.select_one("a")
            if title_el:
                data["news"].append({
                    "url": clean_text(title_el.get("href")),
                    "title": clean_text(title_el.text),
                    "published": clean_text(item.select_one("time").text if item.select_one("time") else "")
                })

        logging.info(f"Parsed data for {url}")
        return data