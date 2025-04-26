
# 📈 CoinMarketCap Watchlist – Crypto Scraper
**Scrape top cryptocurrencies from CoinMarketCap** using **HTML parsing** or **internal JSON API**, with automatic retries, pagination support, and CSV export.

## 🚀 Getting Started

### ✅ Prerequisites

1.  **Install Python 3.12 or higher**  
    Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    
2.  **Install Poetry** (dependency manager)  
	 Run in terminal: 
    `pip install playwright`
    
4.  **Install Poetry** 
    Run in terminal: 
    pip install poetry` 
    
5.  **Install project dependencies**  
    In the project root directory, run:
    `poetry install` 
    This will create a virtual environment and install all required libraries.
    

----------

## ⚙️ How to Run
You can choose between **HTML scraping** or **JSON API scraping**.
### Option 1: Run via IDE

Open `main.py` in your IDE and execute it directly.
You can pass optional arguments: scrapper, loops, pages.

### Option 2: Run via Terminal
Navigate to the project folder and run:
`poetry run python main.py` 
**Default behavior:**
-   Scraper: `json`
-   Loops: `1` (For debuging)
-   Pages per loop: `5`
**Example with arguments:**
 `poetry run python main.py --scrapper html--loops 3 --pages 10` 
  
## 🧠 Features
-   ✅ Scrape cryptocurrency data (Rank, Name, Symbol, Price, 24h % Change, Market Cap)
-   ✅ Supports both **HTML parsing** and **internal JSON API**.
-   ✅ Handles pagination
-  	✅ Control how much data you collect by select pages and loop

## 🛠 Improvements (Planned)
-  Error and logging handling (for example if missing data, give logs and continue. for now we stop script).
- Save more data (Timestamp, who run script and etc) in DB and not cvs for future filters and statistic.
- Improve HTML execution time.
- Control what values to extract with parametrs before execution.
- Stop script with CTRL+C (if we stop write all data before closing).
## 📏 Compare Lines of Code and  Performance##
| HTML Scraper  | JSON  Scraper |
|--|--|
| ~80 lines|~40 lines|

HTML scraping needs almost double the code compared to JSON scraping.
-   HTML scraping needs to:
    -   Load browser (Playwright)
    -   Navigate with retries
    -   Auto-scroll
    -   Parse dynamic DOM with XPath
-   JSON scraping:
    -   Fetch endpoint
    -   Parse JSON directly (easier)
    - 
**Compare Requests per Second:**
Single Request :
| HTML Scraper  | JSON  Scraper |
|--|--|
| ~20s|~1s|

✅ **JSON parser is much faster and more stable** because:
-   It works with **direct API requests** (no browser needed).
-   Responses are  **structured** (pure JSON) (after parsing to tree).
-   **HTTP requests** are lightweight.
-   **Much lower resource usage**: no browser process, no DOM rendering, less RAM and CPU.