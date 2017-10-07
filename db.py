# coding=utf8
import config
from models import *


class DBStore(object):
    def __init__(self):
        database = config.MYSQLDB
        db_url = 'mysql+mysqldb://%s:%s@%s/%s?charset=utf8mb4' % \
            (database['user'],
             database['passwd'],
             database['host'],
             database['db_name'])
        self.mgr = Mgr(create_engine(db_url, pool_recycle=10))

    def save(self, items):
        for k, v in enumerate(items):
            self.mgr.add_video(v)

    def save_web(self, items):
        for k, v in enumerate(items):
            self.mgr.add_video_web(v)

    def save_comment(self, items):
        for k, v in enumerate(items):
            self.mgr.add_comment(v)

    def get_videos(self, params=None):
        if not params:
            params = {}
        return self.mgr.get_videos(params)

    def video_top_comments_updated(self, gids):
        self.mgr.video_top_comments_updated(gids)

    def video_expire_updated(self, gids):
        self.mgr.video_expire_updated(gids)

    def save_csv(self, items):
        for k, v in enumerate(items):
            pass

    def save_txt(self, items):
        pass
