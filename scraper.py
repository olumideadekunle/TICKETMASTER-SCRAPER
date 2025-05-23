import time
import re
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

def scrape_broadway_shows():
    

    # Launch browser
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(320)

    base_url = "https://www.ibdb.com"
    extracted_shows = []

    try:
        driver.get("https://www.ibdb.com/shows")
        time.sleep(5)
        soup_main_page = BeautifulSoup(driver.page_source, "html.parser")

        show_containers = soup_main_page.find("div", class_="page-wrapper xtrr")\
            .find("div", class_="shows-page")\
            .find("div", class_="row bgcolor-greyWhite2")\
            .find("div", class_="xt-c-box row")\
            .find("div", id="current")\
            .find("div", class_="row show-images xt-iblocks")\
            .find_all("div", class_="xt-iblock")

        # Load existing data
        try:
            df_existing = pd.read_csv("Buari_show.csv")
            existing_entries = set(zip(df_existing["Title"], df_existing["Date"]))
        except FileNotFoundError:
            df_existing = pd.DataFrame()
            existing_entries = set()

        for show_block in show_containers:
            show_link_tag = show_block.find("div", class_="xt-iblock-inner").find("a", href=True)
            if not show_link_tag:
                continue

            full_show_url = base_url + show_link_tag['href']
            try:
                driver.get(full_show_url)
                time.sleep(5)
            except Exception as page_error:
                print(f"Error accessing {full_show_url}: {page_error}")
                continue

            soup_detail_page = BeautifulSoup(driver.page_source, "html.parser")
            body_tag = soup_detail_page.find("body", class_="winOS")

            if not body_tag:
                print("Missing body.winOS tag")
                continue

            content_layout = body_tag.find("div", class_=re.compile("^production-page"))\
                .find("div", class_=re.compile("^xt-c-box"))\
                .find("div", class_="row xt-fixed-sidebar-row")

            left_section = content_layout.find("div", class_=re.compile("col l4.*xt-l-col-left"))\
                .find("div", class_=re.compile("production-info-panel"))\
                .find("div", class_=re.compile("xt-fixed-sidebar"))\
                .find("div", class_=re.compile("jsfixed-placeholder"))\
                .find("div", class_=re.compile("jsfixed-block"))

            logo_section = left_section.find("div", class_=re.compile("xt-fixed-block main-logo-wrapper"))\
                .find("div", class_="row logo")\
                .find("div", class_="col s12")\
                .find("div", class_="logo-block xt-logo-block sdf")

            poster_url = logo_section.find("div", class_="xt-logo-img").find("img")['src']
            title_text = logo_section.find("div", class_="title").find("div").find("h3").text.strip()
            show_genre = left_section.find("div", attrs={"data-id": "part-b"})\
                .find("div", class_="row wrapper hide-on-small-and-down")\
                .find("div").find("i").text.strip()

            extra_info = left_section.find("div", attrs={"data-id": "part-b"})\
                .find("div", class_="xt-info-block")\
                .find_all("div", class_="row wrapper")

            right_section = content_layout.find("div", class_=re.compile("col l8.*xt-l-col-right"))\
                .find_all("div", class_="row")

            venue_column = right_section[1]
            venue_content = venue_column.find(id="venues")
            if not venue_content:
                venue_column = right_section[2]
                venue_content = venue_column.find(id="venues")
            if not venue_content:
                raise Exception("Venue information not found")

            venue_box = venue_content.find("div", class_=re.compile("col s12 m4 theatre"))
            venue_rows = venue_box.find_all("div", class_="row")

            venue_title = venue_rows[1].find("a").text.strip()
            show_schedule = venue_rows[1].find("i").text.strip()

            if (title_text, show_schedule) in existing_entries:
                continue

            extracted_shows.append({
                "Link_Detail": full_show_url,
                "Show_Title": title_text,
                "Date/Time": show_schedule,
                "Venue_Name": venue_title,
                "Type": show_genre,
                "Image Url": poster_url,
            })

            print(f"Collected: {title_text} - {show_schedule}")

    except Exception as global_error:
        print(f"Error occurred during scraping: {global_error}")
    finally:
        driver.quit()

    # Save collected data
    if extracted_shows:
        df_new = pd.DataFrame(extracted_shows)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset=["Show_Title", "Date/Time"], inplace=True)
        df_combined.to_csv("Buari_show.csv", index=False)
    else:
        print("No new entries collected.")

# Run the function
scrape_broadway_shows()

