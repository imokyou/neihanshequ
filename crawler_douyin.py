# coding=utf8
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from time import sleep, time
from random import randrange
import json
import traceback
from config import *
from utils import *
from db import DBStore
import uploadImg


_WORKER_THREAD_NUM = 1

'''

'''
API_DY_CURSOR = 'https://aweme.snssdk.com/aweme/v1/story/?cursor=0&count=20&retry_type=no_retry&iid=20779054872&device_id=40113379514&ac=wifi&channel=oppo&aid=1128&app_name=aweme&version_code=166&version_name=1.6.6&device_platform=android&ssmix=a&device_type=ONEPLUS+A5000&device_brand=OnePlus&language=zh&os_api=25&os_version=7.1.1&uuid=99000979108573&openudid=683195cfdb2b2c4c&manifest_version_code=166&resolution=1080*1920&dpi=480&update_version_code=1662&_rticket={}&ts={}&as=a1850ba46c7c7adac1&cp=b8c7aa5ec51244a6e1'

API_DY = 'https://aweme.snssdk.com/aweme/v1/feed/?type=0&min_cursor={}&count=6&volume=0.06666666666666667&retry_type=no_retry&iid=20779054872&device_id=40113379514&ac=wifi&channel=oppo&aid=1128&app_name=aweme&version_code=166&version_name=1.6.6&device_platform=android&ssmix=a&device_type=ONEPLUS+A5000&device_brand=OnePlus&language=zh&os_api=25&os_version=7.1.1&uuid=99000979108573&openudid=683195cfdb2b2c4c&manifest_version_code=166&resolution=1080*1920&dpi=480&update_version_code=1662&_rticket={}&ts={}&as=a1055b74549a0a68e1&cp=bda6aa574915488ce1'

class NeihanSpider(object):

    def __init__(self):
        self._db = DBStore()

    def crawl_video(self):
        params = { }
        headers = {
            'Accept-Encoding': 'gzip',
            'Cache-Control': 'max-stale=10',
            'Host': 'aweme.snssdk.com',
            'Connection': 'Keep-Alive',
            'Cookie': 'login_flag=3caab73ecc4f08f6760d889163bc781d; sessionid=be4c03153c97da7c62a98bad29b184b8; uid_tt=228a590198845c3f646c011de0f1423e; sid_tt=be4c03153c97da7c62a98bad29b184b8; sid_guard="be4c03153c97da7c62a98bad29b184b8|1514256333|2592000|Thu\054 25-Jan-2018 02:45:33 GMT"; install_id=20779054872; ttreq=1$61b4fa10976cf688d66ece268f8392e880b5c74f; qh[360]=1',
            'User-Agent': 'okhttp/3.8.1',
        }

        while True:
            try:
                logging.info('Crawl video guanzhu...')
                ret = []
                s = requests.Session()

                ts, rts = int(time()), int(time()*1000)
                resp_cursor = s.get(API_DY_CURSOR.format(rts, ts), headers=headers, timeout=30)
                print resp_cursor
                print resp_cursor.json()

                resp = s.get(API_DY.format(rts, rts, ts), headers=headers, timeout=30)
                print resp
                print resp.json()

                if resp:
                    contents = resp['aweme_list']
                    if len(contents) == 0:
                        break
                    for content in contents:
                        print content
                    #     info = self._parse_item(content)
                    #     if info:
                    #         print info
                    #         ret.append(info)
                    # self._db.save(ret)
                    
                else:
                    break
            except:
                traceback.print_exc()
                break
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
        video_url = d.get('main_mv_urls', '')
        if not video_url:
            return info
        video_id = 'fasthand_{}'.format(d['photo_id'])
        info = {
            'group_id': video_id,
            'item_id': video_id,
            'video_id': video_id,
            'content': d['caption'],
            'category_id': '1115',
            'category_name': '快手视频',
            'url': d['main_mv_urls'][0]['url'],
            'cover_image': d['cover_thumbnail_urls'][0]['url'],
            'online_time': int(int(d['timestamp'])/1000),

            'user_id': d['user_id'],
            'user_name': d['user_name'],
            'user_avatar': d['headurls'][0]['url'],

            'play_count': int(d['view_count']),
            'bury_count': int(d['unlike_count']),
            'repin_count': 0,
            'share_count': int(d['forward_count']),
            'digg_count': int(d['like_count']),
            'comment_count': 0,
            'has_comments': 0,
            'comments': json.dumps([]),
            'top_comments': 0,
            'comment_crawled': 0
        }
        info['vurl'] = info['url']
        return info


class Crawler(object):

    def run(self):
        logging.info('开始爬抖音视频了了了了...')
        ps = NeihanSpider()
        ps.crawl_video()

if __name__ == '__main__':
    proxy_crawler = Crawler()
    proxy_crawler.run()
