from splinter import Browser
from bs4 import BeautifulSoup as Soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

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
        browser = Browser('chrome', **executable_path, headless=True)

        return browser

    def open_page(self, url):
        self.browser.visit(url)
        self.load_page_html()

    def load_page_html(self):
        self.html = self.browser.html
        return self.html


class MongoConnector:

    def __init__(self):
        self._conn = 'mongodb://localhost:27017'
        self._client = pymongo.MongoClient(self._conn)
        self._database = MongoConnector.database

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, db_name):
        self._database = self._client[db_name]

    def drop_collection(self, collection_name):
        self._database[collection_name].drop()


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


def scrape_mars_hemisphere_images(web_browser):
    url = 'https://marshemispheres.com'
    web_browser.open_page('https://marshemispheres.com')
    html = web_browser.html
    browser = web_browser.browser

    links = browser.find_by_css('a.product-item img')

    hemisphere_image_urls = []

    for link in range(len(links)):
        hemi_dict = {}
        logger.info(link)

        browser.find_by_css('a.product-item img')[link].click()
        hemi_name = browser.find_by_css('h2').value
        logger.info(hemi_name)

        sample = browser.find_by_text('Sample')
        logger.info(sample['href'])

        hemi_dict['name'] = hemi_name
        hemi_dict['img_url'] = sample['href']

        hemisphere_image_urls.append(hemi_dict)

        browser.back()

    return hemisphere_image_urls


def scrape():
    browser = WebBrowser()

    news_title, news_paragraph = scrape_mars_news(browser)
    jpl_featured_image_url = scrape_jpl_featured_image(browser)
    mars_facts = scrape_mars_facts()
    hemisphere_images = scrape_mars_hemisphere_images(browser)

    mongo_conn = MongoConnector()
    mongo_conn.database = "mars_db"
    db = mongo_conn.database

    mongo_conn.drop_collection('headline')
    db['headline'].insert_one(
        {'headline': news_title,
         'paragraph': news_paragraph}
    )

    mongo_conn.drop_collection('featured_image')
    db['featured_image'].insert_one(
        {'image_url': jpl_featured_image_url}
    )

    mongo_conn.drop_collection('mars_facts')
    logger.debug(mars_facts.to_dict())
    db['mars_facts'].insert_one(mars_facts.to_dict('index'))

    mongo_conn.drop_collection('hemisphere_images')
    db['hemisphere_images'].insert_many(hemisphere_images)


if __name__ == '__main__':
    scrape()
