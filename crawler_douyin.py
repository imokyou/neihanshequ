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
API_DY = 'https://aweme.snssdk.com/aweme/v1/feed/?type=0&min_cursor=1514256426246&count=6&volume=0.06666666666666667&retry_type=no_retry&iid=20779054872&device_id=40113379514&ac=wifi&channel=oppo&aid=1128&app_name=aweme&version_code=166&version_name=1.6.6&device_platform=android&ssmix=a&device_type=ONEPLUS+A5000&device_brand=OnePlus&language=zh&os_api=25&os_version=7.1.1&uuid=99000979108573&openudid=683195cfdb2b2c4c&manifest_version_code=166&resolution=1080*1920&dpi=480&update_version_code=1662&_rticket=1514256548961&ts=1514256548&as=a1055b74549a0a68e1&cp=bda6aa574915488ce1'

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
                request_url = API_DY
                resp = get_page(request_url, headers=headers)
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
