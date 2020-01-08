# -*- coding: utf-8 -*-

from selenium import webdriver
import sys
import json
import const_define
from abc import ABC, abstractmethod
from datetime import datetime
from dateutil import tz
import re


class DateTimeControl(object):
    def __init__(self):
        super(DateTimeControl, self).__init__()

    def change_string_to_utc_datetime(self, time_text, current_timezone):
        datetime_h = self.str_to_datetime(time_text)
        return self.datetime_current_timezone_to_utc(datetime_h, current_timezone)

    def str_to_datetime(self, s):
        t = None
        try:
            if s.find('-') > -1:
                if s.find('T') > -1:
                    t = datetime(*map(int, re.split('[-T:]', s)))
                else:
                    t = datetime(*map(int, re.split('[- :]', s)))
            elif s.find('/') > -1:
                t = datetime(*map(int, re.split('[/ :]', s)))
        except Exception as e:
            print('set string to datetime error: %s, error log: %s' % (s, e))

        return t

    @staticmethod
    def datetime_current_timezone_to_utc(datetime_h, current_timezone):
        time_h = datetime_h.replace(tzinfo=tz.gettz(current_timezone))
        return time_h.astimezone(tz.tzutc())

    @staticmethod
    def datetime_naive_add_utc_timezone(datetime_h):
        time_h = datetime_h.replace(tzinfo=tz.tzutc())
        return time_h.astimezone(tz.tzutc())


class WebDriverControl(object):
    def __init__(self):
        super(WebDriverControl, self).__init__()
        self.username = ''
        self.password = ''

    @staticmethod
    def create_driver(option):
        # option.add_argument('headless')
        # option.add_argument("--start-maximized")
        if sys.platform.startswith('win'):
            driver = webdriver.Chrome(chrome_options=option)
        else:
            driver = webdriver.Chrome(const_define.WEB_DRIVER_PATH, chrome_options=option)

        driver.implicitly_wait(10)
        return driver

    def init_driver(self):
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # option.add_argument("--start-maximized")
        return self.create_driver(option)

    def init_driver_headless(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        # option.add_argument("--start-maximized")
        return self.create_driver(option)

    # @staticmethod
    # def load_cookies_to_open_page(drivers, url, cookie_path):
    #     drivers.delete_all_cookies()
    #     drivers.get(url)
    #     time.sleep(1)
    #
    #     with open(cookie_path, 'r', encoding='utf-8') as f:
    #         list_cookies = json.loads(f.read())
    #     # print(list_cookies)
    #     for cookie in list_cookies:
    #         drivers.add_cookie({
    #             'domain': cookie['domain'],
    #             'httpOnly': cookie['httpOnly'],
    #             'secure': cookie['secure'],
    #             'name': cookie['name'],
    #             'value': cookie['value'],
    #             'path': '/'
    #         })
    #         if 'expiry' in cookie:
    #             drivers.add_cookie({
    #                 'expiry': cookie['expiry']
    #             })

    # def renew_cookies_file(self, driver, cookie_path):
    #     driver.delete_all_cookies()
    #     driver.get(setting.LOGIN_URL)
    #     input_message = input("please press enter key for get cookie file when browser ready")
    #     print(input_message)
    #     driver.refresh()
    #     time.sleep(5)
    #
    #     cookies = driver.get_cookies()
    #     json_cookies = json.dumps(cookies)
    #     with open(cookie_path, 'w') as f:
    #         f.write(json_cookies)


class CrawlerByWebDriver(ABC):
    @abstractmethod
    def start_crawl(self, fanpage_dic_ld, form_foldername, q):
        return


def start_crawl(obj, fanpage_dic_ld, form_foldername, q):
    obj.start_crawl(fanpage_dic_ld, form_foldername, q)
    return
