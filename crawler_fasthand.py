# coding=utf8
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from time import sleep, time
from random import randrange
import json
import traceback
from config import *
from utils import get_page_post, conbine_params
from db import DBStore
import uploadImg


_WORKER_THREAD_NUM = 1

'''
POST /rest/n/feed/hot?mod=OnePlus(ONEPLUS%20A5000)&lon=0&country_code=cn&did=ANDROID_683195cfdb2b2c4c&net=WIFI&app=0&oc=OPPO&ud=780974892&c=OPPO&sys=ANDROID_7.1.1&appver=5.4.7.5533&ftt=&language=zh-cn&iuid=&lat=0&ver=5.4&max_memory=256 HTTP/1.1
tag 美女
count   20
ussid   M183ODA5NzQ4OTJfMTUxNDE4OTI4ODQxMF_nvo7lpbM
client_key  3c2cd3f3
__NStokensig    15fe45abe09cb1dd4c2f2bb70e1fb56c3a683b43c1dbf237bf740a7a12890d68
token   9351d4b1bcc748b597dd7c3cdeed6feb-780974892
os  android
sig 08eb6c14f5b29a68de3ba93f87cb0e55
'''
API_FH = 'http://api.ksapisrv.com/rest/n/feed/tag?mod=OnePlus(ONEPLUS%20A5000)&lon=113.372312&country_code=cn&did=ANDROID_683195cfdb2b2c4c&net=WIFI&app=0&oc=OPPO&ud=780974892&c=OPPO&sys=ANDROID_7.1.1&appver=5.4.7.5533&ftt=&language=zh-cn&iuid=&lat=23.123042&ver=5.4&max_memory=256'

class NeihanSpider(object):

    def __init__(self):
        self._db = DBStore()

    def crawl_video(self):
        params = { }
        headers = {
            'User-Agent': 'kwai-android',
            'X-REQUESTID': '185307446',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'api.gifshow.com',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'tag': '美女',
            'count': '20',
            'ussid': 'M183ODA5NzQ4OTJfMTUxNDE4OTI4ODQxMF_nvo7lpbM',
            'client_key': '3c2cd3f3',
            '__NStokensig': '15fe45abe09cb1dd4c2f2bb70e1fb56c3a683b43c1dbf237bf740a7a12890d68',
            'token': '9351d4b1bcc748b597dd7c3cdeed6feb-780974892',
            'os': 'android',
            'sig': '08eb6c14f5b29a68de3ba93f87cb0e55',
            # 'pcursor': '4348581655'
        }
        while True:
            try:
                logging.info('Crawl video guanzhu...')
                ret = []
                request_url = API_FH
                resp = get_page_post(request_url, data=data, headers=headers)
                if resp:
                    contents = resp['feeds']
                    if len(contents) == 0:
                        break
                    for content in contents:
                        info = self._parse_item(content)
                        if info:
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
        logging.info('开始爬快手视频了了了了...')
        ps = NeihanSpider()
        ps.crawl_video()

if __name__ == '__main__':
    proxy_crawler = Crawler()
    proxy_crawler.run()
