"""
Get Url Youtube
Search in Search Box Youtube
Get all Channel and Follower
Convert to csv
Package : Selenium , pandas
"""

from selenium import webdriver
import time
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

search_value_input = input("Enter the word or phrase you want to search for: ")

URL = "https://www.youtube.com/"

driver_path = r"chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(driver_path)

driver.maximize_window()
driver.get(URL)

# Click to button accept all cookies
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH,
                                '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/'
                                'div[6]/div[1]/ytd-button-renderer[2]/a/'
                                'tp-yt-paper-button/yt-formatted-string'))).click()

time.sleep(10)
wait = WebDriverWait(driver, 3)
visible = EC.visibility_of_element_located

# send string in search box and click search
wait.until(visible((By.NAME, "search_query")))
driver.find_element(By.NAME, "search_query").click()
driver.find_element(By.NAME, "search_query").send_keys(search_value_input)
driver.find_element(By.ID, "search-icon-legacy").click()
time.sleep(5)

# TODO Activate this section to search until the last link   End Page Scroll
i = 0
while i < 1000:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    i += 1

# TODO Activate this section to search until the last link of the current page   lazy Scroll
# driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)


time.sleep(10)

# Get All Link Video And Append to Links list
user_data = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
links = []
for i in user_data:
    if i.get_attribute('href') is not None:
        links.append(i.get_attribute('href'))

df = pd.DataFrame(columns=['Channel', 'subscribers'])

# open all Link in Links list And Extract Channel Name and Subscribe
wait = WebDriverWait(driver, 10)
for x in links:
    driver.get(x)
    v_id = x.strip('https://www.youtube.com/watch?v=')
    v_channel = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="text"]/a'))).text
    v_sub = None
    try:
        v_sub = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="owner-sub-count"]'))).text.split(" ")[0]
    except:
        pass
    # You can also extract other information in this section

    print(v_channel + " " + v_sub)
    df.loc[len(df)] = [v_channel, v_sub]

df.to_csv('Youtube.csv')
driver.quit()
