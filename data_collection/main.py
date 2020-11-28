"""
This program is used for crawling daily hot topics on Weibo
"""
import os
import logging
from tools.notification import Notification
from service.webscraping import scraping
from datetime import datetime
from time import sleep
import configparser
from proxy.proxy_pool import Proxy
from tools.kafka_configuration import KafkaObj


def main():
    global inst_proxy
    try:
        while True:
            now = datetime.now()
            if 2 <= now.hour <= 5:
                sleep(1)
            elif now.minute % 30 == 0:
                proxy = inst_proxy.get_proxy()
                proxy_count = inst_proxy.get_proxies_num()
                times = 3
                while proxy_count > 5 and times >= 0:
                    code = scraping(proxy, data_dir, kafka_obj)
                    if code == 200:
                        # logging.info("Crawled one record successfully.")
                        break
                    elif code == 9092:
                        # kafka写入异常
                        if mailObj is not None:
                            mailObj.notification("Write Kafka ERROR! code: {}".format(code))
                        break
                    else:
                        times = times - 1
                        # inst_proxy.delete_proxy(proxy)
                        # proxy_count = inst_proxy.get_proxies_num()
                        # logging.warning(
                        #     "Proxy ip:{} error! Use another proxy ip. Current # of proxy is {}".format(proxy,
                        #                                                                                proxy_count))
                        logging.warning(
                            "Proxy ip:{} error! Use another proxy ip.".format(proxy))
                        logging.warning("Retry: {} times".format(times))
                        proxy = inst_proxy.get_proxy()
                if proxy_count <= 5 or times < 0:
                    # logging.warning("The number of available proxy ip is {}".format(proxy_count))
                    # if mailObj is not None:
                    #     mailObj.notification("The number of available proxy ip is {}".format(proxy_count))
                    # inst_proxy = Proxy("proxy/proxy.txt")
                    logging.warning("Retry: over 3 times. Scraping without proxy!")

                    code = scraping(None, data_dir, kafka_obj)

                    if code == 9092:
                        if mailObj is not None:
                            mailObj.notification("Write Kafka ERROR! code: {}".format(code))
                        sleep(61)
                        continue

                    if code != 200:
                        logging.error("Webscraping ERROR! code: {}".format(code))
                        if mailObj is not None:
                            mailObj.notification("Webscraping ERROR! code: {}".format(code))
                        sleep(61)
                        continue
                sleep(61)
            else:
                sleep(1)
    except Exception as e:
        logging.error(e)
        if mailObj is not None:
            mailObj.notification("Error! Please check the log")


if __name__ == '__main__':
    config_file = "../config.ini"
    if not os.path.exists("../config.ini"):
        config_file = "../config-template.ini"

    conf = configparser.ConfigParser()
    conf.read(config_file)

    # 邮件通知配置
    sender = conf.get("notification", "sender")
    pw = conf.get("notification", "passwd")
    receiver = conf.get("notification", "receiver")

    # 日志配置
    log_dir = conf.get("web_scraping", "log_dir")

    # 文件存储地址配置
    data_dir = conf.get("web_scraping", "data_dir")

    # kafka配置
    kafka_server = conf.get("kafka", "server")
    kafka_topic = conf.get("kafka", "topic")
    kafka_obj = KafkaObj(kafka_server, kafka_topic)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(level=logging.INFO,
                        filename=os.path.join(log_dir, 'web_scraping.log'),
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        )
    logging.info("WeiboTrendRecord launching")

    inst_proxy = Proxy("proxy/proxy.txt")
    mailObj = Notification(sender, pw, receiver)
    if "../config-template.ini" is config_file :
        mailObj = None
    main()
