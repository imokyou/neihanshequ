# coding=utf8
import traceback
import json
import requests
from time import time, sleep
from db import DBStore
import config


def get_from_http():
    db = DBStore()
    total = 0
    api = 'https://search.hyhuo.com/so/tag'
    params = {'sort': 'new', 'page': 1, 'keyword': '红人'}

    while True:
        try:
            resp = requests.post(api, data=params, timeout=30, verify=False)
            print resp
            print 'saving video...'
            if resp and resp.status_code == 200:
                content = resp.json()
                if len(content['data']['data_list']) == 0:
                    break
                print 'get videos num: {}'.format(len(content['data']['data_list']))
                videos = []
                for item in content['data']['data_list']:
                    video_id = 'hyhuo_' + item['vid']
                    print video_id, item['title']
                    info = {
                        'video_id': video_id,
                        'group_id': video_id,
                        'item_id': video_id,
                        'content': item['title'],
                        'category_id': 1112,
                        'category_name': '美女视频',
                        'url': item['video_preview_url'].replace('sd.m3u8', 'fhd.mp4'),
                        'vurl': item['video_preview_url'].replace('sd.m3u8', 'fhd.mp4'),
                        'cover_image': item['thumb_img'],
                        'online_time': int(time()),
                        'user_id': item['uid'],
                        'user_name': item['username'],
                        'user_avatar': item['user_avatar'],
                        'play_count': 0,
                        'share_count': 0,
                        'digg_count': 0,
                        'bury_count': 0,
                        'repin_count': 0,
                        'comment_count': 0,
                        'source': 'hyhuo'
                    }
                    if u'万' in item['play_num']:
                        info['play_count'] = int(item['play_num'].replace('万'))*10000
                    else:
                        info['play_count'] = int(item['play_num'])

                    if u'万' in item['download_num']:
                        info['share_count'] = int(item['download_num'].replace('万'))*10000
                    else:
                        info['share_count'] = int(item['download_num'])
                    videos.append(info)
                    total += 1
                db.save(videos)
        except:
            traceback.print_exc()
        params['page'] += 1
        sleep(config.HYHUO_CRAWL_PAGE_SLEEP)
    print 'total pages: {}, total records: {}'.format(params['page'], total)
    print 'Script Done'


def main():
    get_from_http()


if __name__ == '__main__':
    main()
