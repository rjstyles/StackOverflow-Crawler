import requests
from bs4 import BeautifulSoup
import operator
import os
import sys


Tag_Rank = {}


def tag_crawler(url):
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    for tag_div in soup.find_all('div', {'class': 'post-taglist'}):
        for tag_link in tag_div.find_all('a'):
            tag = tag_link.string
            if tag in Tag_Rank:
                Tag_Rank[tag] += 1
            else:
                Tag_Rank[tag] = 1


def ques_links_crawler(base_url, end_url, page_limit):
    page_no = 1
    while page_no <= page_limit:
        page_url = base_url + str(page_no) + end_url
        source_code = requests.get(page_url).text
        soup = BeautifulSoup(source_code, 'html.parser')
        if page_no is 1:
            os.system('clear')
        print('crawling page ' + str(page_no) + ': [', end='')
        prev_len = 0
        q_no = 1
        for ques_link in soup.find_all('a', {'class': 'question-hyperlink'}):
            url = 'http://stackoverflow.com/' + ques_link.get('href')
            tag_crawler(url)
            for _ in range(prev_len):
                print('\b', end='')
            print('#', end='')
            p_cent = q_no*2
            percent = '] (' + str(p_cent) + '%)'
            prev_len = len(percent)
            print(percent, end='')
            sys.stdout.flush()
            q_no += 1
        page_no += 1


def start():
    page_limit = int(input('Enter no. of pages to crawl : '))
    os.system('clear')
    print('starting crawling...')
    ques_links_crawler('http://stackoverflow.com/questions?page=', '&sort=newest', page_limit)
    fw = open('Tags_frequency3.txt', 'w')
    for key, value in sorted(Tag_Rank.items(), key=operator.itemgetter(1), reverse=True):
        try:
            fw.write(key + " : " + str(Tag_Rank[key]) + "\n")
        except TypeError:
            continue
    print('\nResult saved to file Tags_frequency.txt')

start()
