import requests
from dateutil.parser import parse
import shutil
from datetime import datetime
import const_define
import os
from crawler import WebDriverControl
from crawler import CrawlerByWebDriver
from crawler import DateTimeControl
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re

log_queue = None


class CrawlerIG(CrawlerByWebDriver):
    def __init__(self):
        super(CrawlerIG, self).__init__()
        web_driver_h = WebDriverControl()
        if const_define.WEB_DRIVER_SHOW:
            self.web_driver = web_driver_h.init_driver()
        else:
            self.web_driver = web_driver_h.init_driver_headless()
        self.date_time_control = DateTimeControl()

    def start_crawl(self, fanpage_dic_ld, form_foldername, queue_h):
        global log_queue
        if queue_h:
            log_queue = queue_h
        self.start_to_crawl_fanpage(fanpage_dic_ld, form_foldername)

    def start_to_crawl_fanpage(self, fanpage_dic_ld, form_foldername):
        self.print_log('info', 'start')
        # -----Start to crawl fan page data-----
        self.login_to_ig()

        # for fanpage_name, fanpage_url in fanpage_dic_ld.items():
        #     # print('%s - %s' % (fanpage_name, fanpage_id))
        #     # print("開始抓取粉絲頁: %s" % fanpage_name)
        #     queue_h.put(['info', "開始抓取粉絲頁: %s" % fanpage_name])
        #     posts = self.start_crawl_ig(web_drive, fanpage_url)
        #     # if posts:
        #     #     # self.setlog("抓取結束!產生報表中", "info2")
        #     #     queue_h.put(['info2', "抓取結束! 產生報表中"])
        #     #     # 檔案輸出
        #     #     create_form(posts, fanpage_name, form_foldername, queue_h)
        #     # else:
        #     #     # print("粉絲頁: %s 讀取失敗, 換個token再試試吧" % fanpage_name)
        #     #     queue_h.put(['error', "粉絲頁: %s 讀取失敗, 換個token再試試吧" % fanpage_name])

        # print('所有工作已完成!!')
        self.web_driver.quit()
        # queue_h.put(['end', '所有工作已完成!!'])
        self.print_log('end', '所有工作已完成!!')

    def close_message_dialog(self):
        try:
            self.web_driver.find_element_by_class_name("HoLwm")
            skip_button_elem = self.web_driver.find_element_by_class_name("HoLwm")
            skip_button_elem.click()
        except Exception as e:
            print('dialog not find, skip it: %s' % e)

    def close_login_dialog(self):
        login_button = self.web_driver.find_element_by_class_name("dCJp8")
        login_button.click()

    def start_crawl_ig_article_all(self, fanpage_url):
        self.print_log('info2', '開啟: %s' % fanpage_url)
        self.go_to_crawl_main_page(fanpage_url)

        page_count = 0
        while page_count <= 3:
            page_count += 1
            self.crawl_ig_article_one_page()

        return ''

    def go_to_crawl_main_page(self, fanpage_url):
        self.close_message_dialog()
        self.web_driver.get(fanpage_url)
        # self.close_login_dialog()

    def crawl_ig_article_one_page(self):
        article = self.get_article_element()
        rows = self.get_row_list_by_article(article)
        for row in rows:
            posts = self.get_post_list_by_row(row)
            count = 0
            for post in posts:
                count += 1
                self.print_log('info', count)
                like_message = self.get_post_like_and_message_num_by_mouse_move(post)
                print('like: ' + like_message[0] + ' message: ' + like_message[1])
                # post.click()
                # content_dic = self.get_post_content()
                #
                # post_close_button_elem = self.web_driver.find_element_by_class_name("ckWGn")
                # post_close_button_elem.click()
                # # self.web_driver.send_keys(Keys.ESCAPE)

                # self.print_log('info', content_dic)

    def get_article_element(self):
        return self.web_driver.find_element_by_xpath(
                                        "//*[@id='react-root']/section/main/div/div[3]/article[2]/div[1]/div")

    def get_row_list_by_article(self, article):
        return article.find_elements_by_class_name("Nnq7C")

    def get_post_list_by_row(self, row):
        return row.find_elements_by_class_name("v1Nh3")

    def get_post_picture(self):
        first_image = self.web_driver.find_element_by_class_name("KL4Bh")
        first_image_url = first_image.find_element_by_tag_name("img")
        first_image_url = first_image_url.get_attribute("src")
        return first_image_url

    def get_post_content(self):
        content_ele = self.web_driver.find_element_by_class_name("C7I1f")
        content = content_ele.find_element_by_class_name("C4VMK")
        content_text = content.find_element_by_tag_name("span").text
        return content_text

    def get_post_time(self):
        post_ele = self.web_driver.find_element_by_class_name("_1o9PC")
        post_time = post_ele.get_attribute('datetime')
        post_time = re.sub('.000Z', '', post_time)
        return self.date_time_control.change_string_to_utc_datetime(post_time, 'Asia/Taipei')

    def get_all_post_reply(self):
        post_all_reply = []
        reply_eles = self.web_driver.find_elements_by_class_name("Mr508")
        for reply_ele in reply_eles:
            reply = reply_ele.find_element_by_class_name("C4VMK")
            reply_dic = self.get_each_post_reply_data(reply)
            post_all_reply.append(reply_dic)
        return post_all_reply

    def get_each_post_reply_data(self, reply_ele):
        reply_dic = {'reply_author': reply_ele.find_element_by_class_name("_6lAjh").text,
                     'reply_content': reply_ele.find_element_by_tag_name("span").text,
                     'reply_time': self.get_reply_time(reply_ele)
                     }
        return reply_dic

    def get_reply_time(self, reply_ele):
        reply_time_ele = reply_ele.find_element_by_tag_name("time")
        reply_time = reply_time_ele.get_attribute('datetime')
        reply_time = re.sub('.000Z', '', reply_time)
        return self.date_time_control.change_string_to_utc_datetime(reply_time, 'Asia/Taipei')

    def get_post_like_and_message_num_by_mouse_move(self, post):
        ActionChains(self.web_driver).move_to_element(post).perform()
        like_and_message_num = post.find_element_by_class_name("qn-0x")
        like_and_message_num_ele = like_and_message_num.find_elements_by_class_name("-V_eO")
        like_ele = like_and_message_num_ele[0]
        like_num = like_ele.find_element_by_tag_name("span").text
        message_ele = like_and_message_num_ele[1]
        message_num = message_ele.find_element_by_tag_name("span").text
        like_message = [like_num, message_num]
        return like_message

    def login_to_ig(self, username, password):
        self.print_log('info', '登入IG')
        self.web_driver.get(const_define.IG_LOGIN_URL)
        account_elem = self.web_driver.find_element_by_name("username")
        account_elem.send_keys(username)
        password_elem = self.web_driver.find_element_by_name("password")
        password_elem.send_keys(password)
        login_button_elem = self.web_driver.find_element_by_class_name("y3zKF")
        login_button_elem.click()

    def print_log(self, log_type, message):
        return
        if log_queue:
            log_queue.put([log_type, message])
        else:
            print(message)

    def start_crawl_ig_old(token, fanpage_id, datetime_limt, queue_h):
        # print(token)
        # 建立空的list
        posts = []
        try:
            # 抓取貼文時間、ID、內文、分享內容
            res = requests.get('https://graph.facebook.com/v2.11/{}/posts?limit=100&access_token={}'.format(fanpage_id, token))
        except:
            # self.setlog("讀取失敗", "error")
            return

        page = 1
        while 'paging' in res.json():
            # self.setlog("正在抓取第%d頁" % page, "info2")
            # print('正在抓取第%d頁' % page)
            post_count = 0
            for post in res.json()['data']:
                post_count += 1
                queue_h.put(['info2', '正在抓取第%d頁, 第%d篇貼文' % (page, post_count)])

                post_date = parse(post['created_time'])
                post_date = post_date.replace(tzinfo=None)
                if post_date < datetime.strptime(datetime_limt, const_define.DATETIME_FORMAT):
                    return posts

                # 透過貼文ID來抓取讚數與分享數
                try:
                    res2 = requests.get('https://graph.facebook.com/v2.11/{}?fields=comments.limit(0).summary(true),likes.limit(0).summary(true), shares&access_token={}'.format(post['id'], token))
                except:
                    # print('粉絲頁讀取失敗, 換個token再試一次吧')
                    queue_h.put(['error', "粉絲頁讀取失敗, 換個token再試試吧"])
                    return

                # 留言數
                if 'comments' in res2.json():
                    comments = res2.json()['comments']['summary'].get('total_count')
                else:
                    comments = 0

                # 按讚數
                if 'likes' in res2.json():
                    likes = res2.json()['likes']['summary'].get('total_count')
                else:
                    likes = 0

                # 分享數
                if 'shares' in res2.json():
                    shares = res2.json()['shares'].get('count')
                else:
                    shares = 0

                temp_dic = {}
                temp_dic['date'] = parse(post['created_time'])
                temp_dic['content'] = str(post.get('message'))
                temp_dic['likes'] = likes
                temp_dic['shares'] = shares
                temp_dic['comments'] = comments
                temp_dic['id'] = post['id']

                posts.append(temp_dic)

            if 'next' in res.json()['paging']:
                res = requests.get(res.json()['paging']['next'])
                page += 1
            else:
                return posts


    def store_file_to_folder(file, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        shutil.copy2(file, folder_path)


    def create_form(posts, fanpage_name, form_foldername, queue_h):
        # copy temp.html to log folder
        store_file_to_folder('temp_form.xls', form_foldername)
        os.rename(('%s\\temp_form.xls' % form_foldername), ('%s\\%s.xls' % (form_foldername, fanpage_name)))
        excel_full_path = ('%s\\%s.xls' % (form_foldername, fanpage_name))

        # write to html
        try:
            readfile_excel_lh = open(excel_full_path, 'r', encoding='utf8')
            excel_content = str(readfile_excel_lh.read())
            readfile_excel_lh.close()
        except Exception as ex:
            queue_h.put(['error', "Error! 讀取excel檔發生錯誤!請確認%s目錄有temp_form.xls且內容正確" % const_define.TITLE])
            return

        if posts:
            for post in posts:
                excel_content = excel_content.replace('{{next_item}}', const_define.form_template_need_repeat)

                excel_content = excel_content.replace('{{post_date}}', str(post['date']))
                excel_content = excel_content.replace('{{post_content}}', str(post['content']))
                excel_content = excel_content.replace('{{post_likes}}', str(post['likes']))
                excel_content = excel_content.replace('{{post_shares}}', str(post['shares']))
                excel_content = excel_content.replace('{{post_comments}}', str(post['comments']))
                excel_content = excel_content.replace('{{post_id}}', str(post['id']))

            excel_content = excel_content.replace('{{next_item}}', '')

            try:
                writhfile_excel_lh = open(excel_full_path, 'w', encoding='utf8')
                writhfile_excel_lh.write(excel_content)
                writhfile_excel_lh.close()
                # print("已產生excel檔, 路徑:" + excel_full_path)
                queue_h.put(['info2', "已產生excel檔, 路徑:%s" % excel_full_path])

            except Exception as ex:
                # print("Error! 寫入excel檔發生錯誤!請確認目錄有temp_form.xls且內容正確", 'error')
                queue_h.put(['error', "Error! 寫入excel檔發生錯誤!請確認目錄有temp_form.xls且內容正確"])
                return
