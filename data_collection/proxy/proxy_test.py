import requests
from proxy.proxy_pool import Proxy
from tqdm import tqdm


def test_proxy(proxy, https_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    try:
        proxies = {"http": proxy}
        res = requests.post(https_url, headers=headers, proxies=proxies, timeout=1)
        content = res.content.decode("utf-8")

        # print(content)
        if res.status_code == 200:
            return True
        return False
    except Exception as e:
        msg = str(e)
        print(msg)
        return False


def delete_proxy(proxy_list):
    with open("/Users/libou/Code/Projects/WeiboTrendRecord/data_collection/proxy/proxy.txt", "w+") as file:
        proxies = file.read().split("\n")[:-1]
        for item in proxy_list:
            proxies.remove(item)
        file.writelines("%s\n" % proxy for proxy in proxies)


def doTest():
    inst = Proxy('/Users/libou/Code/Projects/WeiboTrendRecord/data_collection/proxy/proxy.txt')
    count = 0
    remove_list = []
    for i in tqdm(range(inst.get_proxies_num())):
        proxy = inst.get_proxy()
        # url = "https://s.weibo.com/top/summary?cate=realtimehot"
        url = "https://www.baidu.com"
        if not test_proxy(proxy, url):
            count += 1
            print("Wrong Proxy: {}".format(proxy))
            remove_list.append(proxy)
            inst.delete_proxy(proxy)
    delete_proxy(remove_list)
    print("Total Count of Wrong Proxies: {}".format(count))
    print("Bad proxies have been removed. {}".format(remove_list))
    print("# of rest available proxies: {}".format(inst.get_proxies_num()))

    # if inst.get_proxies_num() < 10:
    #     with open("proxy.txt", 'a+') as file:
    #         for i in range(5):
    #             proxy_list = get_proxy(i + 1)
    #             file.writelines("%s\n" % proxy for proxy in proxy_list)


