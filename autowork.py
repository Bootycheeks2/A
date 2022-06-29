# Usage:
# [python interpreter alias] [this script] /path/to/file

# Purpose:
# 1. Extract all orders from file given
# 2. Perform the selenium script on each order

# File management requisites
import os # access to OS
import sys # access to cli arguments
import re # use regex pattern-matching

# Selenium library
from selenium import webdriver # access to browser
from selenium.webdriver.common.keys import Keys # access to special keys
from selenium.webdriver.common.by import By # selector helper
from selenium.webdriver.common.action_chains import ActionChains


class Order:
    """Represents one order line from a given filepath."""

    order_lst = []
    r_str = r"(\d{6}) - \$?\s?([0-9.,]{4,11}) - (\d+ \w+) - (\d+)"

    def __init__(self, param):
        """Instantiates one order (constructor) from string"""
        # Param is a tuple that we deconstruct
        # It contains parts of the order
        self.param = "::".join(param)
        self.num, self.monies, self.date, self.receipt = param

    
    def __repr__(self):
        """Produces string representation of object"""
        return self.param


    @classmethod
    def extract_orders(cls, path):
        
        orderlst = [] # list of orders

        with open(path) as f:
            data = f.read()
            orderlst.extend(re.findall(cls.r_str, data))

        for order in orderlst:
            obj = cls(order)
            print(obj)
            cls.order_lst.append(obj)


    def act(self):
        pass


if __name__ == "__main__":
    Order.extract_orders(sys.argv[1])

