# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import requests
import pymongo

# DB setup
#client = pymongo.MongoClient('mongodb://localhost:27017')
#db = client.mars_db
#collection = db.mars 
 # ========================
 # Scraping NASA Mars News
 # ========================
def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    # scrape the NASA mars news site and collect latest info
    browser = init_browser()
    
    # The Mars News url 
    #print("Scraping Mars News...")

    # create dictionary to store all scrape data
    data_dict = {}
    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)
    time.sleep(5)

    # Collect the latest News Title and Paragraph Text
    html = browser.html
    soup = bs(html, "html.parser")
    
    # get the first <li> item under <ul> list of headlines: this contains the latest news title and paragraph text 
    first_li = soup.find('li', class_='slide')
    
    # save the news title under the <div> tag with a class of 'content_title' 
    news_title = first_li.find('div', class_='content_title').text
    print(f"News Title is: {news_title}")

    # save the paragraph text under the <div> tag with a class of 'article_teaser_body'
    news_para = first_li.find('div', class_='article_teaser_body').text
    print(f"News Paragraph is: {news_para}")

    
    # =====================================================
    # Scraping JPL Mars Space Images - Featured Mars Image
    # =====================================================

    # visit the url for the Featured Space Image website 
    jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_image_url)
    time.sleep(2)

    # create HTML object 
    html = browser.html
    # print(html)
    # parse HTML with BeautifulSoup
    soup = bs(html, "html.parser")
    # Retrieve image url
    image_url=soup.find_all('img')

    # Store url for latest featured image (index 1, after the NASA logo) into a variable for later
    featured_image_url = jpl_image_url + image_url[1].get("src")
    print(featured_image_url)
    
    # ====================
    # Scraping Mars Facts
    # ====================

    # url page to be scraped
    mars_facts_url = 'https://galaxyfacts-mars.com/'

    # using pandas to scrape tables
    facts_tables=pd.read_html(mars_facts_url)
    facts_tables

    mars_table = facts_tables[0]
    # convert the data of table into an html string
    mars_table.to_html('mars_facts_table.html')

    # =====================================
    # Scraping images for Mars Hemispheres
    # =====================================

    # URL of page to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # create html object
    html = browser.html
    # parsing with beautiful soup
    soup = bs(html, 'html.parser')
    # Finding all links on the main page for hemisphere pages and store link urls
    all_links = soup.find_all('a', class_='itemLink')
    # printing all links to see if it is scraped properly
    print(all_links)

    hemisphere_links = [all_links[0].get('href')]
    print(hemisphere_links)

    hemisphere_links.append(all_links[2].get('href'))

    print(hemisphere_links)

    hemisphere_links.append(all_links[4].get('href'))
    print(hemisphere_links)

    hemisphere_links.append(all_links[6].get('href'))
    print(hemisphere_links)

    # Create an empty list to store dictionaries
    mars_hemisphere_image_urls = []

    # Scrape links and visit each to find data
    for hemisphere in hemisphere_links:
        try:    
           # Go to hemisphere page
           hemisphere_url = url + hemisphere
           browser.visit(hemisphere_url)
           html = browser.html
           soup = bs(html, 'html.parser')
        
           # Store data of the title and image found
           title = soup.find_all('h2', class_='title')[0].text
           image_url = url + soup.find('img', class_='wide-image').get('src')
    
           # Create a dictionary of this data and append to list
           hemisphere_dict = {'Title': title, "Image_Url": image_url}        
           mars_hemisphere_image_urls.append(hemisphere_dict)
        
           # Go back to original page
           browser.visit(url)
    
        
        except Exception as e:
           print(e)

    # printing image urls of the hemispheres 
    print("Printing Image URL's of Mars Hemispheres")
    print("-----------------------------------------")
    mars_hemisphere_image_urls

    # Close the browser
    browser.quit()

    
    # Return results
    # creating dictionary of all the information scraped so far.
    mars_hemisphere_dict = {
    "news_title":news_title,
    "news_para":news_para,
    "featured_image_url":featured_image_url,
    "mars_facts":mars_table,
    "mars_hemisphere_image_urls":mars_hemisphere_image_urls
    }
    #mars_hemisphere_dict 
    
    # Return the dictionary to LOCATION
    return mars_hemisphere_dict

