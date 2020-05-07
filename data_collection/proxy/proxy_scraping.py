from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def get_proxy(page_no):
    url = "https://www.xicidaili.com/nn/{}".format(page_no)
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
    response = urlopen(req)
    assert (response.getcode() == 200)
    response = response.read()

    result = []

    container = BeautifulSoup(response, 'html.parser')
    proxy_ips = container.table.find_all('tr')[1:]
    for proxy_ip in proxy_ips:
        elements = proxy_ip.find_all('td')
        protocol = elements[5].text
        if protocol != 'HTTPS':
            continue
        ip = elements[1].text
        port = elements[2].text
        proxy = "https://{}:{}".format(ip, port)
        result.append(proxy)

    return result


with open("proxy.txt", 'w+') as file:
    for i in range(5):
        proxy_list = get_proxy(i + 1)
        file.writelines("%s\n" % proxy for proxy in proxy_list)
