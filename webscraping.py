"""
WebScraping
"""
from requests import get
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os


def scraping():
    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    res = get(url, headers=headers)

    if res.status_code != 200:
        logging.error(res.status_code + ": Open url Error")
        raise Exception(res.status_code + ": Open url Error")

    result = []
    content = res.content.decode('utf-8')
    html_container = BeautifulSoup(content, "html.parser")
    container = html_container.tbody
    tr_list = container.find_all('tr')

    for tr in tr_list:
        td_set = tr.find_all("td")
        rank = td_set[0].text
        title = td_set[1].a.text
        if td_set[1].span is None:
            count = 0
        else:
            count = td_set[1].span.text
        result.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rank, title, count])
    result.pop(0)

    if not os.path.exists("data"):
        os.mkdir("data")
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    filename = "_".join([year, month])
    if not os.path.exists(os.path.join("data", filename)):
        os.mkdir(os.path.join("data", filename))

    df = pd.DataFrame(result, columns=['time', 'rank', 'title', 'count'])
    if not os.path.exists(os.path.join("data", filename, "record.csv")):
        df.to_csv(os.path.join("data", filename, "record.csv"), mode='w', index=None, header=True)
    else:
        df.to_csv(os.path.join("data", filename, "record.csv"), mode='a', index=None, header=None)