
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Setup splinter
def scrape():
    executable_path = {"executable_path" : ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    
    # -- Get News Title and Paragragh Text --

    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scrape and collect the latest News Title and Paragraph Text.

    web_news_titles = soup.find_all("div", class_="content_title")
    news_title = web_news_titles[0].text

    web_news_paragraphs = soup.find_all("div", class_="article_teaser_body")
    news_paragraph = web_news_paragraphs[0].text

    # -- Get JPL Mars Space Images—Featured Image --

    Image_url = "https://spaceimages-mars.com/"
    browser.visit(Image_url)
    Image_html = browser.html
    Image_soup = BeautifulSoup(Image_html, "html.parser")
    
    # Pick the feature image

    Image_features = Image_soup.find("a", class_="showimg fancybox-thumbs")
    Feature_image_source = Image_features["href"]

    #Get feature image url

    feature_image_url = Image_url + Feature_image_source

    # -- Get Mars Facts --

    Facts_url = "https://galaxyfacts-mars.com"

    Facts_tables = pd.read_html(Facts_url)
    Mars_facts = Facts_tables[1]
    Mars_facts.columns = ["Description","Data"]
    Mars_facts_tables = Mars_facts.to_html(classes="table table-striped")
    

    # -- Mars Hemispheres --

    Mars_url = "https://marshemispheres.com/"
    browser.visit(Mars_url)
    Mars_html = browser.html
    Mars_soup = BeautifulSoup(Mars_html, "html.parser")

    Hemispheres = Mars_soup.find("div", class_= "collapsible results")
    Each_Hemp = Hemispheres.find_all("div", class_= "item")
    Each_Hemp_Title_Image = []

    for Hemp in Each_Hemp:

        try:
            # Get title
            Get_title = Hemp.find("div", class_="description")
            Title = Get_title.h3.text
            
            # Get image url
            Each_Hemp_Page = Get_title.find("a", class_="itemLink product-item")
            
            Hemp_Url = Each_Hemp_Page["href"]
            Link_Url = Mars_url + Hemp_Url
            browser.visit(Link_Url)
            
            Hemp_html = browser.html
            Hemp_soup = BeautifulSoup(Hemp_html,"html.parser")
            
            Hemp_Image_Url = Hemp_soup.find("li").a["href"]
            Image_Url_Link = Mars_url + Hemp_Image_Url
            
            # Create dictionary for title and url
            Hemp_dict = {"title": Title, "image_url": Image_Url_Link}
            Each_Hemp_Title_Image.append(Hemp_dict)
            
        except:
            print("Scraping Complete")

    browser.quit()

    hemp1 = Each_Hemp_Title_Image[0]["title"]
    image1 = Each_Hemp_Title_Image[0]["image_url"]
    
    hemp2 = Each_Hemp_Title_Image[1]["title"]
    image2 = Each_Hemp_Title_Image[1]["image_url"]

    hemp3 = Each_Hemp_Title_Image[2]["title"]
    image3 = Each_Hemp_Title_Image[2]["image_url"]

    hemp4 = Each_Hemp_Title_Image[3]["title"]
    image4 = Each_Hemp_Title_Image[3]["image_url"]
    
    # Store scraped data into dictionary
    mars_dict = {
        "recent_news_title": news_title,
        "recent_news_paragraph": news_paragraph,
        "featured_image_url": feature_image_url,
        "facts": Mars_facts_tables,
        "mars_hemispheres": Each_Hemp_Title_Image,
        "hemp1": hemp1,
        "hemp2": hemp2,
        "hemp3": hemp3,
        "hemp4": hemp4,
        "image1": image1,
        "image2": image2,
        "image3": image3,
        "image4": image4,
    }
    
    return mars_dict
    
    
          




