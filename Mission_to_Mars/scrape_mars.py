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
    mars_complete_data = {}

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #create html object and parse with bs
    html = browser.html
    soup = bs(html, "html.parser")

    ## 1. LATEST MARS NEWS: scrape Mars latest news and snippeets and isolate most recent title + paragraph
    titles = soup.find_all("div", {"class":'content_title'})
    most_recent_title = titles[0].text
    mars_complete_data['nasa_news_title'] = most_recent_title

    paragraphs = soup.find_all("div", {"class":'rollover_description_inner'})
    most_recent_paragraph = paragraphs[0].text
    mars_complete_data['nasa_news_snippet'] = most_recent_paragraph

    ## 2. JPL MARS SPACE IMAGE : scrape featured Mars Image
    mars_url = 'https://www.jpl.nasa.gov/images?query=mars'
    browser.visit(mars_url)
    #FIGURE OUT IF I NEED TO KEEP CHANGING html and soup name values
    html = browser.html
    soup = bs(html, 'html.parser')

    #Find all images, save first image and display
    mars_results = soup.find_all('img', class_="BaseImage object-contain")
    image_urls = [i['src'] for i in mars_results]
    featured_image_url = image_urls[0]
    mars_complete_data['featured_image'] = featured_image_url

    ## 3. MARS FACTS: Collect Mars facts using Pandas
    #Setting the URL to scrape
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_tables = pd.read_html(mars_facts_url)
    mars_facts_df = mars_facts_tables[0]
    updated_df = mars_facts_df.rename(columns={0: "Fact", 1: "Value"})
    #Save df to html string
    html_table = updated_df.to_html(index = False)
    #Clean up table
    final_html_table = html_table.replace('\n', '')
    mars_complete_data['mars_facts_table'] = final_html_table

    #4. HEMISPHERE DICTIONARY: 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Set open lists
    hemisphere_urls= soup.find_all('div', class_='item')
    hemisphere_titles = []
    img_urls = []
    img_urls_list = []

    #Run for loop to find titles and links to each individual hemisphere page
    for x in hemisphere_urls:
        #find h3 text
        hem_title = x.find('h3').text
        #append to list
        hemisphere_titles.append(hem_title)
        #find individual links to hemisphere pages
        img_url = x.find('a')['href']
        #append to list
        img_urls.append(img_url)
    #create full urls to visit    
    img_urls_list = ['https://astrogeology.usgs.gov' + url for url in img_urls]

    #Create open list for final jpg img urls in full size
    final_jpg_urls = []

    # For loop to pull out jpg urls
    for i in img_urls_list:
        #Visit and create html object for each link in img urls list
        browser.visit(i)
        html = browser.html
        soup = bs(html, 'html.parser')
        #search and find jpg links
        jpg_bucket = soup.find('div', class_='downloads')
        jpg_url = jpg_bucket.find('a')['href']
        #append to list
        final_jpg_urls.append(jpg_url)

    #Create dictionary to hold titles and img/jpg urls
    final_hemisphere_data = dict(zip(hemisphere_titles, final_jpg_urls))
    mars_complete_data['mars_hemispheres'] = final_hemisphere_data

    # Close the browser after scraping
    browser.quit()

    return mars_complete_data

#Debugged this updated code for my .py file by running through terminal with the below script
# mars_data = scrape()
# print(mars_data)