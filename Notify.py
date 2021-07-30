import os
import json
import time

import requests
import loguru
from bs4 import BeautifulSoup

logger = loguru.logger

r = requests.session()


def get_notify():
    n = r.get("https://www.52pojie.cn/home.php?mod=space&do=notice")
    soup = BeautifulSoup(n.text, 'lxml')
    news = soup.find_all(class_='ntc_body')
    ret = []
    for new in news:
        new_soup = BeautifulSoup(str(new), 'lxml')
        ret.append(new_soup.text)
    logger.info("获取信息成功！")
    return ret


def get_notify_():
    with open("test.html", "r", encoding="utf-8") as t:
        soup = BeautifulSoup(t.read(), 'lxml')
    news = soup.find_all(class_='ntc_body')
    ret = []
    for new in news:
        new_soup = BeautifulSoup(str(new), 'lxml')
        ret.append(new_soup.text)
    logger.info("获取信息成功！")
    return ret


def get_send_key():
    try:
        with open("SendKey.txt", "r", encoding="utf-8") as key:
            return key.read()
    except Exception:
        logger.warning("打开文件失败，请确保SendKey.txt存在!")


def send(title):
    key = get_send_key()
    requests.get(f'https://sctapi.ftqq.com/{key}.send?title={title}')
    logger.info(f'已发送信息：{title}')


if os.path.exists("cookies.json"):
    logger.info("找到Cookies文件!")
    with open("cookies.json", "r") as f:
        cookies = json.loads(f.read())
    r_cookies = dict()
    for cookie in cookies:
        r_cookies[cookie['name']] = cookie['value']
    r.cookies.update(r_cookies)
else:
    logger.warning("未发现Cookies文件，请使用 GetCookies.exe 获取")

if __name__ == '__main__':
    base_news = get_notify()
    while True:
        news = get_notify()
        different = set(news) - set(base_news)
        base_news = news
        if different is not None:
            for diff in different:
                send(diff)
        time.sleep(60 * 10)
