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
    "device_type": "SM-G9350",
    "os_api": "24",
    "uuid": "356156072316243",
    "version_code": "661",
    "os_version": "7.0",
    "update_version_code": "6613",
    "channel": "samsungapps",
    "device_platform": "android",
    "iid": "15628443576",
    "device_brand": "samsung",
    "manifest_version_code": "661",
    "version_name": "6.6.1",
    "openudid": "a7f0b3b274b19977",
    "device_id": "39614193210",
    "count": "20",
    "aid": "7",
    "resolution": "1440*2560",
    "dpi": "640"
}
_API = 'http://is.snssdk.com/neihan/comments/'
_CRAWL_PAGE_SLEEP = 4


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
            'comment_count': int(data['second_level_comments_count'])
        }
        top_comments.append(info)
        if len(top_comments) >= 5:
            break
    return top_comments


def crawl_comment(video):
    _PARAMS['group_id'] = str(video['group_id'])
    _PARAMS['item_id'] = str(video['group_id'])
    request_url = '{}?{}'.format(_API, conbine_params(_PARAMS))
    resp = get_page(request_url)
    if resp:
        comments = parse_items(resp)
        _DB.save_comment(comments)
        logging.info('{} 热门评论已获取, 共{}个评论'.format(video['video_id'], len(comments)))
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
            sleep(_CRAWL_PAGE_SLEEP)


if __name__ == '__main__':
    proxy_crawler = Crawler()
    proxy_crawler.run()
