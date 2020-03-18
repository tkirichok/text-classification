from bs4 import BeautifulSoup
import requests
import re
import sqlite3
from context import *


def search_main_hrefs(last_date):
    data = requests.get("https://www.foxnews.com/").text
    soup = BeautifulSoup(data, 'lxml')
    element = soup.find('div', attrs={'class': 'main main-secondary'})
    list_elem = element.find_all('header', attrs={'class': 'info-header'})

    pattern = re.compile(r'<span class="eyebrow"><a href="https://www\.fox\w*\.com/(.+?)">.*'
                         r'<span class="time" data-time-published="(.+?)">.*'
                         r'<a href="(.+?)">')

    for el in list_elem:
        for match in pattern.finditer(str(el)):
            if match[2] > last_date:
                print(match[1], match[2], match[3])
                yield match[1], match[2], match[3], None


with sqlite3.connect(base_of_links) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT ifnull(max(pub_date),'0') FROM metadata")
    max_pub_date = cursor.fetchone()[0]
    cursor.executemany("INSERT INTO metadata VALUES (?,?,?,?)", search_main_hrefs(max_pub_date))
    conn.commit()
