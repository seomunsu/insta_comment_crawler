import pandas as pd
import datetime

from typing import List
from datetime import datetime

from instagram.data import InstagramComment


def export_excel(instagram_comments: List[InstagramComment]):
    data_frame = pd.DataFrame(instagram_comments, columns=['profile', 'post', 'comment'])
    today = datetime.today()
    filename = f'{today}_instagram.xlsx'
    data_frame.to_excel(filename, index=False, header=True, engine='xlsxwriter')


def export_csv(instagram_comments: List[InstagramComment]):
    data_frame = pd.DataFrame(instagram_comments, columns=['profile', 'post', 'comment'])
    today = datetime.today()

    filename = f'{today}_instagram.csv'
    data_frame.to_csv(filename, index=False, header=True, encoding='utf-8-sig')
