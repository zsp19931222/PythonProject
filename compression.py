# -*- coding: utf-8 -*-
import os

from PIL import Image, ImageFile

# 网络图片地址
img_local_path = 'F:/PycharmProjects/img/push.png'


# 下载到本地
def request_download(img_url):
    import requests
    r = requests.get(img_url)
    with open(img_local_path, 'wb') as f:
        f.write(r.content)
    compress_image(img_local_path)

    # 压缩图片文件


# 压缩本地图片
def compress_image(outfile, mb=30, quality=85, k=0.9):
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """

    o_size = os.path.getsize(outfile) // 1024
    print(o_size, mb)
    if o_size <= mb:
        return outfile

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    while o_size > mb:
        im = Image.open(outfile)
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
        try:
            out.save(outfile, quality=quality)
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024
    return outfile
