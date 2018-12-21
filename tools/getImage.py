#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: wang
# Date: 18/12/20 13:53

import requests
from urllib.parse import urlencode


# 请求页面
def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return None


# 获取图片信息
def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('media_name')
            images = item.get('image_list'),
            for image in images:
                yield {
                    'image': 'http:' + image[0]['url'],
                    'title': title
                }


import os
from hashlib import md5


# 保存图片
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                     'images/{0}'.format(item.get('title'))))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                     'images/{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(),
                                                                 'jpg'))
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('already download', file_path)
    except requests.ConnectionError:
        print('failed')


from multiprocessing.pool import Pool


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    pool = Pool()
    group = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    # 多进程下载
    pool.map(main, group)
    pool.close()
    pool.join()
