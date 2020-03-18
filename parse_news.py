from bs4 import BeautifulSoup
import requests
import sqlite3
import os
from context import *


if not os.path.exists(rowdata):
    os.makedirs(rowdata)


def generate_text_from_new(url):
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')

    element = soup.find('div', attrs={'class': 'article-body'})

    for c in element.children:
        if c.name == 'p':
            s = c.get_text()
            try:
                c.a.decompose()
            except AttributeError:
                pass
            if c.get_text():
                yield s


with sqlite3.connect(base_of_links) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, url FROM metadata WHERE file is NULL")
    for rowid, new in cursor.fetchall():
        print(new)
        file_name = f'{rowdata}/article{rowid}.txt'
        with open(file_name, 'w') as f1:
            f1.write('\n'.join(generate_text_from_new(new)))
        cursor.execute(f"UPDATE metadata SET file='{file_name}' WHERE rowid={rowid}")
