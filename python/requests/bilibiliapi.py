import requests

API_URL = "https://api.bilibili.com/x/web-interface/popular"  # 示例接口
MIN_DURATION = 300  # 秒数，5分钟起
headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
    }
def get_videos(page=1):
    resp = requests.get(API_URL, params={"pn": page},headers=headers)
    data = resp.json()

    # 提取视频列表
    videos = data['data']['list']
    long_videos = []

    for v in videos:
        duration = v.get("duration", 0)
        # 核心过滤逻辑：
        if duration >= MIN_DURATION:
            long_videos.append({
                "title": v["title"],
                "duration": duration,
                "url": f"https://www.bilibili.com/video/{v['bvid']}"
            })

    return long_videos

if __name__ == "__main__":
    videos = get_videos()
    for v in videos:
        print(f"{v['title']} ({v['duration']//60} min) → {v['url']}")
