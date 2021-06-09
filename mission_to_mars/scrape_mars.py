# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

def scrape():

    # Initialize PyMongo to work with MongoDBs
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Iterate through all pages
    news_titles = []
    news_ps = []

    for x in range(5):
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        # Retrieve all elements that contain article information
        articles = soup.find_all('div', class_='list_text')

        # Iterate through each article 
        for article in articles:
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
            news_title = article.find('div', class_='content_title').text
            news_p = article.find('div', class_='article_teaser_body').text
            print('-----------')
            print(news_title,'\n')
            print(news_p)
            
            news_titles.append(news_title)
            news_ps.append(news_p)

        # Click the 'Next' button on each page
        try:
            browser.links.find_by_partial_text('more').click()
            
        except:
            print("Scraping Complete")

    #Getting most recent article and sub-title
    news_title = news_titles[0]
    news_p = news_ps[0]

    #Closing browser session to move on to next site to scrape
    browser.quit()

    #Re-initialize PyMongo to work with MongoDBs
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Defining an HTML object to extract the featured image on the site
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information
    img = soup.find_all('img', class_='headerimage fade-in')

    #Combining original URL with the source path for the featured image
    featured_image_url = url + img[0]['src']

    #Closing browser session to move on to next site to scrape
    browser.quit()

    #Resetting the url definition for Mars fact scraping and accessing Mars facts with pandas
    url = 'https://galaxyfacts-mars.com/'
    mars_table_incoming = pd.read_html(url)

    #Convert incoming information into pandas dataframe
    mars_facts_df = mars_table_incoming[0]

    # Ref: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
    mars_facts_df = pd.DataFrame({"Attribute": mars_table_incoming[0][0], 
                              "Mars": mars_table_incoming[0][1],
                             "Earth": mars_table_incoming[0][2]})

    mars_facts_df = mars_facts_df.drop([0])
    mars_facts_df = mars_facts_df.set_index(keys="Attribute")

    #DataFrame to HTML
    mars_facts_df_html = mars_facts_df.to_html()

    #Cleaning HTML
    mars_facts_df_html = mars_facts_df_html.replace('\n','')

    
    #Re-initialize PyMongo to work with MongoDBs
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Iterate through the page to acquire HTML pages the four requested images
    hemisphere_page_urls = []

    for x in range(4):
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        # Retrieve all elements that contain book information
        thumbnails = soup.find_all('a', class_='itemLink product-item')

        for thumbnail in thumbnails:
            
            if thumbnail['href'] not in hemisphere_page_urls:
            
                hemisphere_page_urls.append(thumbnail['href'])
    
    #Ending session on landing page for hemispheres
    browser.quit()

    #Iterate through each page on website to pull full resolution image

    hemisphere_raw_urls = []
    base_url = 'https://marshemispheres.com/'
    
    for hemisphere in hemisphere_page_urls:
        
        if hemisphere != '#':
            
            executable_path = {'executable_path': ChromeDriverManager().install()}
            browser = Browser('chrome', **executable_path, headless=False)
            
            url = 'https://marshemispheres.com/' + hemisphere
            browser.visit(url)
        
            # HTML object
            html = browser.html
            # Parse HTML with Beautiful Soup
            soup = bs(html, 'html.parser')
            # Retrieve all elements that contain book information
            hem_img = soup.find_all('img', class_='wide-image')

        
            #Combining original URL with the source path for the featured image
            hemisphere_raw_urls.append(base_url + hem_img[0]['src'])

            browser.quit()
            
        if hemisphere == '#':
            
            browser.quit()

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": hemisphere_raw_urls[3]},
        {"title": "Cerberus Hemisphere", "img_url": hemisphere_raw_urls[0]},
        {"title": "Schiaparelli Hemisphere", "img_url": hemisphere_raw_urls[1]},
        {"title": "Syrtis Major Hemisphere", "img_url": hemisphere_raw_urls[2]},
    ]

    scraped_dictionary = {"news_title": news_title, 
                      "news_p": news_p, 
                      "featured_image":featured_image_url, 
                      "mars_table": mars_facts_df_html, 
                      "hemisphere_images": hemisphere_image_urls}


    return (scraped_dictionary)