from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import csv

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get("https://owasp.org/www-project-top-ten/")

    top_10_link = driver.find_element(By.XPATH, '//a[text()="OWASP Top 10:2025"]')
    url = top_10_link.get_attribute("href")

    top_10_link.click()

    list = driver.find_elements(By.XPATH, '//ol/li/a')
    
    top_10 = []

    for item in list:
        title = item.text
        url = item.get_attribute("href")

        element = {"Title": title, "Link": url}
        top_10.append(element)

    print(top_10)
    df = pd.DataFrame(top_10)

    df.to_csv('owasp_top_10.csv', index=False)
except Exception as e:
    print(e)
finally:
    driver.quit()