from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    

    #scrape the news -------------------------------------------
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    news_title = []
    news_p_text = []
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    articles = soup.find_all('div', class_='list_text')
    for article in articles:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        title = article.find('div', class_='content_title')
        news_title.append(title.text)
        p_ = article.find('div', class_ = 'article_teaser_body')
        news_p_text.append(p_.text)
    try:
        browser.click_link_by_partial_text('More')
          
    except:
        print("Scraping Complete")
    
    #scrape the feature images -------------------------------------------
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url = []
    # Retrieve all elements that contain book information
    a_tags = soup.find_all('a', class_="button fancybox")
    for a_tag in a_tags:
    #     print(a_tag)
        href = a_tag['data-fancybox-href']
        base_url = 'https://www.jpl.nasa.gov'
        featured_image_url = base_url + href
        image_url.append(featured_image_url)
        

    #scrape the weather -------------------------------------------
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    #scrape the data table -------------------------------------------
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.columns = ['Category', 'Data']
    df.set_index('Category', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')
    # df.to_html('table.html')
    

    #scrape the hemisphere images -------------------------------------------
    hemisphere_image_urls = [ 
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}
]
    # scrape dictionary
    mars_dict = {"mars_news_title": news_title[0],
                "mars_news_P": news_p_text[0],
                "featured_image": image_url[0],
                "Mars_facts": html_table,
                "hemisphere_images": hemisphere_image_urls}
    
    # print(mars_dict)
    return mars_dict
    
    # Quite the browser after scraping
    browser.quit()

scrape()