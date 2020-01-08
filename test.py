from crawler import WebDriverControl
from crawler_ig import CrawlerIG

dic = {"麵包貓": r"https://www.instagram.com/corocoro_coronya/"}
url = r"https://www.instagram.com/corocoro_coronya/"
# web_driver_h = WebDriverControl()
# web_drive = web_driver_h.init_driver()

crawler = CrawlerIG()
crawler.login_to_ig("username", "password")


def test_one_post():
    crawler.go_to_crawl_main_page(url)
    article = crawler.get_article_element()
    rows = crawler.get_row_list_by_article(article)
    posts = crawler.get_post_list_by_row(rows[0])
    post = posts[0]
    like_message = crawler.get_post_like_and_message_num_by_mouse_move(post)
    post.click()
    content_text = crawler.get_post_content()
    post_time = crawler.get_post_time()
    image_url = crawler.get_post_picture()
    reply_all_text = crawler.get_all_post_reply()
    print(content_text)
    print('like: ' + like_message[0] + ' message: ' + like_message[1])
    print(post_time)
    print(image_url)
    print(reply_all_text)
    print("==============")


def test_crawler_all():
    crawler.start_crawl_ig_article_all(url)


if __name__ == '__main__':
    test_one_post()
    # test_crawler_all()
