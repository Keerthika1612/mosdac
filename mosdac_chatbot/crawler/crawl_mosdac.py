# Crawl Mosdac.Py - Placeholder
# crawler/crawl_mosdac.py
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# URLs grouped by category
STATIC_CATEGORIES = {
    "satellite_data": ["https://mosdac.gov.in/data"],
    "about_mosdac": ["https://mosdac.gov.in/about"]
}

DYNAMIC_CATEGORIES = {
    "gallery": ["https://mosdac.gov.in/gallery/index.html?&prod=3SIMG_*_L1B_STD_IR1_V*.jpg"]
}

META_FILE = "data/raw/meta.json"

def sanitize_filename(url):
    return url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_").replace("&", "_").replace("*", "_")

def scrape_static_pages(meta):
    for category, urls in STATIC_CATEGORIES.items():
        save_dir = f"data/raw/static/{category}"
        os.makedirs(save_dir, exist_ok=True)
        for url in urls:
            try:
                res = requests.get(url, headers=HEADERS)
                soup = BeautifulSoup(res.content, "html.parser")
                filename = sanitize_filename(url) + ".html"
                file_path = os.path.join(save_dir, filename)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
                meta.append({"category": category, "url": url, "file": file_path})
                print(f"[✓] Static scraped: {url}")
            except Exception as e:
                print(f"[x] Static error at {url}: {e}")

def scrape_dynamic_pages(meta):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for category, urls in DYNAMIC_CATEGORIES.items():
        save_dir = f"data/raw/dynamic/{category}"
        os.makedirs(save_dir, exist_ok=True)
        for url in urls:
            try:
                driver.get(url)
                time.sleep(4)
                html = driver.page_source
                filename = sanitize_filename(url) + ".html"
                file_path = os.path.join(save_dir, filename)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html)
                meta.append({"category": category, "url": url, "file": file_path})
                print(f"[✓] Dynamic scraped: {url}")
            except Exception as e:
                print(f"[x] Dynamic error at {url}: {e}")

    driver.quit()

def crawl_mosdac():
    os.makedirs("data/raw", exist_ok=True)
    meta = []
    print("==> Crawling Static Pages")
    scrape_static_pages(meta)
    print("==> Crawling Dynamic Pages")
    scrape_dynamic_pages(meta)
    # Save metadata
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=4)
    print(f"[✓] Crawling completed. Metadata saved to {META_FILE}")

if __name__ == "__main__":
    crawl_mosdac()
