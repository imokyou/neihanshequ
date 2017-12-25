# coding=utf8
import os
import requests
import hashlib
import oss2
from config import *

 
auth = oss2.Auth(OSS2['AccessKeyId'], OSS2['AccessKeySecret'])
bucket = oss2.Bucket(auth, OSS2['Endpoint'], OSS2['Bucket'])


def run(url):
    extension  = os.path.splitext(url)[-1]
    image = requests.get(url, timeout=30)

    hash_md5 = hashlib.md5(image.content)
    filename = hash_md5.hexdigest()+extension
    result = bucket.put_object(filename, image.content)

    image_url = ''
    if result.status == 200:
        image_url = 'http://{}.{}/{}'.format(OSS2['Bucket'], OSS2['Endpoint'], filename)
    return image_url
    


if __name__ == '__main__':
    img_url = 'https://xcx.mengjukeji.com/Uploads/VideoVideo/2017-12-17/5a36503281b00.jpg'
    print run(img_url)