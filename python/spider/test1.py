import requests
from bs4 import BeautifulSoup
url = "https://www.runoob.com/python3/python3-with-keyword.html"
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'}
resp = requests.get(url,headers=headers)
soup = BeautifulSoup(resp.text,'html.parser')
print(soup.markup)