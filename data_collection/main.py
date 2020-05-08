"""
This program is used for crawling daily hot topics on Weibo
"""
import os
import logging
from notification import Notification
from webscraping import scraping
from datetime import datetime
from time import sleep
import configparser
from proxy.proxy_pool import Proxy


def main():
    # sched_time = [9, 16, 22]
    # i = 0
    # current_hour = datetime.now().hour
    # for e in sched_time:
    #     if current_hour > e:
    #         i = (i + 1) % 3

    global inst_proxy
    try:
        while True:
            now = datetime.now()
            if 2 <= now.hour <= 5:
                sleep(1)
            elif now.minute == 30 or now.minute == 0:
                proxy = inst_proxy.get_proxy()
                proxy_count = inst_proxy.get_proxies_num()
                while proxy_count > 5:
                    code = scraping(proxy, data_dir)
                    if code == 200:
                        logging.info("Crawled one record successfully.")
                        break
                    else:
                        inst_proxy.delete_proxy(proxy)
                        proxy_count = inst_proxy.get_proxies_num()
                        proxy = inst_proxy.get_proxy()
                if proxy_count <= 5:
                    scraping(None, data_dir)
                    logging.warning("The number of available proxy ip is {}".format(proxy_count))
                    mailObj.notification("The number of available proxy ip is {}".format(proxy_count))
                    inst_proxy = Proxy("proxy/proxy.txt")
                sleep(61)
            else:
                sleep(1)
    except Exception as e:
        logging.error(e)
        mailObj.notification("Error! Please check the log")


if __name__ == '__main__':
    config_file = "../config.ini"

    conf = configparser.ConfigParser()
    conf.read(config_file)

    sender = conf.get("notification", "sender")
    pw = conf.get("notification", "passwd")
    receiver = conf.get("notification", "receiver")

    log_dir = conf.get("web_scraping", "log_dir")
    data_dir = conf.get("web_scraping", "data_dir")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(level=logging.WARNING,
                        filename=os.path.join(log_dir, 'monitor.log'),
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        )
    logging.info("WeiboTrendRecord launching")
    inst_proxy = Proxy("proxy/proxy.txt")
    mailObj = Notification(sender, pw, receiver)
    main()
