import asyncio
from playwright.async_api import async_playwright
from scrapers.scrapers import Scraper
from lxml import html
from tenacity import retry, stop_after_attempt, wait_fixed

class HTMLScraper(Scraper):

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def safe_goto(self, page, url):
        """Navigate to URL with retry logic using @retry."""
        await page.goto(url, timeout=60000)

    async def fetch(self):
        """Fetch pages in parallel, repeat for self.loops times, flatten the result."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            all_pages = []
            for _ in range(self.loops):
                async def fetch_single_page(page_number):
                    page = await context.new_page()
                    url = f"{self.url}?page={page_number}"
                    await self.safe_goto(page, url)
                    await self.auto_scroll(page)
                    content = await page.content()
                    await page.close()
                    return content
                tasks = [fetch_single_page(i) for i in range(1, self.pages+1)]
                pages = await asyncio.gather(*tasks)
                all_pages.extend(pages)  
            await browser.close()
        return all_pages

    async def auto_scroll(self, page):
        """Auto-scroll page to load dynamic content."""
        await page.evaluate("""
            async () => {
                const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
                for (let i = 0; i < document.body.scrollHeight; i += window.innerHeight / 2) {
                    window.scrollBy(0, window.innerHeight / 2);
                    await delay(200);
                }
            }
        """)

    def parse(self, pages):
        """Parse all collected pages."""
        for page_content in pages:
            tree = html.fromstring(page_content)
            rows = tree.xpath('//tbody/tr')

            for row in rows:
                try:
                    rank_list = row.xpath('.//td[2]//text()')
                    name_list = row.xpath('.//td[3]//*[contains(@class, "coin-item-name")]/text()')
                    symbol_list = row.xpath('.//td[3]//*[contains(@class, "coin-item-symbol")]/text()')
                    price_list = row.xpath('.//td[4]//text()')
                    change_24h_list = row.xpath('.//td[5]//text()')
                    market_cap_list = row.xpath('.//td[8]//text()')

                    rank = rank_list[0].strip() if rank_list else None
                    name = name_list[0].strip() if name_list else None
                    symbol = symbol_list[0].strip() if symbol_list else None
                    price = price_list[0].strip() if price_list else None
                    change_24h = change_24h_list[0].strip() if change_24h_list else None
                    market_cap = market_cap_list[0].strip() if market_cap_list else None

                    if all([rank, name, symbol, price, change_24h, market_cap]):
                        self.results.append({
                            'Rank': rank,
                            'Name': name,
                            'Symbol': symbol,
                            'Price (USD)': price,
                            '24h % Change': change_24h,
                            'Market Cap (USD)': market_cap,
                        })
                    else:
                        raise Exception("Not all data is parsed")
                except Exception as e:
                    raise
