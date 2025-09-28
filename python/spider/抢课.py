import requests
url = "https://xk.xidian.edu.cn/xsxk/elective/clazz/add"
data = "clazzType=XGKC&clazzId=20252026124TS521301&secretVal=gOj%2BcPfitMb62bE2Xgk1kpzS%2FCJhEXtf0d8O%2FapIaHSs1tFg4TDU9mCI7M%2B%2FgVKnf7zTVGSVJj3z428dDzfIkXoTw9bsGFQvqGBfSCJZ13V50rRaxWw%2BX4vXrt3shGIeq6OwQJo4RwTCovqYxx0kBpdzSg3Hx3q8d1u00FDdUZxfxlUh2aMOy25%2FXq%2Fa3Va7"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzU3MDUwNDQ2MzIxLCJsb2dpbl91c2VyX2tleSI6IjI1MjA5MTAwMjk2IiwidG9rZW4iOiJ2c2NvZG5tbWY0aG45bzVscWF0MDdkaW1jMyJ9.GaOVJBza6nC-b3Zi0tZLryGTIE4JBR_vTUy4s3Wsa-CtE18nwGTKnBiBzjStqriKJZHYBy3fWfhXTsAe_4z8EQ",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://xk.xidian.edu.cn",
    "Referer": "https://xk.xidian.edu.cn/xsxk/elective/grablessons?batchId=b2cbbed2af674914a39b2491f04718a4",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "batchId": "b2cbbed2af674914a39b2491f04718a4",
}
cookies_str = "route=96c792601f32dee97fb7b2aeb2c2e26b; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzU3MDUwNDQ2MzIxLCJsb2dpbl91c2VyX2tleSI6IjI1MjA5MTAwMjk2IiwidG9rZW4iOiJ2c2NvZG5tbWY0aG45bzVscWF0MDdkaW1jMyJ9.GaOVJBza6nC-b3Zi0tZLryGTIE4JBR_vTUy4s3Wsa-CtE18nwGTKnBiBzjStqriKJZHYBy3fWfhXTsAe_4z8EQ; UqZBpD3n3iPIDwJU9BK0+GaUSfMU+shOdMyKuI8_=v1BqFbQwSDPH1"
cookies = {kv.split("=",1)[0].strip(): kv.split("=",1)[1] for kv in cookies_str.split("; ")}
session = requests.Session()
while True:
    response = session.post(url, headers=headers, cookies=cookies, data=data)

    print("状态码:", response.status_code)
    print("返回内容:", response.text[:500])