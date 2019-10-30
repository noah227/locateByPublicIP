# __Author__: NOLA
# __Date__: 2019/10/29


import requests
from bs4 import BeautifulSoup
import geoip2.database
import time

url = "http://ip.tool.chinaz.com/"


# 检查是否加入标题栏
def add_column():
    with open("../log/log_exist", "a+") as f:
        pass
    with open("../log/log_exist", "r+") as f:
        content = f.readline()
        if not content or content == "0":
            f.write("1")
            with open("../log/log", "a+", encoding="utf-8") as file:
                file.write("          时间                   IP          纬度         "
                           "经度      城市        国家        洲" + "\n")


"""
def add_column():
    with open("../log/log", "a+", encoding="utf-8") as file:
        file.write("          时间                   IP          纬度         经度      城市        国家        洲" + "\n")
"""


def log(response, ip):
    current_time = time.ctime()
    latitude = str(response.location.latitude).ljust(8, " ")
    longitude = str(response.location.longitude).ljust(8, " ")
    continent = response.continent.names["zh-CN"].ljust(5, " ")
    country = response.country.names["zh-CN"].ljust(8, " ")
    city = response.city.names["zh-CN"].ljust(8, " ")

    information = [current_time, ip, latitude, longitude, city, country, continent]

    log_info = "\t".join(information)
    # add_column()
    with open("../log/log", "a+", encoding="utf-8") as f:
        f.write(log_info + "\n")


def general_location(ip):
    reader = geoip2.database.Reader("../lib/GeoLite2-City.mmdb")
    response = reader.city(ip)
    return response


def get_location(url):
    html = requests.get(url)
    content = html.text
    soup = BeautifulSoup(content, "lxml")
    # 获取公网ip
    public_ip_address = soup.find_all("dl", {"class": "IpMRig-tit"})[0].find_all("dd")[0].get_text()
    # 通过geoip2获取地理位置信息集
    result = general_location(public_ip_address)
    # 写入日志
    log(result, public_ip_address)


if __name__ == "__main__":
    add_column()
    get_location(url)


# ip 15
# gps 8
