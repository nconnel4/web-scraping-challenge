from splinter import Browser
from bs4 import BeautifulSoup as Soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

import logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class WebBrowser:

    def __init__(self):
        self.browser = self.create_browser()
        self.html = None

    @staticmethod
    def create_browser():
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

        return browser

    def open_page(self, url):
        self.browser.visit(url)
        self.load_page_html()

    def load_page_html(self):
        self.html = self.browser.html
        return self.html


def scrape_mars_news(web_browser):
    web_browser.open_page('https://redplanetscience.com')
    html = web_browser.html

    news_soup = Soup(html, 'html.parser')

    element = news_soup.select_one('div.list_text')
    news_title = element.find('div', class_='content_title').get_text()
    logger.info(news_title)

    news_paragraph = element.find('div', class_='article_teaser_body').get_text()
    logger.info(news_paragraph)

    return news_title, news_paragraph


def scrape_jpl_featured_image(web_browser):

    web_browser.open_page('https://spaceimages-mars.com/')
    html = web_browser.html

    image_element = web_browser.browser.find_by_tag('button')[1]
    image_element.click()

    html = web_browser.load_page_html()
    image_soup = Soup(html, 'html.parser')

    image_url = image_soup.find('img', class_='fancybox-image').get('src')
    logger.info(image_url)

    full_image_url = f'https://spaceimages-mars.com/{image_url}'

    return full_image_url


def scrape_mars_facts():
    mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]
    mars_df.columns = ['Description', 'Mars', 'Earth']
    mars_df.set_index('Description', inplace=True)

    logger.info(mars_df)
    return mars_df



def scrape():
    browser = WebBrowser()

    news_title, news_paragraph = scrape_mars_news(browser)
    jpl_featured_image_url = scrape_jpl_featured_image(browser)
    mars_facts = scrape_mars_facts()



if __name__ == '__main__':
    scrape()