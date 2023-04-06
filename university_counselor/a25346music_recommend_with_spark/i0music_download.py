import requests
from bs4 import BeautifulSoup
import csv

# 设置请求头部
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://music.163.com/",
    "Host": "music.163.com",
}

# 设置歌曲ID
song_id = "447925871"

# 发送请求，获取歌曲详情页面
url = "https://music.163.com/song?id=" + song_id
response = requests.get(url, headers=headers)
html = response.text

# 解析页面，获取歌曲信息
soup = BeautifulSoup(html, "html.parser")
song_name = soup.find("em", class_="f-ff2").get_text()
singer_name = soup.find("div", class_="cnt").find_all("a", class_="s-fc7")[0].get_text()

# 尝试获取专辑名称，如果找不到则将其设置为空字符串
album_name_tag_list = soup.find("div", class_="cnt").find_all("a", class_="s-fc7")
if len(album_name_tag_list) > 1:
    album_name = album_name_tag_list[1].get_text()
else:
    album_name = ""


# 尝试获取下载链接，如果找不到则将其设置为空字符串
download_url_tag = soup.find("div", class_="u-share")
if download_url_tag:
    download_url_tag = download_url_tag.find("a", class_="u-btni u-btni-dwn")
    if download_url_tag:
        download_url = download_url_tag["href"]
    else:
        download_url = ""
else:
    download_url = ""

# 保存歌曲信息到CSV文件
with open("data/163music_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["Song ID", "Song Name", "Singer Name", "Album Name", "Download URL"]
    )
    writer.writerow([song_id, song_name, singer_name, album_name, download_url])

# print('Download URL:', download_url)
print("bot is downloaing music data")
