import os
import time
import json
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def article_crawl(args):

    fwrite = open(f"{args.crawl_dir}/result.csv", 'w', encoding='utf-8')
    
    # 1~10 페이지
    for n in range(1, 100, 10):
        main_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+str(args.keyword)+"&start="+str(n)
        main_page = BeautifulSoup(requests.get(main_url).text, 'lxml')

        articles = main_page.find("div", {"class":"group_news"}).findAll("li", {"class": "bx"})
        for article in articles:
            title = article.find("a", {"class":"news_tit"}).get_text()
            press = article.find("a", {"class":"info press"}).get_text()
            print(title + " | " + press)

            article_url = article.find("a")["href"]
            print(article_url)

            title = title.replace(",", "")
            # 언론사 이름만 추출
            press = press.replace("언론사 선정", "")
                  
            fwrite.write(title + ',' + press + '\n')

    fwrite.close()
