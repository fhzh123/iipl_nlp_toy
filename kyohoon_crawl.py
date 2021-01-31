# Import Modules
import os
import time
import argparse
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

def main(args):
    title_list = list()
    text_list = list()

    page = 1
    loop_start = False

    while True:
        main_url = f'http://www.inven.co.kr/board/lol/4625?sort=PID&p={page}'
        main_page = BeautifulSoup(requests.get(main_url).text, 'html.parser')
        ix_list = list()

        hot_text_cnt = len(main_page.findAll('span', {'class':'cmtnum'}))
        
        for i, date in enumerate(main_page.findAll('td', {'class':'date'})):
            if date.text.strip() == args.crawl_date:
                ix_list.append(i - hot_text_cnt)

        if len(ix_list) >= 1:
            loop_start = True
        else:
            page += 1
            time.sleep(0.4)

        if loop_start:
            if len(ix_list) >= 1:
                for i in tqdm(ix_list):
                    url = main_page.findAll('a', {'class': 'sj_ln'})[i]['href']
                    page = BeautifulSoup(requests.get(url).text, 'html.parser')
                    title_list.append(page.find('div', {'class':'articleTitle'}).text.replace(u'\xa0', u' '))
                    text_list.append(page.find('div', {'id': 'powerbbsContent'}).text.replace(u'\xa0', u' '))
                    time.sleep(0.3)
            else:
                break


    pd.DataFrame({
        'title': title_list,
        'text': text_list
    }).to_csv(os.path.join(args.save_path, f'{crawl_date}.csv'), index=False)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Naver Article Crawling')
    parser.add_argument('--save_path', type=str, default='./', help='Main directory')
    parser.add_argument('--crawl_date', type=str, default='01-30', help='Main directory')
    args = parser.parse_args()

    start_time = time.time()
    main(args)
    spend_time = (time.time() - start_time) / 60
    print('Done!; {:2.2%}min spend.'.format(spend_time))