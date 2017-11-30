# coding=utf8
import traceback
import json
import requests
from time import time, sleep
from db import DBStore
import config


db = DBStore()


def get_from_http(video_id):
    api = 'https://api.hyhuo.com/comment/list'
    params = {
        'nonce': '151203862505260',
        'token': 'c1b180879b8f79157d1038fab8c0a578',
        'vid': video_id,
        'timestamp': 1512038625,

        'version_code': '2017111500',
        'channel': 'c1025',
        'source': 'android',
        'uuid': '91bc59ba-a134-5994-f134-9294621b7cd1',
        'device_name': 'ONEPLUS A5000',
        'up_uid': '1445262',
        'device_code': '',
        'system_version': '7.1.1',
        'lan': 'zh',
        'page': 1,
    }
    comment_count = 0

    try:
        resp = requests.post(api, data=params, timeout=30, verify=False)
        print resp
        print 'saving comment...'
        if resp and resp.status_code == 200:
            content = resp.json()
            if content['status'] == 0:
                comment_count = len(content['data'])
                print 'get comment num: {}'.format(comment_count)
                comments = []
                for item in content['data']:
                    info = {
                        'group_id': 'hyhuo'+str(video_id),
                        'item_id': 'hyhuo'+str(video_id),
                        'user_id': item['uid'],
                        'user_name': item['username'],
                        'user_avatar': item['user_avatar'],
                        'create_time': item['create_time'],
                        'content': item['content'],
                        'digg_count': 0,
                        'comment_count': 0
                    }
                    comments.append(info)
                    if len(comments) > 5:
                        break
                db.save_comment(comments)
            else:
                print content
    except:
        traceback.print_exc()
    return comment_count


def main():
    get_from_http('7882')


if __name__ == '__main__':
    main()
