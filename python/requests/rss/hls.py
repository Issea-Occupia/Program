import requests
import lxml
from bs4 import BeautifulSoup
url = "https://cn.yna.co.kr/RSS/nk.xml"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"}
resp = requests.get(url=url,headers=headers)
text = resp.text
soup = BeautifulSoup(text,"xml")
print(soup.title.string)