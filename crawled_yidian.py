# coding=utf8
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from time import sleep, time, mktime, strptime
from random import randrange
import json
import traceback
from config import *
from utils import get_page_post, conbine_params
from db import DBStore

_WORKER_THREAD_NUM = 1

API_YD = 'https://a1.go2yd.com/Website/channel/news-list-for-keyword?searchentry=search_sug_keyword&reqid=ahu8lp4t_{}_{}&group_id=101240634685&distribution=www.oppo.com&searchid=634626061_1514359292867_3630&refresh=1&appid=yidian&cstart={}&word_type=token&platform=1&ctype=video&cv=4.5.5.1&display=%E6%80%A7%E6%84%9F%E7%BE%8E%E5%A5%B3&cend={}&fields=docid&fields=date&fields=image&fields=image_urls&fields=like&fields=source&fields=title&fields=url&fields=comment_count&fields=up&fields=down&ctype_type=card_type&version=020200&ad_version=010943&group_fromid=g181&net=wifi'

class NeihanSpider(object):

    def __init__(self):
        self._db = DBStore()

    def crawl_video(self):
        params = { }
        headers = {
            'cookie': 'JSESSIONID=_vmRHWQbSFFvZXSNbyrv5g',
            'accept-encoding': 'gzip, deflate',
            'content-encoding': 'gzip',
            'x-tingyun-lib-type-n-st': '3;{}'.format(int(time()*1000)),
            'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.1; ONEPLUS A5000 Build/NMF26X)'
        }
        cnum = 6
        cstart, cend = 16, 25 
        while True:
            try:
                logging.info('Crawl video yidian...')
                ret = []
                request_url = API_YD.format(int(time()*1000), randrange(4261, 4266), cstart, cend)
                print request_url
                cstart += cnum
                cend += cnum
                resp = get_page_post(request_url, data={}, headers=headers)
                if resp:
                    contents = resp['result']
                    if len(contents) == 0:
                        pass
                        # break
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
            sleep_time = randrange(10, 60)
            logging.info('休息{}秒'.format(sleep_time))
            sleep(sleep_time)

    def _parse_item(self, data):
        info = self._video_item(data)
        return info


    def _video_item(self, data):
        info = {}
        d = data
        video_id = 'yidian_{}'.format(d.get('sdk_video_id', int(time()*10000)))
        info = {
            'group_id': video_id,
            'item_id': video_id,
            'video_id': video_id,
            'content': d['title'],
            'category_id': '1116',
            'category_name': '一点视频',
            'sub_category_name': ','.join(d['keywords']) if d.get('keywords', '') else '',
            'url': d['video_urls'][0]['url'],
            'cover_image': d['image'],
            'online_time': mktime(strptime(d['date'], '%Y-%m-%d %H:%M:%S')),

            'user_id': 0,
            'user_name': d['wemedia_info']['name'],
            'user_avatar': d['wemedia_info']['image'],

            'play_count': randrange(10000, 100000),
            'bury_count': randrange(100, 1000),
            'repin_count': randrange(100, 1000),
            'share_count': randrange(100, 10000),
            'digg_count': randrange(100, 10000),
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
