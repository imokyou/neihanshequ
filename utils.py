# coding=utf8
import traceback
import requests
from time import sleep
import urllib
from config import *


def get_page(url, headers={}, count=0):
    try:
        if count > RETRY_TIMES:
            logging.info('Max retries exceeded with url, retry: %s times' % count)
            return None
        # print url
        resp = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
        print resp
        if not resp or resp.status_code != 200:
            count = count + 1
            sleep(CRAWL_PAGE_SLEEP)
            get_page(url, headers=headers, count=count)
        return resp.json()
    except:
        traceback.print_exc()
        count = count + 1
        sleep(CRAWL_PAGE_SLEEP)
        get_page(url, headers=headers, count=count)
    return None


def conbine_params(params):
    query_strs = []
    for k, v in params.iteritems():
        query_strs.append('{}={}'.format(k, urllib.quote(v)))
    return '&'.join(query_strs)
