# coding : UTF-8
import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

URL = 'https://movie.douban.com/subject/4920389/comments'

def get_content(url):

    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    # 需要在使用时更换cookie，否则只能爬取10页内容
    cookies = {'cookie': 'll="118094"; bid=aotCqzQpk2E; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=D7117608C8269DCAA3E3C34FD6B3B60D0|4896d757d54a51320711db1f9871b710; ap=1; ps=y; push_doumail_num=0; push_noty_num=0; __utmz=30149280.1522574190.6.2.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/4920389/comments; __utmv=30149280.13028; __utmz=223695111.1522576569.7.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ct=y; ck=TpN6; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1522739732%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.593009337.1522550220.1522593022.1522739732.10; __utmb=30149280.0.10.1522739732; __utma=223695111.1061134660.1522550221.1522593022.1522739732.10; __utmb=223695111.0.10.1522739732; _pk_id.100001.4cf6=366e6d7d6177aad7.1522550221.10.1522740886.1522594570.; dbcl2="130283083:WrRfm0FKKhE"'}
    timeout = random.choice(range(40000, 100000))

    while True:
        try:
            rep = requests.get(url, cookies = cookies, headers = header, timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8000, 15000)))
        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20000, 60000)))
        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30000, 80000)))
        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5000, 15000)))
    return rep.content

def parse_html(html_text):
    final = []
    bs = BeautifulSoup(html_text, 'html.parser')
    # 豆瓣
    review_list = bs.find('div', attrs={'class', 'article'})
    mod_bd = review_list.find('div', {'id': 'comments'})
    for comment in mod_bd.find_all('div'):
        temp = []
        if comment.find('div', {'class': 'comment'}) is not None:
            b = comment.find('span', {'class': 'comment-info'}).find('a').string
            a = comment.find('div', {'class': 'comment'}).find('p').string
            temp.append(b)
            if comment.find('span', {'class': 'allstar50 rating'}) is not None:
                # print(5)
                temp.append('5')
            elif comment.find('span', {'class': 'allstar40 rating'}) is not None:
                # print(4)
                temp.append('4')
            elif comment.find('span', {'class': 'allstar30 rating'}) is not None:
                # print(3)
                temp.append('3')
            elif comment.find('span', {'class': 'allstar20 rating'}) is not None:
                # print(2)
                temp.append('2')
            elif comment.find('span', {'class': 'allstar10 rating'}) is not None:
                # print(1)
                temp.append('1')
            else:
                temp.append('NULL')
            temp.append(a)
        final.append(temp)

    # 下一页
    next_page = bs.find('div', {'id': 'paginator'}).find('a', {'class': 'next'})
    if next_page:
        return final, URL + next_page['href']
    return final, None

def main():
    url = URL
    with open("douban.csv", 'w', encoding='utf8', newline='') as f:
        while url:
            html = get_content(url)
            result, url = parse_html(html)
            f_csv = csv.writer(f)
            f_csv.writerows(result)
            print(url)

if __name__ == '__main__':
    main()