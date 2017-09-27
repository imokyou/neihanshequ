# coding=utf8
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from time import sleep, time
import json
import traceback
from config import *
from utils import get_page, conbine_params
from db import DBStore


_WORKER_THREAD_NUM = 3
_DB = DBStore()
_PARAMS = {
    "group_id": "70377693537",
    "item_id": "70377693537",

    "ac": "wifi",
    "app_name": "joke_essay",
    "offset": "0",
    "ssmix": "a",
    "device_type": "ONEPLUS A5000",
    "os_api": "25",
    "uuid": "864630039828537",
    "version_code": "660",
    "os_version": "7.1.1",
    "update_version_code": "6603",
    "channel": "oppo-cpa",
    "device_platform": "android",
    "iid": "15475911318",
    "device_brand": "OnePlus",
    "manifest_version_code": "660",
    "version_name": "6.6.0",
    "openudid": "683195cfdb2b2c4c",
    "device_id": "39503669487",
    "count": "20",
    "aid": "7",
    "resolution": "1080*1920",
    "dpi": "480"
}
_API = 'http://is.snssdk.com/neihan/comments/'


def parse_items(resp):
    top_comments = []
    for data in resp['data']['top_comments']:
        info = {
            'group_id': int(data['group_id']),
            'item_id': int(data['group_id']),
            'user_id': int(data['user_id']),
            'user_name': data['user_name'],
            'user_avatar': data['avatar_url'],
            'create_time': data['create_time'],
            'content': data['text'],
            'digg_count': int(data['digg_count']),
            'comments_count': int(data['second_level_comments_count'])
        }
        top_comments.append(info)
    return top_comments


def crawl_comment(video):
    _PARAMS['group_id'] = str(video['group_id'])
    _PARAMS['item_id'] = str(video['group_id'])
    request_url = '{}?{}'.format(_API, conbine_params(_PARAMS))
    resp = get_page(request_url)
    if resp:
        comments = parse_items(resp)
        _DB.save_comment(comments)
        logging.info('{} 热门评论已获取'.format(video['video_id']))
    else:
        logging.info('{} 暂无热门评论'.format(video['video_id']))
    gids = [video['group_id']]
    _DB.video_top_comments_updated(gids)


class Crawler(object):

    def run(self):
        logging.info('开始爬内涵了了了了...')
        pools = Pool(_WORKER_THREAD_NUM)
        while True:
            params = {
                'top_comments': 0,
                'limit': _WORKER_THREAD_NUM
            }
            videos = _DB.get_videos(params)
            pools.map(crawl_comment, videos)
            logging.info('主进程休息 {} 秒后再爬取评论...'.format(CRAWL_PAGE_SLEEP))
            sleep(CRAWL_PAGE_SLEEP)


if __name__ == '__main__':
    proxy_crawler = Crawler()
    proxy_crawler.run()
