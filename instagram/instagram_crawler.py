import unicodedata

from bs4 import BeautifulSoup
from time import sleep

from tqdm import tqdm
from core import Crawler
from exception import NotFoundAttributeException
from exception import RetryException
from util import retry_wrap
from util import randomized_sleep
from util import create_logger
from consts import instagram_consts


class InstagramCrawler:
    def __init__(self):
        self.__crawler = Crawler()
        self.__option = self.__crawler.get_option()
        self.__log = create_logger(self.__class__.__name__)

    def close(self):
        self.__crawler.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__crawler.close()

    def get_option(self):
        return self.__option

    def login(self):
        self.__log.info('start')
        crawler = self.__crawler
        crawler.get(instagram_consts.LOGIN_URL)
        crawler.find_one(instagram_consts.LOGIN_INPUT_USERNAME)\
            .send_keys(self.__option.instagram.login.username)
        crawler.find_one(instagram_consts.LOGIN_INPUT_PASSWORD)\
            .send_keys(self.__option.instagram.login.password)
        crawler.find_one(instagram_consts.LOGIN_BUTTON_SUBMIT).click()

        self.__check_stay_on_login_screen()
        self.__check_stay_on_login_info_save_screen()

        self.__log.info('end')

    def move_to_profile_page(self, profile):
        self.__log.info(f'profile : {profile}')
        self.__crawler.get(f'{instagram_consts.URL}/{profile}')

        try:
            self.__check_load_profile()
            return True
        except NotFoundAttributeException:
            self.__log.info(f' └─ profile({profile}) not found username is pass')
            self.__log.info('end')
            return False

    def move_to_comment_page(self, post):
        self.__crawler.get(f'{instagram_consts.URL}{post}comments')

        try:
            sleep(2)
            self.__check_load_comment()
            return True
        except NotFoundAttributeException:
            self.__log.info(f' └─ post({post}) not found comments is pass')
            self.__log.info('end')
            return False

    def get_current_posts(self):
        timeout = 20
        wait_time = 5
        pre_post_count = 0
        short_codes = set()
        limit = self.__option.collect.items.post.recentCount

        pbar = tqdm(total=limit)
        pbar.set_description('Fetching posts')

        while len(short_codes) < limit and wait_time < timeout:
            post_count, wait_time = self.fetch(pbar, short_codes, pre_post_count, wait_time)
            pbar.update(post_count - pre_post_count)
            pre_post_count = post_count

        pbar.close()
        self.__log.info('Done Fetched %s posts.' % (min(len(short_codes), limit)))

        return list(short_codes)[:limit]

    def fetch(self, pbar, short_codes, pre_post_count, wait_time):
        soup = BeautifulSoup(self.__crawler.page_source(), 'html.parser')
        hrefs = soup.article.find_all('a', href=True)
        for a in hrefs:
            short_code = a['href']
            if short_code not in short_codes:
                short_codes.add(short_code)

        if pre_post_count == len(short_codes):
            pbar.set_description('Wait for %s sec' % wait_time)
            sleep(wait_time)
            pbar.set_description('Fetching...')

            wait_time *= 2
            self.__crawler.scroll_up(300)
        else:
            wait_time = 1

        pre_post_count = len(short_codes)
        self.__crawler.scroll_down()

        return pre_post_count, wait_time

    def get_comments(self):
        comments = []
        soup = BeautifulSoup(self.__crawler.page_source(), 'html.parser')
        body = soup.body
        all_ul = body.find_all(instagram_consts.TAG_UL, instagram_consts.COMMENTS_CLASS)

        for ul in all_ul[:self.__option.collect.items.comment.recentCount]:
            comments.append(
                unicodedata.normalize('NFC', ul.find(instagram_consts.TAG_SPAN,
                                                     instagram_consts.COMMENT_DETAIL_CLASS).getText())
            )

        return comments

    def __count_comments(self):
        soup = BeautifulSoup(self.__crawler.page_source(), 'html.parser')
        body = soup.body

        return len(body.find_all(instagram_consts.TAG_UL, instagram_consts.COMMENTS_CLASS))

    def __check_collect_comment_limit(self):
        if self.__count_comments() >= self.__option.collect.items.comment.recentCount:
            return True
        return False

    @retry_wrap(attempt=15, wait=1, retryable_exceptions=RetryException)
    def __check_stay_on_login_screen(self):
        if self.__crawler.find_one(instagram_consts.LOGIN_INPUT_USERNAME):
            raise RetryException()
        else:
            return True

    @retry_wrap(attempt=10, wait=1, retryable_exceptions=RetryException)
    def __check_stay_on_login_info_save_screen(self):
        if self.__crawler.find_xpath(instagram_consts.LOGIN_INFO_SAVE_NEXT):
            self.__crawler.find_xpath(instagram_consts.LOGIN_INFO_SAVE_NEXT).click()
            raise RetryException()
        else:
            return True

    @retry_wrap(attempt=5, wait=1, retryable_exceptions=RetryException)
    def __check_load_profile(self):
        if self.__crawler.find_tag(instagram_consts.TAG_ARTICLE):
            return True
        else:
            raise RetryException()

    @retry_wrap(attempt=9999, wait=1, retryable_exceptions=RetryException)
    def __check_load_comment(self):
        self.__crawler.scroll_down(0.5)
        if self.__crawler.find_one_xpath(instagram_consts.TAG_BUTTON):
            try:
                self.__crawler.find_one_xpath(instagram_consts.TAG_BUTTON).click()
            except Exception as e:
                self.__log.info(f'[Throws an exception ans passes] message : {str(e)}')
                return True

            if self.__check_collect_comment_limit():
                # todo : log limit
                return True

            randomized_sleep(2)
            raise RetryException()
        else:
            return True

