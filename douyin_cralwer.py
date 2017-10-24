# coding=utf8
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from time import sleep, time
import json
import traceback
from config import *
from utils import get_page, conbine_params
from db import DBStore


_WORKER_THREAD_NUM = 1


# api = 'http://aweme.snssdk.com/aweme/v1/feed/?type=0&max_cursor=0&min_cursor=0&count=6&retry_type=retry_http&iid=16259948390&device_id=40113379514&ac=wifi&channel=oppo&aid=1128&app_name=aweme&version_code=159&version_name=1.5.9&device_platform=android&ssmix=a&device_type=ONEPLUS+A5000&device_brand=OnePlus&os_api=25&os_version=7.1.1&uuid=99000979108573&openudid=683195cfdb2b2c4c&manifest_version_code=159&resolution=1080*1920&dpi=480&update_version_code=1592&ts=1508203925&app_type=normal&as=a125d58e9599495d85&cp=5a9795595e59eadee1'

class DouyinMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs['__CrawlFuncCount__'] = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                attrs['__CrawlFuncCount__'] = attrs['__CrawlFuncCount__'] + 1
        return type.__new__(cls, name, bases, attrs)


class DouyinSpider(object):
    __metaclass__ = DouyinMetaClass

    def __init__(self):
        self._db = DBStore()

    def get_raw_items(self, callback):
        items = []
        for item in eval("self.{}()".format(callback)):
            items.append(item)
        self._db.save(items)

    def crawl_video(self, content_type=None, category_id=None):
        try:
            logging.info('Crawl video...')
            ret = []
            params = {
                "ts": str(int(time())),
                "ac": "wifi",
                "app_name": "aweme",
                "ssmix": "a",
                "as": "a1b5582e077999cb84",
                "device_type": "ONEPLUS A5000",
                "cp": "839e9356714de4bee1",
                "os_api": "25",
                "user_id": "56964089429",
                "uuid": "99000979108573",
                "version_code": "159",
                "os_version": "7.1.1",
                "retry_type": "retry_http",
                "channel": "oppo",
                "device_platform": "android",
                "iid": "16259948390",
                "device_brand": "OnePlus",
                "manifest_version_code": "159",
                "app_type": "normal",
                "version_name": "1.5.9",
                "openudid": "683195cfdb2b2c4c",
                "update_version_code": "1592",
                "device_id": "40113379514",
                "aid": "1128",
                "resolution": "1080*1920",
                "dpi": "480"
            }

            request_url = '{}?{}'.format(API_DOUYIN_V1, conbine_params(params))
            print request_url

            resp = get_page(request_url)
            if resp:
                print resp
                contents = resp['aweme_list']
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
        d = data
        info = {
            'source': 'douyin',
            'group_id': d['aweme_id'],
            'item_id': d['aweme_id'],
            'video_id': d['video']['play_addr']['uri'],
            'content': d['desc'],
            'category_id': '',
            'category_name': '',
            'url': d['video']['play_addr']['url_list'][0],
            'cover_image': d['video']['cover']['url_list'][0],
            'online_time': d['create_time'],

            'user_id': d['author']['uid'],
            'user_name': d['author']['nickname'],
            'user_avatar': d['author']['avatar_larger']['url_list'][0],

            'play_count': d['statistics']['play_count'],
            'bury_count': 0,
            'repin_count': 0,
            'share_count': d['statistics']['share_count'],
            'digg_count': d['statistics']['digg_count'],
            'comment_count': d['statistics']['comment_count'],
            'has_comments': 0,
            'comments': '',
            'top_comments': 0
        }
        info['vurl'] = d['video']['play_addr']['uri']
        return info


class Crawler(object):

    def run(self):
        logging.info('开始爬抖音了了了了...')
        pools = Pool(_WORKER_THREAD_NUM)
        ps = DouyinSpider()
        while True:
            pools.map(ps.get_raw_items, ps.__CrawlFunc__)
            logging.info('主进程休息 {} 秒后再爬取...'.format(CRAWL_PAGE_SLEEP))
            sleep(CRAWL_PAGE_SLEEP)

if __name__ == '__main__':
    proxy_crawler = Crawler()
    proxy_crawler.run()
