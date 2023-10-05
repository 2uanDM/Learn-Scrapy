from src.utils.crawler import run_crawler
import os 


if __name__ == '__main__':
    save_folder = os.path.join(os.getcwd(), 'results')
    os.makedirs(save_folder, exist_ok=True)
    run_crawler(spider_name='quotes', nolog=False, filename='hello.json', overwrite = False)
