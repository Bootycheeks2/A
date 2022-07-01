# Usage:
# [python interpreter alias] autowork.py /path/to/file

# Purpose:
# 1. Extract all orders from file given
# 2. Perform the selenium script on each order

# File management requisites
import sys  # access to cli arguments
import os
import re  # use regex pattern-matching

# Selenium library
from selenium import webdriver  # access to browser
from selenium.webdriver.common.keys import Keys  # access to special keys
from selenium.webdriver.common.by import By  # selector helper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Time library
import time  # access to sleep

# Html-PDF conversion
import pdfkit


class Order:
    """Represents one order line from a given filepath."""

    # Class variable holding Order objects to facilitate iterating over them
    order_lst = []
    # Regex string to capture orders
    r_str = r"(\d{6}) - \$?\s?([0-9.,]{4,11}) - (\d+ \w+) - (\d+)"
    # Path of file
    p_file = ""


    def __init__(self, param):
        """Instantiates one order (constructor) from string"""
        # Param is a tuple that we deconstruct
        # It contains parts of the order
        self.num, self.monies, self.date, self.receipt = param

        # Sanitization
        def sanitize_date(date):
            months = {
                "January": "1",
                "February": "2",
                "March": "3",
                "April": "4",
                "May": "5",
                "June": "6",
                "July": "7",
                "August": "8",
                "September": "9",
                "October": "10",
                "November": "11",
                "December": "12"
            }
            tmp = date.split()
            tmp[1] = months[tmp[1]]  # Replaces word month with integer string
            return tmp

        self.monies = self.monies.replace(",", "")
        self.date = sanitize_date(self.date)  # [0]: day, [1]: month

    def __repr__(self):
        """Produces string representation of object"""
        return "::".join((self.num, self.monies, "/".join(self.date), self.receipt))

    @classmethod
    def extract_orders(cls, path):
        """Class method: Extracts orders from given file path,
        creating a new Order object for each order"""

        orderlst = []  # list of orders
        cls.p_file = path  # saves the path

        with open(path) as f:
            data = f.read()
            orderlst.extend(re.findall(cls.r_str, data))

        for order in orderlst:
            obj = cls(order)
            print(obj)
            cls.order_lst.append(obj)

    def act(self):
        """Executes selenium script on current order"""

        # Websites
        lp = {
            "address": "https://pm62a.leadperfection.com/Start.html",
            "username": "xn4zhang@uwaterloo.ca",
            "password": "XuanNing!234",
        }
        dv = {
            "address": "https://lifestyle.davinci360.ca/",
            "username": "xn4zhang@uwaterloo.ca",
            "password": "123",
        }

        # Davinci360 part
        browser = webdriver.Safari()
        browser.implicitly_wait(10)  # Implicitly wait 3 seconds for each interaction
        browser.get(dv["address"])

        browser.find_element(By.NAME, "email").send_keys(dv["username"])
        browser.find_element(By.NAME, "pwd").send_keys(dv["password"])
        browser.find_element(By.NAME, "submit").click()
        time.sleep(4)

        browser.find_element(By.XPATH, "//div[@id='NavBarToolBar']/span").click()
        browser.find_element(By.XPATH, "//ul[@id='mnuMainSwitch']/li[4]").click()

        # There is an alert pop-up
        try:
            WebDriverWait(browser, 3).until(EC.alert_is_present(), "Timed out waiting for PA creation" + "confirmation popup to appear.")
            browser.switch_to.alert.dismiss()  # Alert accepted
            print("Alert dismissed")
        except TimeoutException:
            print("No alert")
        time.sleep(1)

        browser.find_element(By.XPATH, "//tr[@id='lstReports_53']/td").click()
        time.sleep(3)

        # Get report
        browser.find_element(By.ID, "txtON").send_keys(self.receipt)
        browser.find_element(By.XPATH, "//input[@value='View Report']").click()
        browser.find_element(By.XPATH, "//input[@value='View Report']").click()
        time.sleep(2)

        # Go to report tab
        p = browser.current_window_handle
        children = browser.window_handles
        print(len(children))
        for handle in children:
            if handle != p:  # Presuming handles ordered chronologically
                browser.switch_to.window(handle)
        time.sleep(1)

        # Download and process report html to pdf
        src = browser.page_source
        dirpath = os.path.dirname(Order.p_file)
        inspath = os.path.join(dirpath, self.num)
        with open(f"{inspath}.html", "w") as f:
            f.write(src)

        pdfkit.from_file(f"{inspath}.html", f"{inspath}.pdf")

        browser.close()
        print("Done.")



if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: [python interpreter alias] autowork.py /path/to/file"
    Order.extract_orders(sys.argv[1])
    Order.order_lst[0].act()
