import logging
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Constants
OUTPUT_FILENAME = "full_context.md"
TIMEOUT_SECONDS = 30
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

URLS: List[str] = [
    "https://dev.predict.fun/faqs-684248m0.md",
    "https://dev.predict.fun/-deployed-contracts-1860295m0.md",
    "https://dev.predict.fun/understanding-the-orderbook-685654m0.md",
    "https://dev.predict.fun/ts-how-to-authenticate-your-api-requests-663127m0.md",
    "https://dev.predict.fun/py-how-to-authenticate-your-api-requests-1868364m0.md",
    "https://dev.predict.fun/how-to-create-or-cancel-orders-679306m0.md",
    "https://dev.predict.fun/general-information-1915499m0.md",
    "https://dev.predict.fun/request-format-1915501m0.md",
    "https://dev.predict.fun/response-format-1915502m0.md",
    "https://dev.predict.fun/subscription-topics-1915507m0.md",
    "https://dev.predict.fun/heartbeats-1915508m0.md",
    "https://dev.predict.fun/client-example-1915523m0.md",
    "https://dev.predict.fun/get-auth-message-25326899e0.md",
    "https://dev.predict.fun/get-jwt-with-valid-signature-25326900e0.md",
    "https://dev.predict.fun/get-categories-25326910e0.md",
    "https://dev.predict.fun/get-category-by-slug-25326911e0.md",
    "https://dev.predict.fun/get-all-tags-27399809e0.md",
    "https://dev.predict.fun/get-markets-25326905e0.md",
    "https://dev.predict.fun/get-market-by-id-25552989e0.md",
    "https://dev.predict.fun/get-market-statistics-25326906e0.md",
    "https://dev.predict.fun/get-market-last-sale-information-25326907e0.md",
    "https://dev.predict.fun/get-the-orderbook-for-a-market-25326908e0.md",
    "https://dev.predict.fun/get-order-by-hash-25326901e0.md",
    "https://dev.predict.fun/get-orders-25326902e0.md",
    "https://dev.predict.fun/get-order-match-events-25663812e0.md",
    "https://dev.predict.fun/create-an-order-25326903e0.md",
    "https://dev.predict.fun/remove-orders-from-the-orderbook-25326904e0.md",
    "https://dev.predict.fun/get-connected-account-25326917e0.md",
    "https://dev.predict.fun/get-account-activity-26651508e0.md",
    "https://dev.predict.fun/set-a-referral-25326918e0.md",
    "https://dev.predict.fun/get-positions-25326909e0.md",
    "https://dev.predict.fun/get-positions-by-address-27399808e0.md",
    "https://dev.predict.fun/search-categories-and-markets-27399810e0.md",
    "https://dev.predict.fun/finalize-a-oauth-connection-25326912e0.md",
    "https://dev.predict.fun/get-the-orders-for-a-oauth-connection-25326913e0.md",
    "https://dev.predict.fun/create-an-order-for-a-oauth-connection-25326914e0.md",
    "https://dev.predict.fun/cancel-the-orders-for-a-oauth-connection-25326915e0.md",
    "https://dev.predict.fun/get-the-positions-for-a-oauth-connection-25326916e0.md",
]


def scrape_docs():
    """Scrapes documentation from predefined URLs and saves to a single Markdown file."""
    logger.info("🔥 Начинаю сборку контекста для вайбкодинга...")

    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        f.write("# PREDICT.FUN API DOCUMENTATION (FULL CONTEXT)\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for url in URLS:
            try:
                # Увеличенный таймаут
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)

                if response.status_code == 200:
                    text: str = ""
                    # Если это Markdown файл (по расширению или контенту), берем текст как есть
                    if url.endswith(".md") or response.text.lstrip().startswith("#"):
                        text = response.text
                    else:
                        # Fallback для HTML (если вдруг что-то изменится)
                        soup = BeautifulSoup(response.text, "html.parser")
                        content = (
                            soup.find("article")
                            or soup.find("main")
                            or soup.find("div", class_="content")
                            or soup.body
                        )
                        text = (
                            md(str(content), heading_style="ATX") if content else ""
                        )

                    # Записываем в файл
                    f.write(f"\n\n---\n\n# SOURCE: {url}\n\n")
                    f.write(text)
                    logger.info(f"✅ Скачано: {url.split('/')[-1]}")
                else:
                    logger.error(f"❌ Ошибка {response.status_code}: {url}")
            except Exception as e:
                logger.error(f"❌ Сбой при обработке {url}: {e}")

    logger.info(
        f"\n🚀 Готово! Файл {OUTPUT_FILENAME} создан. Можно грузить в LLM."
    )


if __name__ == "__main__":
    scrape_docs()
