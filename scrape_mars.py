from splinter import Browser
from bs4 import BeautifulSoup as Soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def create_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    return browser


def open_page(browser, url):
    browser.visit(url)


def scrape():
    browser = create_browser()
    open_page(browser, 'https://redplanetscience.com')



if __name__ == '__main__':
    scrape()