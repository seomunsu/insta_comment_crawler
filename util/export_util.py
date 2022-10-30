import pandas as pd

from typing import List

from instagram.data import InstagramComment
from util.time_util import today_datetime
from util.logger_util import create_logger

logger = create_logger('export_util')


def export_excel(instagram_comments: List[InstagramComment]):
    logger.info('start')
    data_frame = pd.DataFrame(instagram_comments, columns=['profile', 'post', 'comment'])
    filename = f'{today_datetime()}_instagram.xlsx'
    data_frame.to_excel(filename, index=False, header=True, engine='xlsxwriter')
    logger.info('end')


def export_csv(instagram_comments: List[InstagramComment]):
    logger.info('start')
    data_frame = pd.DataFrame(instagram_comments, columns=['profile', 'post', 'comment'])
    filename = f'{today_datetime()}_instagram.csv'
    data_frame.to_csv(filename, index=False, header=True, encoding='utf-8-sig')
    logger.info('end')
