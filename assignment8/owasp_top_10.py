from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import csv

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get("https://owasp.org/www-project-top-ten/")

    sidelist_div = driver.find_element(By.CSS_SELECTOR, 'div.sidebar')
    sidelist = sidelist_div.find_elements(By.CSS_SELECTOR, 'a')

    for link in sidelist:
        name = link.text.strip()
        url = link.get_attribute("href")

        if name == "OWASP Top 10:2025" and url == "https://owasp.org/Top10/2025/":
            link.click()

            list_header = driver.find_element(By.CSS_SELECTOR, '[id="top-102025-list"]')
            ordered_list = list_header.find_element(By.XPATH, 'following-sibling::ol')
            list = ordered_list.find_elements(By.CSS_SELECTOR, 'a')

            top_10 = []

            for item in list:
                title = item.text
                url = item.get_attribute("href")

                element = {"Title": title, "Link": url}
                top_10.append(element)

            print(top_10)

            with open('owasp_top_10.csv', 'w') as file:
                writer = csv.writer(file)

                for element in top_10:
                    writer.writerow([element['Title'], element['Link']])

            driver.back()
except Exception as e:
    print("Trouble opoening web page")
    print(e)
finally:
    driver.quit()