import asyncio
import os
import httpx


class CoinGeckoClient:
    async def fetch(self):
        max_concurrent = int(os.environ.get("MAX_CONCURRENT", 2))
        total_pages = int(os.environ.get("TOTAL_PAGES", 3))
        per_page = int(os.environ.get("PER_PAGE", 50))

        semaphore = asyncio.Semaphore(max_concurrent)
        async with httpx.AsyncClient(timeout=10) as client:
            tasks = [self._fetch_page(client, semaphore, page, per_page) for page in range(1, total_pages + 1)]
            pages = await asyncio.gather(*tasks)
            

        return [coin for page in pages for coin in page]

    async def _fetch_page(self, client, semaphore, page, per_page):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "page": page,
            "per_page": per_page,
        }
        async with semaphore:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.TimeoutException:
                raise RuntimeError(f"CoinGecko request timed out on page {page}")
            except httpx.HTTPError as e:
                raise RuntimeError(f"CoinGecko request failed on page {page}: {e}")
