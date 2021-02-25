from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    #Find a way to check this to ensure this is the right path???
     executable_path = {'executable_path': '/Users/shadeetabasi/.wdm/drivers/chromedriver/mac64/88.0.4324.96/chromedriver'}
     return Browser('chrome', **executable_path, headless=False) 

def scrape():
    browser = init_browser()

    # Begin webscraping
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

