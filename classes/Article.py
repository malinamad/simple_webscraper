import requests
from bs4 import BeautifulSoup


class Article:
    url = 'https://www.nature.com'

    def __init__(self, page_num, artcl_type):
        self.pages_num = page_num
        self.artcl_type = artcl_type
        self.artcl_url = f'{self.url}/nature/articles?sort=PubDate&year=2020&page={page_num}'  # &page=3

    def get_pages_content(self):
        headers = {
            'Accept-Language': 'en-US,en;q=0.5'
        }
        resp = requests.request('GET', self.artcl_url, headers=headers)
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
