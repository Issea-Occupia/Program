import requests
from bs4 import BeautifulSoup
url = "https://www.economist.com/leaders/2025/11/06/chinas-clean-energy-revolution-will-reshape-markets-and-politics"
resp = requests.get(url= url)