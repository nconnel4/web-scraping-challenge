from splinter import Browser
from bs4 import BeautifulSoup as Soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

import logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def create_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    return browser


def open_page(browser, url):
    browser.visit(url)
    html = browser.html

    return html


def scrape_mars_news(html):
    news_soup = Soup(html, 'html.parser')

    element = news_soup.select_one('div.list_text')
    news_title = element.find('div', class_='content_title').get_text()
    logger.info(news_title)

    news_paragraph = element.find('div', class_='article_teaser_body').get_text()
    logger.info(news_paragraph)

    return news_title, news_paragraph


def scrape():
    browser = create_browser()
    html = open_page(browser, 'https://redplanetscience.com')

    news_title, news_paragraph = scrape_mars_news(html)



if __name__ == '__main__':
    scrape()