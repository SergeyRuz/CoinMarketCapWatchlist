import asyncio
import httpx
from scrapers.scrapers import Scraper
from lxml import html
import json

class JSONScraper(Scraper):

    async def fetch_page(self, client, page_num):
        """Fetch a single page."""
        url = f"{self.url}?page={page_num}"
        response = await client.get(url)
        tree = html.fromstring(response.text)
        script_content = tree.xpath('//script[@id="__NEXT_DATA__"]/text()')[0]
        data = json.loads(script_content)
        crypto_list = data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["data"]["listing"]["cryptoCurrencyList"]
        return crypto_list  

    async def fetch(self):
        """Fetch pages in parallel, repeat for self.loops times, flatten the result."""
        all_coins = []  
        async with httpx.AsyncClient() as client:
            for _ in range(self.loops):
                tasks = [self.fetch_page(client, i) for i in range(1, self.pages+1)]  # pages 1 to 5
                pages = await asyncio.gather(*tasks)  
                for page in pages:
                    all_coins.extend(page)  
        return all_coins  

    def parse(self, coins):
        """Parse all collected coins."""
        for coin in coins:
            self.results.append({
                'Rank': coin['cmcRank'],
                'Name': coin['name'],
                'Symbol': coin['symbol'],
                'Price (USD)': round(next((item['price'] for item in coin['quotes'] if item.get('name') == 'USD'), None), 2),
                '24h % Change': round(next((item['percentChange24h'] for item in coin['quotes'] if item.get('name') == 'USD'), None), 2),
                'Market Cap (USD)': round(next((item['marketCap'] for item in coin['quotes'] if item.get('name') == 'USD'), None), 2)
            })

