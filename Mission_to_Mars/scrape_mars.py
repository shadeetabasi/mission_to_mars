from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    #Find a way to check this to ensure this is the right path???
     executable_path = {'executable_path': '/Users/shadeetabasi/.wdm/drivers/chromedriver/mac64/88.0.4324.96/chromedriver'}
     return Browser('chrome', **executable_path, headless=False) 

def scrape():
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    #create html object and parse with bs
    html = browser.html
    soup = bs(html, "html.parser")

    # scrape Mars latest news and recent title
    titles = soup.find_all("div", {"class":'content_title'})
    most_recent_title = titles[0]



