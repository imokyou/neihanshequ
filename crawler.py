# coding=utf8
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from time import sleep, time
import json
import traceback
from config import *
from utils import get_page, conbine_params
from db import DBStore


_WORKER_THREAD_NUM = 4


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
        self._db.save(items)

    def crawl_video(self):
        return self._crawler(content_type='-104')

    def crawl_video_dx(self):
        return self._crawler(category_id="189")

    def crawl_video_mt(self):
        return self._crawler(category_id="109")

    def crawl_video_ns(self):
        return self._crawler(category_id="12")

    def _crawler(self, content_type=None, category_id=None):
        try:
            logging.info('Crawl video...')
            ret = []
            params = {
                "min_time": str(int(time())),
                "resolution": "1440*2560",
                "screen_width": "1440",

                "aid": "7",
                "device_brand": "samsung",
                "device_id": "39614193210",
                "device_type": "SM-G9350",
                "iid": "15628443576",
                "openudid": "a7f0b3b274b19977",
                "uuid": "356156072316243",

                "ac": "wifi",
                "am_city": "广州市",
                "am_latitude": "23.122795",
                "am_loc_time": "1506562776598",
                "am_longitude": "113.407836",
                "app_name": "joke_essay",
                "channel": "samsungapps",
                "count": "30",
                "device_platform": "android",
                "double_col_mode": "0",
                "dpi": "640",
                "essence": "1",

                "latitude": "23.07214716",
                "local_request_tag": "1506562863504",
                "longitude": "113.40226613",
                "manifest_version_code": "661",
                "message_cursor": "-1",
                "mpic": "1",

                "os_api": "24",
                "os_version": "7.1.1",
                "ssmix": "a",
                "update_version_code": "6613",
                "version_code": "661",
                "version_name": "6.6.1",
                "video_cdn_first": "1",
                "webp": "1"
            }
            if content_type:
                params['content_type'] = str(content_type)
            if category_id:
                params['category_id'] = str(category_id)
                request_url = '{}?{}'.format(API_V2, conbine_params(params))
            else:
                request_url = '{}?{}'.format(API_V1, conbine_params(params))
            resp = get_page(request_url)
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
            'video_id': d['video_id'],
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
