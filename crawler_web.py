# coding=utf8
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from time import sleep, time
import json
import traceback
from config import *
from utils import get_page, conbine_params
from db import DBStore


_WORKER_THREAD_NUM = 1


class NeihanMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs['__CrawlFuncCount__'] = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                attrs['__CrawlFuncCount__'] = attrs['__CrawlFuncCount__'] + 1
        return type.__new__(cls, name, bases, attrs)


class NeihanSpider(object):
    __metaclass__ = NeihanMetaClass

    def __init__(self):
        self._db = DBStore()

    def get_raw_items(self, callback):
        items = []
        for item in eval("self.{}()".format(callback)):
            items.append(item)
        self._db.save_web(items)

    def crawl_video(self, content_type=None, category_id=None):
        try:
            logging.info('Crawl video...')
            ret = []
            request_url = API_WEB
            resp = get_page(request_url, headers=HEADERS)
            if resp:
                contents = resp['data']['data']
                for content in contents:
                    info = self._parse_item(content)
                    print info
                    ret.append(info)
        except:
            traceback.print_exc()
        return ret

    def _parse_item(self, data):
        info = {}
        group = data.get('group', '')
        if not group:
            return info
        if 'is_video' in data['group'] and data['group']['is_video'] == 1:
            info = self._video_item(data)
        return info

    def _video_item(self, data):
        info = {}
        d = data['group']
        info = {
            'group_id': d['group_id'],
            'item_id': d['group_id'],
            'video_id': d['uri'],
            'content': d['content'],
            'category_id': d['category_id'],
            'category_name': d['category_name'],
            'url': d['origin_video']['url_list'][0]['url'],
            'cover_image': d['large_cover']['url_list'][0]['url'],
            'online_time': data['online_time'],

            'user_id': d['user']['user_id'],
            'user_name': d['user']['name'],
            'user_avatar': d['user']['avatar_url'],

            'play_count': d['play_count'],
            'bury_count': d['bury_count'],
            'repin_count': d['repin_count'],
            'share_count': d['share_count'],
            'digg_count': d['digg_count'],
            'comment_count': d['comment_count'],
            'has_comments': int(d['has_comments']),
            'comments': json.dumps(data['comments']),
            'top_comments': 0
        }
        info['vurl'] = 'http://i.snssdk.com/neihan/video/playback/?video_id={}&quality=origin&line=0&is_gif=0.mp4'.format(d['uri'])
        return info


class Crawler(object):

    def run(self):
        logging.info('开始爬内涵了了了了...')
        pools = Pool(_WORKER_THREAD_NUM)
        ps = NeihanSpider()
        while True:
            pools.map(ps.get_raw_items, ps.__CrawlFunc__)
            logging.info('主进程休息 {} 秒后再爬取...'.format(CRAWL_PAGE_SLEEP))
            sleep(CRAWL_PAGE_SLEEP)

if __name__ == '__main__':
    proxy_crawler = Crawler()
    proxy_crawler.run()
