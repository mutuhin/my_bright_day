from webbrowser import get
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep





from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import TimeoutException
import os
import csv
# Setup Chrome options
options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
# options.add_argument('--headless')  



driver = Chrome(options=options)



months = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='well pull-right left-panel']/ul/li"))
)

data = []
for month in months:
    month.click()
    sleep(2)
    spans = month.find_elements("xpath", ".//div/div/div/div/span")
    month_text = " ".join([span.text for span in spans])

    try:
        urls = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@class='fancybox']"))
        )
        for url in urls:
            sleep(2)
            image_url = url.get_attribute("href")
            data.append((month_text, image_url))
    except TimeoutException:
        print(f"No URLs found for {month_text}, skipping to the next month.")
        continue

driver.quit()

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Month", "URL"]) 
    writer.writerows(data)




# siddharthm
# Bright2024!