from abc import ABC, abstractmethod
import csv

class Scraper(ABC):
    def __init__(self, loops=1, pages=5):
        self.loops = loops
        self.pages = pages
        self.results = []
        self.url = "https://coinmarketcap.com/"
        

    @abstractmethod
    def fetch(self):
        """Fetch the raw data (HTML or JSON)."""
        pass

    @abstractmethod
    def parse(self, raw_data):
        """Parse the raw data into structured results."""
        pass

    def save(self, filename):
        """Save results to CSV."""
        if not self.results:
            raise ValueError("No data to save.")

        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)

        print(f"Saved {len(self.results)} records to {filename}.")
