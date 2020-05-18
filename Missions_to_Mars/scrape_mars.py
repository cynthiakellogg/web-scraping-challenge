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
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')
    tweets = soup.find_all('span', class_= "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    weather_tweets = []
    for tweet in tweets:
        tweet_text = tweet.text
        if 'sol' in tweet_text:
            # print(f"Mars Weather Twitter Tweet:\n\n{tweet_text}")
            weather_tweets.append(tweet_text)
            break
        else: 
            pass
    #scrape the data table -------------------------------------------
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.columns = ['Category', 'Data']
    df.set_index('Category', inplace=True)
    html_table = df.to_html()
    new_table = html_table.replace('\n', '')
    
    
    #scrape the hemisphere images -------------------------------------------
    hemisphere_image_urls = [ 
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}
]
    # scrape dictionary
    mars_dict = {"mars_news_title": news_title,
                "mars_news_P": news_p_text,
                "mars_weather_tweet": weather_tweets,
                "featured_image": image_url,
                "Mars_facts": new_table,
                "hemisphere_images": hemisphere_image_urls}
    
    browser.quit()
    print(mars_dict)

    return mars_dict

scrape()