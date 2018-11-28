

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url_nasa = 'https://mars.nasa.gov/news/'
    url_jplimages = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    url_facts = 'http://space-facts.com/mars/'
    url_himages = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    #  Create a dictionary to store all data
    mars_dict = {}




    # scrape nasa website
    response = requests.get(url_nasa)
    nasa_soup= BeautifulSoup(response.text, 'html.parser')

    news_title =nasa_soup.find('div',class_ ='content_title').text
    news_p =nasa_soup.find('div',class_ ='rollover_description_inner').text

    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    


    # scrape jpl website for Img
    response2 = requests.get(url_jplimages)
   
    jpl_soup= BeautifulSoup(response2.text, 'html.parser')
    title =jpl_soup.find('li',class_="slide").find('a',class_="fancybox")['data-fancybox-href']
    jpl_img= f'https://www.jpl.nasa.gov{title}'

    mars_dict['jpl_img'] = jpl_img



    # scrape mars weather

    response3 = requests.get(url_weather)

    wthr_soup= BeautifulSoup(response3.text, 'html.parser')
    mars_weather =wthr_soup.find('p', class_ = "tweet-text").text

    mars_dict['mars_weather'] = mars_weather



    # scrape mars fact table (need to figure out how to turn df to html)

    tables = pd.read_html(url_facts)
    df = tables[0]
    df.columns = ['fact', 'Value']
    df.set_index('fact', inplace=True)
    x=df.to_dict()
    marstbl_dict=x.pop('Value')
    # Export scraped table into an html script    
    mars_facts = df.to_html()
    mars_facts.replace("\n","")
    df.to_html('mars_facts.html')

    # Store html file to dictionary
    mars_dict['mars_facts'] = mars_facts

    mars_dict['marstbl_dict'] = marstbl_dict


     # scrape mars fact table (need to figure out how to turn df to html)

    hemisphere_image_urls= []

    for i in range (1,9,2): 
        
        hemi_dict = {}
        
        browser.visit(url_himages)
        hemi_html = browser.html
        hemi_soup = BeautifulSoup(hemi_html,'html.parser')
        hemi_name_links = hemi_soup.find_all('a', class_ = 'product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
        detail_links = browser.find_by_css('a.itemLink')
        detail_links[i].click()
        time.sleep(3)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(3)
        browser.windows.current = browser.windows[-1]
        
        hemi_img_html = browser.html
        
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()

        hemi_img_soup = BeautifulSoup(hemi_img_html,'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']
        
        print(hemi_name)
        hemi_dict['title'] = hemi_name.strip()
        
        print(hemi_img_path)
        hemi_dict['img_url'] = hemi_img_path
        
        hemisphere_image_urls.append(hemi_dict)
    
   
    hemiD = {item['title']:item for item in hemisphere_image_urls}


    # Store data in a dictionary
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls
       



    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict
