from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import json
import csv

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

    # All search results
    # Tag: li
    # Class: cp-search-result-item
    search_results = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
    results = []

    for entry in search_results:
        # Title
        # Tag: span
        # Class: title-content
        title = entry.find_element(By.CSS_SELECTOR, "span.title-content")

        # Authors
        # Tag: a
        # Class: author-link
        authors = entry.find_elements(By.CSS_SELECTOR, "a.author-link")

        # Format Year Parent Div
        # Tag: div
        # Class: cp-format-info
        format_year_parent = entry.find_element(By.CSS_SELECTOR, "div.cp-format-info")

        # Format Year
        # Tag: span
        # Class: display-info-primary
        format_year = format_year_parent.find_element(By.CSS_SELECTOR, "span.display-info-primary")

        authors_str = ';'.join(author.text for author in authors)

        book = {"Title": title.text, "Author": authors_str, "Format-Year": format_year.text}
        results.append(book)

    df = pd.DataFrame(results)
    print(df)

    df.to_csv('get_books.csv', index=False)

    with open('get_books.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
except Exception as e:
    print("Couldn't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()