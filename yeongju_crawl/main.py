# Import Modules
import os
import time
import argparse

# Import Custom Modules
from article_crawl import article_crawl

def main(args):
    #Path Setting
    crawl_dir = os.path.join(args.main_dir, args.crawl_dir)
    if not os.path.exists(args.crawl_dir):
        os.mkdir(crawl_dir)
    article_crawl(args)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Naver Article Crawling')
    parser.add_argument('--main_dir', type=str, default='./',
                        help='Main directory')
    parser.add_argument('--crawl_dir', type=str, default='crawl', 
                        help='Main directory of crawled data')
    parser.add_argument('--keyword', type=str, default="소울")

    args = parser.parse_args()
    
    start_time = time.time()
    main(args)
    spend_time = (time.time() - start_time) / 60
    print('Done!; {:2.2%}min spend.'.format(spend_time))
