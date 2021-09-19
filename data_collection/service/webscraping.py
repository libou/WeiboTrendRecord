"""
WebScraping
"""
from requests import get
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import json
import traceback

import re


def scraping(proxy, data_dir, kafkaObj, local=False):
    """
    Crawl data from the website
    :param proxy: proxy ip
    :param data_dir: directory of local records (used when failed to write Kafka)
    :param kafkaObj: Kafka Object
    :param local: Whether save failed records locally
    :return: status code of writing Kafka, error message
    """
    log = logging.getLogger("webscraping_log")

    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    proxies = {"http": proxy}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    if proxy is None:
        res = get(url, headers=headers, timeout=2)
    else:
        res = get(url, headers=headers, proxies=proxies, timeout=2)


    if res.status_code != 200:
        code = res.status_code
        res.close()
        failMsg = "数据爬取异常"
        log.error("数据爬取异常 Webscraping ERROR! code: {}".format(code))
        return code, failMsg

    result = []
    content = res.content.decode('utf-8')
    html_container = BeautifulSoup(content, "html.parser")
    container = html_container.tbody
    tr_list = container.find_all('tr')

    for tr in tr_list:
        td_set = tr.find_all("td")
        rank = td_set[0].text
        title = td_set[1].a.text

        countStr = td_set[1].span
        category = None
        count = 0
        if td_set[1].span is None:
            count = 0
        else:
            countStr = td_set[1].span.text
            if  countStr.strip().isdigit():
                count = countStr.strip()
            else:
                countList = re.findall(r'\d+', countStr.strip())
                if len(countList) is not 0:
                    count = countList[0].strip()
                categoryList = re.findall(r'\D+', countStr.strip())
                if len(categoryList) is not 0:
                    category = categoryList[0].strip()
        result.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rank, title, count, category])
    result.pop(0)
    res.close()

    df = pd.DataFrame(result, columns=['time', 'rank', 'title', 'count', 'category'])
    # TODO: 直接判断rank是否为数字
    df = df[df['rank'] != '•']
    df['rank'] = df['rank'].astype("int")
    df['count'] = df['count'].astype("long")
    # write kafka
    msg = df.to_json(orient='records')
    return sendMsg(data_dir, kafkaObj, msg, df)


def sendMsg(data_dir, kafkaObj, msgList, df, local=False):
    """
    Send records to Kafka topic
    :param data_dir: directory of local records (used when failed to write Kafka)
    :param kafkaObj: Kafka Object
    :param msg: records in json format
    :param df: dataframe of records
    :param local: Whether save failed records locally
    :return: status code of writing Kafka, error message
    """
    log = logging.getLogger("webscraping_log")

    jsonList = json.loads(msgList)
    finalCode = 200
    failedMsg = None
    # 逐行发送
    print(jsonList)
    for jsonElement in jsonList:
        msg = json.dumps(jsonElement)
        code = kafkaObj.send(msg)
        if code != 200:
            finalCode = code
            # kafka写入失败：写入本地备份
            if local:
                break
            year = str(datetime.now().year)
            month = str(datetime.now().month)
            filename = "_".join([year, month])
            try:
                if not os.path.exists(os.path.join(data_dir, filename)):
                    os.mkdir(os.path.join(data_dir, filename))
                if not os.path.exists(os.path.join(data_dir, filename, "record.csv")):
                    df.to_csv(os.path.join(data_dir, filename, "record.csv"), mode='w', index=None, header=True)
                else:
                    df.to_csv(os.path.join(data_dir, filename, "record.csv"), mode='a', index=None, header=None)
            except Exception as e:
                failedMsg = "kafka写入失败，同时保存本地文件异常"
                log.error("kafka写入失败，同时保存本地文件异常：{}".format(traceback.format_exc()))
            else:
                failedMsg = "kafka写入失败, 已成功保存本地文件"
                log.warning("kafka写入失败, 已成功保存本地文件")
    if finalCode == 200:
        log.info("单次数据记录写入kafka成功")
    return finalCode, failedMsg
