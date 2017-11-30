# coding=utf8
import traceback
import json
import requests
from db import DBStore


def get_from_http():
    db = DBStore()
    total = 0
    api = 'http://video.neargh.com:9099/getMsgList'
    params = {'startId': 0}

    while True:
        print params
        try:
            resp = requests.post(api, data=json.dumps(params), timeout=30)
            print resp
            print 'saving video...'
            if resp and resp.status_code == 200:
                content = resp.json()
                if len(content['list']) == 0:
                    break
                print 'get videos num: {}'.format(len(content['list']))
                videos = []
                for item in content['list']:
                    video_id = 'dy_' + item['video_id']
                    print item['id'], video_id
                    info = {
                        'video_id': video_id,
                        'group_id': video_id,
                        'item_id': video_id,
                        'content': item['content'],
                        'category_id': 1111,
                        'category_name': '抖音视频',
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
                        'bury_count': 0,
                        'repin_count': 0,
                        'comment_count': item['comment_count'],
                        'source': 'douyin'
                    }
                    videos.append(info)
                    total += 1
                db.save(videos)
        except:
            traceback.print_exc()
        params['startId'] += 200
    print 'total pages: {}, total records: {}'.format(params['startId'], total)
    print 'Script Done'


def main():
    get_from_http()


if __name__ == '__main__':
    main()
