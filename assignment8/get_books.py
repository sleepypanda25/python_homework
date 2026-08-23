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
    #time.sleep(3)
    search_results = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
    results = []

    for entry in search_results:
        title = entry.find_element(By.CSS_SELECTOR, "span.title-content")
        author = entry.find_element(By.CSS_SELECTOR, "a.author-link")
        format_year_parent = entry.find_element(By.CSS_SELECTOR, "div.cp-format-info")
        format_year = format_year_parent.find_element(By.CSS_SELECTOR, "span.display-info-primary")

        book = {"Title": title.text, "Author": author.text, "Format-Year": format_year.text}
        results.append(book)

    df = pd.DataFrame(results)
    print(df)

    with open('get_books.csv', 'w') as file:
        writer = csv.writer(file)

        for book in results:
            writer.writerow([book['Title'], book['Author'], book['Format-Year']])

    data = {"results": results}
    with open('get_books.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
except Exception as e:
    print("Couldn't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()