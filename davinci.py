from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# set up browser
browser = webdriver.Safari()
browser.get("https://lifestyle.davinci360.ca")

# login
email = browser.find_element(By.NAME, "email")
email.send_keys("xn4zhang@uwaterloo.ca")

pwd = browser.find_element(By.NAME, "pwd")
pwd.send_keys("123")

submit_button = browser.find_element(By.NAME, "submit")
submit_button.click()

# wait 3 secs
time.sleep(3)

# logout
logout_menu = browser.find_element(By.XPATH, "//span[@id='NavBarUser']")
logout_menu.click()
logout_button = browser.find_element(By.ID, "ui-id-8")
logout_button.click()

# close browser
browser.quit()
print("Done.")
