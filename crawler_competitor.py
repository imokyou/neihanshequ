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


class NeihanSpider(object):

    def __init__(self):
        self._db = DBStore()

    def crawl_video(self):
        params = {
            'p': 1,
            'id': ''
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A5000 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CN MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CNw',
            'Cookie': 'PHPSESSID=t7k6tmvsargf4dk3h18jg3ga14'
        }
        while True:
            try:
                logging.info('Crawl video guanzhu...')
                ret = []
                request_url = '{}?{}'.format(API_CP, conbine_params(params))
                resp = get_page(request_url, headers=headers)
                if resp:
                    contents = resp['data']['list']
                    if len(contents) == 0:
                        break
                    for content in contents:
                        info = self._parse_item(content)
                        ret.append(info)
                    self._db.save(ret)
                    params['p'] += 1;
                    logging.info('休息30秒')
                    sleep(60)
                else:
                    break
            except:
                traceback.print_exc()
                break

    def _parse_item(self, data):
        info = self._video_item(data)
        return info


    def _video_item(self, data):
        info = {}
        d = data
        info = {
            'group_id': d['video_video_id'],
            'item_id': d['video_video_id'],
            'video_id': d['video_video_id'],
            'content': d['name'],
            'category_id': '1114',
            'category_name': '内涵有料',
            'url': d['video_url'],
            'cover_image': 'https://xcx.mengjukeji.com/'.d['images'],
            'online_time': data['add_time'],

            'user_id': d['member_id'],
            'user_name': d['nickname'],
            'user_avatar': 'https://xcx.mengjukeji.com/'.d['headimgurl'],

            'play_count': d['view_num'],
            'bury_count': 0,
            'repin_count': 0,
            'share_count': d['forward_num'],
            'digg_count': d['like_num'],
            'comment_count': d['comment_num'],
            'has_comments': 0,
            'comments': json.dumps([]),
            'top_comments': 0,
            'comment_crawled': 0
        }
        info['vurl'] = d['video_url']
        return info


class Crawler(object):

    def run(self):
        logging.info('开始爬内涵了了了了...')
        ps = NeihanSpider()
        ps.crawl_video()

if __name__ == '__main__':
    proxy_crawler = Crawler()
    proxy_crawler.run()
