from datetime import datetime
import os

VERSION = "v1.0.1"
TITLE = 'AJ FanPage Crawler - %s' % VERSION
WEB_DRIVER_SHOW = True
WEB_DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
# 指定要抓到那一天
# DATETIME_LIMIT = '2018-01-1 00-00-00'
DATETIME_FORMAT = "%Y-%m-%d %H-%M-%S"

TODAY_DATE_DIC = {}
today_daytime = datetime.now()
TODAY_DATE_DIC['YEAR'] = (today_daytime.strftime("%Y"))
TODAY_DATE_DIC['MON'] = (today_daytime.strftime("%m"))
TODAY_DATE_DIC['DAY'] = (today_daytime.strftime("%d"))

SETTING_NAME = "Settings.ini"
FANPAGE_NAME = "fanpage.sdb"
FANPAGE_GET_LIST = "fanpageGet.txt"

# https://developers.facebook.com/tools/explorer/
IG_LOGIN_URL = r'https://www.instagram.com/accounts/login/'

ICON_MAIN_PATH = os.path.join(os.getcwd(), 'icons', 'main.ico')

form_template_need_repeat = \
'    <tr>\n'\
'        <th align="center">{{post_date}}</th>\n'\
'        <th align="center">{{post_content}}</th>\n'\
'        <th align="center">{{post_likes}}</th>\n'\
'        <td align="center">{{post_shares}}</td>\n'\
'        <th align="center">{{post_comments}}</th>\n\n'\
'        <th align="center">{{post_id}}</th>\n\n'\
'    </tr>\n'\
'{{next_item}}'
