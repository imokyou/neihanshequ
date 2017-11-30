# coding=utf8
import traceback
import json
import requests


def get_from_http():
    total = 0
    api = 'http://video.neargh.com:9099/getMsgList'
    params = {'startId': 0}

    category_ids = []

    while True:
        print params
        try:
            resp = requests.post(api, data=json.dumps(params), timeout=30)
            print resp
            if resp and resp.status_code == 200:
                content = resp.json()
                if len(content['list']) == 0:
                    break
                print params
                print 'get videos num: {}'.format(len(content['list']))
                for item in content['list']:
                    if item['category_id'] not in category_ids:
                        category_ids.append(item['category_id'])
                    total += 1
        except:
            traceback.print_exc()
        params['startId'] += 200
    print 'total pages: {}, total records: {}'.format(params['startId'], total)
    print 'Script Done'

    for c in category_ids:
        print "https://p3.pstatp.com/obj/{}".format(c)


def main():
    get_from_http()


if __name__ == '__main__':
    main()
