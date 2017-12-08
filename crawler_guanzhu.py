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
            "max_time": str(int(time()))+'673',

            "ac": "wifi",
            "mpic": "1",
            "app_name": "joke_essay",
            "_rticket": "1512641620155",
            "essence": "1",
            "video_cdn_first": "1",
            "webp": "1",
            "device_type": "ONEPLUS A5000",
            "os_api": "25",
            "double_col_mode": "0",
            "version_code": "665",
            "os_version": "7.1.1",
            "update_version_code": "6654",
            "local_request_tag": "1512641620153",
            "channel": "oppo-cpa",
            "device_platform": "android",
            "count": "30",
            "screen_width": "1080",
            "ssmix": "a",
            "iid": "18826291544",
            "device_brand": "OnePlus",
            "manifest_version_code": "665",
            "version_name": "6.6.5",
            "openudid": "683195cfdb2b2c4c",
            "device_id": "39503669487",
            "message_cursor": "-1",
            "language": "zh",
            "level": "8",
            "uuid": "99000979108573",
            "aid": "7",
            "category_id": "3",
            "resolution": "1080*1920",
            "enable_image_comment": "1",
            "dpi": "480",
        }
        headers = {
            'User-Agent': 'okhttp/3.7.0.6',
            'Host': 'is.snssdk.com',
            'Cookie': 'uuid=864630039828537; _ga=GA1.3.1845980332.1506334759; _ga=GA1.2.1845980332.1506334759; login_flag=b392a592d42cbfb8a3b6347830c1ed72; sessionid=4c835d618879f0d53d37c405142abba5; uid_tt=85b70389b3e76192964a4b776e42c812; sid_tt=4c835d618879f0d53d37c405142abba5; sid_guard="4c835d618879f0d53d37c405142abba5|1512203333|15552000|Thu\054 31-May-2018 08:28:53 GMT"; install_id=18826291544; ttreq=1$1564cd48e6bae9f21b1730b187fb782087c513d8; alert_coverage=84; qh[360]=1'
        }
        while True:
            try:
                logging.info('Crawl video guanzhu...')
                print params['max_time']
                ret = []
                request_url = '{}?{}'.format(API_GZ, conbine_params(params))
                resp = get_page(request_url, headers=headers)
                if resp:
                    contents = resp['data']['data']
                    if len(contents) == 0:
                        break
                    for content in contents:
                        info = self._parse_item(content)
                        # print info
                        ret.append(info)
                    self._db.save(ret)
                    if int(params['max_time']) <= resp['data']['min_time']:
                        params['max_time'] = str(int(params['max_time'] - 3600000))
                    else:
                        params['max_time'] = str(resp['data']['min_time'])
                    logging.info('休息30秒')
                    sleep(30)
                else:
                    break
            except:
                traceback.print_exc()
                break

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
            'category_id': '1113',
            'category_name': '关注类视频',
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
            'top_comments': 0,
            'comment_crawled': 0
        }
        info['vurl'] = 'http://i.snssdk.com/neihan/video/playback/timestamp/?video_id={}&quality=480p&line=0&is_gif=0.mp4'.format(d['video_id'])
        return info


class Crawler(object):

    def run(self):
        logging.info('开始爬内涵了了了了...')
        ps = NeihanSpider()
        ps.crawl_video()

if __name__ == '__main__':
    proxy_crawler = Crawler()
    proxy_crawler.run()
