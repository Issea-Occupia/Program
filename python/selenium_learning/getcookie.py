from selenium import webdriver
from pathlib import Path
import json
import time
driver = webdriver.Chrome()
driver.get("https://www.bilibili.com")
time.sleep(10.0)