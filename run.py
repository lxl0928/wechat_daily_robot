# coding: utf-8

import time

from timi_robot import SensoroLoggerClient

from settings import ACCEPT_PHONES, ROBOT_URL

sensoro_logger = SensoroLoggerClient(url=ROBOT_URL, phones=ACCEPT_PHONES)


class SensoroDailyNotice(object):

    def judge_time(self):
        while True:
            localtime = time.localtime(time.time() + 8 * 60 * 60)
            tm_wday = localtime.tm_wday + 1
            tm_hour = localtime.tm_hour
            print(tm_wday, tm_hour)
            if tm_wday in [1, 2, 3, 4, 5]:  # 周一 ~ 周五
                if tm_hour in (10, 19):  # 早10，晚19
                    self.send_notice(wday=tm_wday)

            time.sleep(60 * 29)

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


sensoro_notice = SensoroDailyNotice()
sensoro_notice.judge_time()
