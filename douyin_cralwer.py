# coding=utf8
import traceback
import json
import requests
from db import DBStore


def get_from_http():
    db = DBStore()
    total = 0
    api = 'http://video.neargh.com:9099/getMsgList'
    params = {'startId': 1}

    for i in xrange(2, 10000):
        params['startId'] = i
        print params
        try:
            resp = requests.post(api, data=json.dumps(params), timeout=30)
            print resp
            if resp and resp.status_code == 200:
                content = resp.json()
                if content['errcode'] != 200:
                    break
                for item in content['list']:
                    video_id = 'dy_' + item['video_id']
                    info = {
                        'video_id': video_id,
                        'group_id': video_id,
                        'item_id': video_id,
                        'content': item['content'],
                        'category_id': 12,
                        'category_name': '女神来了',
                        'url': item['url'],
                        'vurl': item['url'],
                        'cover_image': item['cover_image'],
                        'online_time': item['online_time'],
                        'user_id': item['user_id'],
                        'user_name': item['user_name'],
                        'user_avatar': item['user_avatar'],
                        'play_count': item['play_count'],
                        'share_count': item['share_count'],
                        'digg_count': item['digg_count'],
                        'comment_count': item['comment_count'],
                        'source': 'douyin'
                    }
                    print info
                    db.save([info])
                    total += 1
        except:
            traceback.print_exc()
    print 'total pages: {}, total records: {}'.format(params['startId'], total)
    print 'Script Done'


def main():
    get_from_http()


if __name__ == '__main__':
    main()
