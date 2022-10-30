from typing import List
from time import time

from instagram import InstagramCrawler
from instagram.data import InstagramPost
from instagram.data import InstagramComment
from util import create_logger
from util import randomized_sleep


class InstagramDelegate:
    def __init__(self):
        self.__instagram_crawler = InstagramCrawler()
        self.__profiles = self.__instagram_crawler.get_option().collect.profiles
        self.__log = create_logger(self.__class__.__name__)

    def scrap(self):
        now = time()

        self.__instagram_crawler.login()
        instagram_posts: List[InstagramPost] = self.__get_current_posts_by_profiles()
        instagram_comments = self.__get_comments_by_posts(instagram_posts)
        self.__instagram_crawler.close()

        self.__log.info('result elapsed : {}s'.format(time() - now))

        return instagram_comments

    def __get_current_posts_by_profiles(self) -> List[InstagramPost]:
        now = time()
        instagram_posts: List[InstagramPost] = []
        for profile in self.__profiles:
            if self.__instagram_crawler.move_to_profile_page(profile):
                instagram_posts.extend(self.__get_current_posts_by_profile(profile))
            randomized_sleep(0.5)

        self.__log.info('get current posts result elapsed : {}s'.format(time() - now))

        return instagram_posts

    def __get_current_posts_by_profile(self, profile) -> List[InstagramPost]:
        instagram_posts: List[InstagramPost] = []
        for post in self.__instagram_crawler.get_current_posts():
            instagram_posts.append(InstagramPost(profile=profile, post=post))

        return instagram_posts

    def __get_comments_by_posts(self, instagram_posts: List[InstagramPost]) -> List[InstagramComment]:
        now = time()
        instagram_comments = []
        for instagram_post in instagram_posts:
            self.__log.info(f'get comments -> profile={instagram_post.profile}, post={instagram_post.post}')
            if self.__instagram_crawler.move_to_comment_page(instagram_post.post):
                instagram_comments.extend(self.__get_comments_by_post(instagram_post))
            randomized_sleep(0.5)

        self.__log.info('get comments result elapsed : {}s'.format(time() - now))

        return instagram_comments

    def __get_comments_by_post(self, instagram_post: InstagramPost) -> List[InstagramComment]:
        instagram_comments = []
        for comment in self.__instagram_crawler.get_comments():
            instagram_comments.append(
                InstagramComment(profile=instagram_post.profile, post=instagram_post.post, comment=comment)
            )

        return instagram_comments
