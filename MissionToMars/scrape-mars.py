import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    ##This will the 
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # The dictionary where we will store our scraped information
    mars_scrape = {}

    # scraping the title and article teaser and storing in the mars scrape dictionary
    mars_scrape['title'] = soup.find('div', class_='content_title').text
    mars_scrape['teaser'] = soup.find('div', class_='article_teaser_body').text
    browser.quit()
    
    # Opens browser to access page
    new_browser = Browser('chrome', **executable_path, headless=True)

    # storing mars image URL
    image_url = "https://spaceimages-mars.com/"
    new_browser.visit(image_url)

    new_html = new_browser.html

    # Parse HTML with Beautiful Soup
    new_soup = BeautifulSoup(new_html, 'html.parser')

    # Retrieve and storeall elements that contain header image information
    image_results = new_soup.find('img', class_='headerimage fade-in')['src']

    # storing image_rsults in mars_scrape
    mars_scrape['featured_img_url'] = image_url+image_results

    new_browser.quit()

    #storing facts table URL
    facts_url = "https://galaxyfacts-mars.com/"

    #read html to variable facts_df and then creating a dataframe to match example
    tables = pd.read_html(facts_url)

    facts_df = tables[0]

    facts_df.columns = ['','Mars','Earth']

    new_row = pd.DataFrame({"":"Description", " ":" ", " ":" "}, index=[0])

    facts_df = pd.concat([new_row, facts_df[:]]).reset_index(drop = True)

    facts_df = facts_df.fillna(" ")

    facts_df = facts_df.set_index(" ")

    facts_html = facts_df.to_html(border = 2)

    #scrape html table to mars_scraoe
    mars_scrape['facts_df'] = facts_html

    #storing hemisphere urls for each image
    hemi_url = "https://marshemispheres.com/"
    valles_url = hemi_url +"valles.html"
    cerbrus_url = hemi_url +"cerberus.html"
    schia_url = hemi_url +"schiaparelli.html"
    syrt_url = hemi_url +"syrtis.html"

    #create browsers for each hemisphere
    valles_browser = Browser('chrome', **executable_path, headless=True)
    cerb_browser = Browser('chrome', **executable_path, headless=True)
    schia_browser = Browser('chrome', **executable_path, headless=True)
    syrt_browser = Browser('chrome', **executable_path, headless=True)


    valles_browser.visit(valles_url)
    cerb_browser.visit(cerbrus_url)
    schia_browser.visit(schia_url)
    syrt_browser.visit(syrt_url)

    # HTML object
    valles_html = valles_browser.html
    cerb_html = cerb_browser.html
    schia_html = schia_browser.html
    syrt_html = syrt_browser.html

    # Parse HTML with Beautiful Soup
    valles_soup = BeautifulSoup(valles_html, 'html.parser')
    cerb_soup = BeautifulSoup(cerb_html, 'html.parser')
    schia_soup = BeautifulSoup(schia_html, 'html.parser')
    syrt_soup = BeautifulSoup(syrt_html, 'html.parser')

    #create list to store title & image
    hemi_title = []
    hemi_image_url = []

    #locating title and image for all hemispheres and storing in variables
    valles_name = valles_soup.find('h2', class_="title").text
    valles_image = valles_soup.find('img', class_="wide-image")['src']

    #append values to list
    hemi_title.append(valles_name)
    hemi_image_url.append(hemi_url+valles_image)

    valles_browser.quit()

    #locating title and image for all hemispheres and storing in variables
    cerb_name = cerb_soup.find('h2', class_="title").text
    cerb_image = cerb_soup.find('img', class_="wide-image")['src']

    #append values to list
    hemi_title.append(cerb_name)
    hemi_image_url.append(hemi_url+cerb_image)

    cerb_browser.quit()

    #locating title and image for all hemispheres and storing in variables
    schia_name = schia_soup.find('h2', class_="title").text
    schia_image = schia_soup.find('img', class_="wide-image")['src']

    #append values to list
    hemi_title.append(schia_name)
    hemi_image_url.append(hemi_url+schia_image)

    schia_browser.quit()

    #locating title and image for all hemispheres and storing in variables
    syrt_name = syrt_soup.find('h2', class_="title").text
    syrt_image = syrt_soup.find('img', class_="wide-image")['src']

    #append values to list
    hemi_title.append(syrt_name)
    hemi_image_url.append(hemi_url+syrt_image)

    syrt_browser.quit()

    hemisphere_image_urls = [
    {"title": hemi_title[0], "img_url": hemi_image_url[0]},
    {"title": hemi_title[1], "img_url": hemi_image_url[1]},
    {"title": hemi_title[2], "img_url": hemi_image_url[2]},
    {"title": hemi_title[3], "img_url": hemi_image_url[3]}
    ]

    #store dictionary with list for each hemisphere and scrape to mars_scrape
    mars_scrape['hemi_image_title'] = hemisphere_image_urls

    return mars_scrape
