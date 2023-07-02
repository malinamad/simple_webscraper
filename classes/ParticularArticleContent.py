from .Article import Article
import requests
from string import punctuation
from bs4 import BeautifulSoup


class ParticularArticleContent(Article):

    def __init__(self, page_num, artcl_type):
        super().__init__(page_num, artcl_type)
        self.saved_articles = []

    def get_selected_article_content(self, article_url):
        artcl_content = requests.get(article_url).content
        if artcl_content:
            article_soup = BeautifulSoup(artcl_content, 'html.parser')
            article_body = article_soup.find('body')
            return article_body

    def get_article_text(self, article_content):
        article_paragraphs = article_content.find_all('p', {'class': 'article__teaser'})
        article_text = [x.text for x in article_paragraphs]
        return article_text

    def prepare_article_title_as_file_name(self, article_title):
        article_title_text = article_title.text
        for mark in punctuation:
            if mark in article_title_text:
                article_title_text = article_title_text.replace(mark, '')
        file_name = article_title_text.replace(' ', '_')
        return file_name

    def save_the_article_as_file(self, article_text, file_name):
        with open(f'{file_name.strip()}.txt', 'w', encoding='utf-8') as f:
            f.writelines(article_text)
            self.saved_articles.append(f'{file_name.strip()}.txt')

    def main(self):
        page_content = self.get_pages_content()

        for article in page_content:
            artcl_type = self.get_article_type(article)

            if artcl_type.text == 'News':
                artcl_title = self.get_article_title(article)
                artcl_link = self.get_article_link(artcl_title)
                artcl_content = self.get_selected_article_content(artcl_link)

                # Saves file with article content
                artcl_txt = self.get_article_text(artcl_content)
                file_name = self.prepare_article_title_as_file_name(artcl_title)
                self.save_the_article_as_file(artcl_txt, file_name)
        ParticularArticleContent.__str__(self)

    def __str__(self):
        print('Saved articles:', self.saved_articles)
