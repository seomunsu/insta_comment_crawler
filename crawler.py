from instagram.instagram_delegate import InstagramDelegate
from util.export_util import export_csv

if __name__ == '__main__':
    delegate = InstagramDelegate()
    instagram_comments = delegate.scrap()
    export_csv(instagram_comments)
