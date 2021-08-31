# Download timetable file


import requests
from bs4 import BeautifulSoup
import tabula
import os

from data import second

def get_html(url):
    r = requests.get(url)
    return r.text


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('div', property='content:encoded').find_all('a')
    return h1


def get_urlList(url):
    urlList = []
    for elem in get_data(get_html((url))):
        tmp = elem.get('href')
        if '.pdf' in tmp and 'https' in tmp:
            urlList.append(tmp)
    return urlList


def get_updates(urlList):
    r = requests.get(urlList[1], allow_redirects=True)
    open( '2.pdf', 'wb').write(r.content)
    tabula.convert_into('2.pdf', '2_1.csv', pages=1)
    tabula.convert_into('2.pdf', '2_2.csv', pages=2)
    tabula.convert_into('2.pdf', '2_3.csv', pages=3)


if __name__ == '__main__':
    url = 'https://cs.msu.ru/studies/schedule'
    get_updates(get_urlList(url))

