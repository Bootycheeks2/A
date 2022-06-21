from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# set up browser
browser = webdriver.Safari()
browser.get("https://pm62a.leadperfection.com/Start.html")

# login
email = browser.find_element(By.XPATH, "//input[@id='txtUserName']")
email.send_keys("xn4zhang@uwaterloo.ca")

pwd = browser.find_element(By.XPATH, "//input[@id='txtPassword']")
pwd.send_keys("XuanNing!234")

submit_button = browser.find_element(By.ID, "btnLogin")
submit_button.click()

# wait 3 secs
time.sleep(3)

# pass that check
pass

# go to job
browser.maximize_window() # to show the buttons

time.sleep(2) # wait

prod_btn = browser.find_element(By.XPATH, "//ul/li[4]/a[@class='nav-link nav-toggle ']")
a = ActionChains(browser) # used for mouseover
a.move_to_element(prod_btn).perform()

time.sleep(1) # wait until it appears

job_btn = browser.find_element(By.XPATH, "//ul/li[4]/ul/li[1]/a[@href='JobFilters.html?BC=Production|Job Search']")
a.move_to_element(job_btn).click().perform()

