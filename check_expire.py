# coding=utf8
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
import requests
from time import sleep, time, localtime, strftime
import json
import traceback
from config import *
from db import DBStore


_WORKER_THREAD_NUM = 4
_SLEEP_SECOND = 2
_DB = DBStore()


def format_time(t):
    timeArray = localtime(t)
    otherStyleTime = strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def checker():
    expire_num = 0
    total_num = 0
    page = 1
    while True:
        params = {
            'order': 'asc',
            'limit': 100,
            'page': page,
            # 'is_expired': 0,
            # 'online_time': 1507132800
        }
        urls = _DB.get_videos(params)
        if len(urls) == 0:
            break
        total_num += len(urls)
        page += 1
        gids = []
        for u in urls:
            r = requests.head(u['vurl'].replace('timestamp', str(time())), headers=HEADERS)
            resp = requests.head(r.headers['location'], headers=HEADERS)
            print resp, resp.headers
            if resp.status_code == 403:
                expire_num += 1
                if u['group_id'] not in gids:
                    gids.append(u['group_id'])
            if resp.status_code == 200:
                if int(resp.headers['Content-Length']) < 1000:
                    expire_num += 1
                    if u['group_id'] not in gids:
                        gids.append(u['group_id'])
            logging.info('休息{}秒'.format(_SLEEP_SECOND))
            sleep(_SLEEP_SECOND)
        logging.info('{} {}'.format(u['id'], format_time(u['online_time'])))
        logging.info('当前页码: {}, 当前失效链接数: {}, 当前总链接数: {}'.format(page-1, expire_num, total_num))
        _DB.video_expire_updated(gids)
        # logging.info('休息{}秒'.format(_SLEEP_SECOND))
        # sleep(_SLEEP_SECOND)
    logging.info('总失效的链接数为: {}, 总链接数: {}'.format(expire_num, total_num))


if __name__ == '__main__':
    checker()
