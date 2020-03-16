"""
This program is used for crawling daily hot topics on Weibo
"""
import os
import logging
import sys
from notification import Notification
from webscraping import scraping
from datetime import datetime
from time import sleep


def main():
    sched_time = [9, 16, 22]
    i = 0
    current_hour = datetime.now().hour
    for e in sched_time:
        if current_hour > e:
            i = (i + 1) % 3

    try:
        while True:
            now = datetime.now()
            if now.hour == sched_time[i] and now.min == 0:
                scraping()
                i = (i+1) % len(sched_time)
                sleep(61 * 60)
            else:
                # if sched_time[i] - now.hour > 1:
                #     sleep((now.hour - sched_time[i] - 1) * 60 * 60)
                # else:
                sleep(1)
    except Exception as e:
        logging.error(e)
        mailObj.notification(e)


if __name__ == '__main__':
    sender = sys.argv[1]
    pw = sys.argv[2]
    receiver = sys.argv[3]

    if not os.path.exists("log"):
        os.mkdir("log")

    logging.basicConfig(level=logging.WARNING,
                        filename='log/monitor.log',
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        )
    logging.info("WeiboTrendRecord launching")
    mailObj = Notification(sender, pw, receiver)
    main()
