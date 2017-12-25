# coding=utf8
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from time import sleep, time
from random import randrange
import json
import traceback
from config import *
from utils import get_page, conbine_params
from db import DBStore
import uploadImg


_WORKER_THREAD_NUM = 1


class NeihanSpider(object):

    def __init__(self):
        self._db = DBStore()

    def crawl_video(self):
        params = {
            'p': '1',
            'id': ''
        }
        headers = {
            'User-Agent':'Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A5000 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile MQQBrowser/6.2 TBS/043722 Safari/537.36 MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CN MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CN',
            'Cookie': 'PHPSESSID=t7k6tmvsargf4dk3h18jg3ga14',
            'Accept-Encoding': 'gzip',
            'referer': 'https://servicewechat.com/wxec920bf7a9fd3d8a/1/page-frame.html',
            'cookie': 'PHPSESSID=3057hmvun0u5s6onefg0re55s2',
            'content-type': 'application/json',
            'Host': 'v-api.mengjukeji.com',
        }
        while True:
            try:
                logging.info('Crawl video guanzhu...')
                ret = []
                request_url = '{}?{}'.format(API_CP, conbine_params(params))
                params['p'] = str(int(params['p']) + 1);
                print request_url
                resp = get_page(request_url, headers=headers)
                if resp:
                    contents = resp['data']['list']
                    if len(contents) == 0:
                        break
                    for content in contents:
                        info = self._parse_item(content)
                        print info
                        ret.append(info)
                    self._db.save(ret)
                    
                else:
                    pass
                    # break
            except:
                traceback.print_exc()
                break
            sleep_time = randrange(60, 120)
            logging.info('休息{}秒'.format(sleep_time))
            sleep(sleep_time)

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
            'category_name': '有料段子',
            'url': d['video_url'],
            'cover_image': uploadImg.run('https://xcx.mengjukeji.com/Uploads/'+d['images']),
            'online_time': data['add_time'],

            'user_id': d['member_id'],
            'user_name': d['nickname'],
            'user_avatar': uploadImg.run('https://xcx.mengjukeji.com/Uploads/'+d['headimgurl']),

            'play_count': int(d['view_num'])*100,
            'bury_count': 0,
            'repin_count': 0,
            'share_count': int(d['forward_num']),
            'digg_count': int(d['like_num']),
            'comment_count': int(d['comment_num']),
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
