import requests
from bs4 import BeautifulSoup
from os import getcwd, path, mkdir


class Article:
    url = 'https://www.nature.com'

    def __init__(self):
        self.pages_num = int(input())
        self.artcl_type = input()
        self.artcl_url = f'{self.url}/nature/articles?sort=PubDate&year=2020&page={self.pages_num}'

    def get_page_link_number(self, page_num):
        artcl_url = f'{self.url}/nature/articles?sort=PubDate&year=2020&page={page_num}'
        return artcl_url

    def create_directory_with_page_num(self, page_num):
        cur_dir = getcwd()
        if path.isdir('articles') is False:
            cur_dir = getcwd()
            mkdir(cur_dir + '\\articles')

        dir_path = path.join(cur_dir, f'articles\\Page_{page_num}')
        if not path.isdir(f'articles\\Page_{page_num}'):
            mkdir(dir_path)

    def get_pages_content(self, article_url):
        headers = {
            'Accept-Language': 'en-US,en;q=0.5'
        }
        resp = requests.request('GET', article_url, headers=headers)
        if resp:
            soup = BeautifulSoup(resp.content, 'html.parser')
            all_artcls = soup.find_all('article')
            return all_artcls

    def get_article_type(self, article_content):
        artcl_type = article_content.find('span', {'class': 'c-meta__type'})
        return artcl_type

    def get_article_title(self, article_content):
        artcl_title = article_content.find('a', {'class': 'c-card__link'})
        return artcl_title

    def get_article_link(self, article_content):
        artcl_link_attr = article_content.get('href')
        artcl_link = self.url + artcl_link_attr
        return artcl_link
