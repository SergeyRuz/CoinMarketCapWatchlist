
import argparse
import asyncio
import time
from scrapers.scrapers import Scraper
from scrapers.html_scraper import HTMLScraper
from scrapers.json_scraper import JSONScraper


def main(scraper: Scraper, filename: str):
    raw_data = asyncio.run(scraper.fetch()) 
    scraper.parse(raw_data)
    scraper.save(filename)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Run Crypto Parser.")
        parser.add_argument(
            "--scrapper", 
            type=lambda s: s.lower(),
            default="json", 
            choices=["json", "html"],
            help="The way we want to scrap"
        )
        parser.add_argument(
            "--loops", 
            type=int,
            default=1, 
            help="Choose loop count, single loop is 5 pages"
        )
        parser.add_argument(
            "--pages", 
            type=int,
            default=5, 
            help="Choose page amount, to parse"
        )

        args = parser.parse_args()
        start= time.time()
        if args.scrapper == "json":
            html_scraper = JSONScraper(loops=args.loops, pages=args.pages)
            main(html_scraper, "coins_json.csv")
            
        if args.scrapper == "html":
            html_scraper = HTMLScraper(loops=args.loops, pages=args.pages)
            main(html_scraper, "coins_html.csv")
        end = time.time()
        print(f"Total time for {args.loops} runs: {end - start:.2f} seconds")
        print(f"Average time per run: {(end - start)/args.loops:.2f} seconds")
    except Exception as e:
        print(str(e))
