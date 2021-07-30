import json
from selenium import webdriver
import loguru
from time import sleep

logger = loguru.logger
driver = webdriver.Chrome()
url = "https://www.52pojie.cn/home.php?mod=space&do=notice"


def login_with_qq():
    driver.find_element_by_xpath("""/html/body/div[6]/div/div[2]/div/div[2]/div[1]/div[1]/form/div/div[
7]/table/tbody/tr/td/a""").click()


def get_cookies():
    driver.get(url)
    while True:
        logger.info("请在30秒内登入")
        sleep(30)
        while driver.current_url == url:
            cookies = driver.get_cookies()
            driver.quit()
            logger.debug(cookies)
            cookies_list = list(cookies)
            with open("cookies.json", "w+", encoding="utf-8") as f:
                f.write(json.dumps(cookies_list))
            logger.info("Cookies写入成功.")


if __name__ == '__main__':
    get_cookies()
