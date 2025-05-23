
#  Broadway Shows Scraper

This project is a Python-based web scraper that extracts production data for current Broadway shows listed on [IBDB.com](https://www.ibdb.com/shows). It collects show titles, dates, venues, categories, images, and links to full show details, then stores the structured data in a CSV file.

---

##  Features

- Extracts real-time show data including:
  - Show Title
  - Show Date/Time
  - Venue Name
  - Show Type (e.g., Musical, Play)
  - Poster Image URL
  - Full Details Page URL
- Stores data in `shows.csv` with deduplication logic.
- Uses **Selenium** and **BeautifulSoup** for robust scraping of JavaScript-rendered pages.
- Polite scraping: includes request delays and avoids overloading the site.
- Ready for automation using task schedulers (cron or Windows Task Scheduler).

---

##  Setup Instructions

### 1. Clone or Download

```bash
git clone https://github.com/olumideadekunle/broadway-shows-scraper.git
cd broadway-shows-scraper
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
# Windows
.env\Scriptsctivate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Or manually install:
```bash
pip install selenium beautifulsoup4 pandas
```

---

## ⚙️ Usage

Run the scraper:

```bash
python scraper.py
```

Output will be saved in:

```
shows.csv
```

If the file exists, only new shows will be appended (duplicates are ignored).

---

##  Automation (Optional)

You can schedule this script to run daily using:

- **Windows Task Scheduler**
- **macOS/Linux cron jobs**
- Or Python `schedule` or `APScheduler` libraries

To log each run, you can modify the script to include:

```python
with open("log.txt", "a") as log:
    log.write(f"{datetime.now()} - {title_text} scraped\n")
```

---

##  How It Works

1. Launches a Selenium Chrome browser.
2. Navigates to the [IBDB shows page](https://www.ibdb.com/shows).
3. Extracts the list of shows using BeautifulSoup.
4. For each show:
   - Navigates to the detail page.
   - Parses information: title, date, venue, category, image, etc.
5. Avoids re-scraping already collected shows.
6. Saves all new results to `shows.csv`.

---

##  Ethical Scraping & Limitations

- Includes delays between requests (`time.sleep(5)`) to avoid hammering the server.
- Uses browser-based scraping to stay within site rendering patterns.
- Avoids frequent or high-volume scraping.
- ** Always respect site terms of service.**

---

##  File Structure

```
broadway-shows-scraper/
├── scraper.py         # Main scraper script
├── shows.csv          # Output data
├── venv/              # Python virtual environment
└── README.md          # This file
```

---

##  Contact

For feedback, issues, or contributions, please contact:

##  Olumide Adekunle Buari 

