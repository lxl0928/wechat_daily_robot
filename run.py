# coding: utf-8

import json
import time
import base64
import logging
import hashlib

from dateutil import tz
from datetime import datetime
from pprint import pprint

import requests

from settings import ROBOT_URL

headers = {"Content-Type": "application/json"}

news_template = {
    "msgtype": "news",
    "news": {
       "articles": [
           {
               "title": "{title}",
               "description": "{description}",
               "url": "{url}",
               "picurl": "{pic_url}"
           }
        ]
    }
}

text_template = {
    "msgtype": "text",
    "text": {
        "content": "{content}",
        "mentioned_list": ["@all"],
        "mentioned_mobile_list": ["@all"]
    }
}

image_template = {
    "msgtype": "image",
    "image": {
        "base64": "{b64_data}",
        "md5": "{md5}"
    }
}


def convert(image_url):
    try:
        response = requests.get(url=image_url)
        print(type(response.content))
        image_base64 = base64.b64encode(response.content)
        md5 = hashlib.md5(response.content).hexdigest()
        return image_base64.decode(), md5
    except Exception as e:
        logging.error(msg="转换出错!")
    return None


def send_text_msg(content):
    text_template['text'].update(
        {
            "content": f"{content}",
            "mentioned_list": ["@all"],
            "mentioned_mobile_list": ["@all"]
        }
    )
    pprint(text_template)
    requests.post(url=ROBOT_URL, headers=headers, data=json.dumps(text_template))


def send_news_msg(title, description, url, pic_url):
    news_template['news']['articles'][0].update(
        {
            "title": f"{title}",
            "description": f"{description}",
            "url": f"{url}",
            "picurl": f"{pic_url}"
        }
    )
    pprint(news_template)
    requests.post(url=ROBOT_URL, headers=headers, data=json.dumps(news_template))


def send_image_msg(image_url):
    b64, md5 = convert(image_url=image_url)
    image_template['image'].update(
        {
            "base64": f"{b64}",
            "md5": f"{md5}"
        }
    )
    requests.post(url=ROBOT_URL, headers=headers, data=json.dumps(image_template))


class SensoroDailyNotice(object):

    def judge_time(self):
        while True:
            tz_sh = tz.gettz('Asia/Shanghai')
            cnt_datetime = datetime.fromtimestamp(time.time(), tz=tz_sh)
            tm_wday = cnt_datetime.isoweekday()
            tm_hour = cnt_datetime.hour
            tm_min = cnt_datetime.minute

            print(f"周{tm_wday}, 小时: {tm_hour}, 分钟: {tm_min}")
            logging.info(msg="{},{}".format(tm_wday, tm_hour, tm_min))
            if tm_wday in [1, 2, 3, 4, 5]:
                if tm_hour == 11 and 29 <= tm_min <= 59:
                    self.send_notice(wday=tm_wday, on_work=True)

                if tm_hour == 19 and 10 <= tm_min <= 30:
                    self.send_notice(wday=tm_wday, on_work=False)

            time.sleep(60 * 30)  # 半小时检查一次

    @staticmethod
    def send_notice(wday, on_work=False):
        weekdays = {
            1: "星期一",
            2: "星期二",
            3: "星期三",
            4: "星期四",
            5: "星期五"
        }

        if not on_work:
            url = "https://shimo.im/sheets/5rk9d8YDEwspDbqx/E58FM"
            if wday != 5:
                send_text_msg(content="下班啦..., 别忘记打下班卡喔!".format(url))
            elif wday == 5:
                send_text_msg(content="下班啦..., 别忘记打下班卡喔! 周末愉快！".format(url))

        else:
            tianqi_url = "https://tianqiapi.com/api?version=v6&appid=49564374&appsecret=4rNE9xdd&cityid=101010300"
            response = requests.get(url=tianqi_url)
            content = json.loads(response.content)
            wea = content.get('wea', '')
            tem_high = content.get('tem1', '')
            tem_low = content.get('tem2', '')
            air_tips = content.get('air_tips', '')
            ct_date = datetime.now().date()
            title = f"{ct_date.year}年{ct_date.month}月{ct_date.day}日  {weekdays[wday]} "
            description = "早上好!\n今日朝阳区天气: {} 最高温度: {}℃ 最低温度: {}℃\n{}".format(
                wea, tem_high, tem_low, air_tips)

            url = "https://shimo.im/sheets/V5qeWO77wKUbF8AJ"

            meiri_yiju_url = "https://open.iciba.com/dsapi/"
            response = requests.get(url=meiri_yiju_url)
            content = json.loads(response.content)
            fenxiang_img = content.get('fenxiang_img')
            pic_url = content.get('picture2')

            # 发送添加news
            send_news_msg(title=title, description=description, url=url, pic_url=pic_url)
            # 发送每日一句image
            send_image_msg(image_url=fenxiang_img)
            # 发送上班打卡tips
            send_text_msg(content="上班啦..., 别忘记打上班卡喔!".format(url))


sensoro_notice = SensoroDailyNotice()
sensoro_notice.judge_time()
