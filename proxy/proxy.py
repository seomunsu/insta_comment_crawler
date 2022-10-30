import requests

from bs4 import BeautifulSoup
from itertools import cycle


class Proxy:
    PROXY_URL = 'https://free-proxy-list.net/'

    def __init__(self):
        super(Proxy, self).__init__()
        response = requests.get('https://free-proxy-list.net/')
        soup = BeautifulSoup(response.text, 'html5lib')
        table = soup.find('tbody')
        list_tr = table.find_all('tr')
        list_td = [elem.find_all('td') for elem in list_tr]
        list_td = list(filter(None, list_td))
        list_ip = [elem[0].text for elem in list_td]
        list_ports = [elem[1].text for elem in list_td]
        list_proxies = [':'.join(elem) for elem in list(zip(list_ip, list_ports))]
        self.proxy_pool = cycle(list_proxies)
