# coding: utf-8

import time
import logging

from timi_robot import SensoroLoggerClient

from settings import ACCEPT_PHONES, ROBOT_URL

sensoro_logger = SensoroLoggerClient(url=ROBOT_URL, phones=ACCEPT_PHONES)


class SensoroDailyNotice(object):

    def run(self):
        while True:
            localtime = time.localtime(time.time() + 8 * 60 * 60)
            tm_wday = localtime.tm_wday + 1
            tm_hour = localtime.tm_hour
            if tm_wday in [1, 2, 3, 4, 5]:  # 周一 ~ 周五
                if tm_hour in (10, 19):  # 早10，晚19
                    logging.info("当前时间{}, {}, {}".format(localtime, tm_wday, tm_hour))
                    self.send_notice(wday=tm_wday)

            time.sleep(60 * 29)  # 29分钟检测一次, 保证一小时发送2次，最多不超过3次

    @staticmethod
    def send_notice(wday):
        weekdays = {
            1: "一",
            2: "二",
            3: "三",
            4: "四",
            5: "五"
        }
        sensoro_logger.log(err="今天是周{}, 大家记得提交日报喔!".format(weekdays[wday]))
        if wday == 5:  # 周五还需要提醒大家修改周报
            sensoro_logger.log(
                err="今天是周{}, 周报也需要更新喔!"
                    "周报链接: https://shimo.im/sheets/CTrdYQ8HRDtD3tVJ/CdyCZ".format(weekdays[wday]))


sensoro_notice = SensoroDailyNotice()
sensoro_notice.run()
