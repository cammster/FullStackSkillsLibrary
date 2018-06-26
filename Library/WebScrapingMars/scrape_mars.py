##############################################################################################
# This script:
#   Scrapes 5 websites for information on Mars
#   Returns a dictionary containing information from each site
##############################################################################################

from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

##############################################################################################
def scrape():
    mars_dict={"stories":[],"image":[],"weather":[],"facts":[],"hemispheres":[]}

    ########################################################
    # Visit NASA News Site to get latest articles on Mars
    ########################################################
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url1)
    html=browser.html
    soup=bs(html,'html.parser')

    # Scrape stories from website
    for x in range(2):
        html = browser.html
        soup = bs(html, 'html.parser')    
        stories=soup.find_all('div', class_='list_text',)     
    #Extract 5 stories from scrape and store in dictionary
    for s in range(5):
        headline_date=stories[s].find('div',class_='list_date').text
        headline_title=stories[s].find('div',class_='content_title').text
        headline_p=stories[s].find('div',class_='article_teaser_body').text
        mars_dict["stories"].append({"dateposted":headline_date,"title":headline_title,"paragraph":headline_p})
       

    ########################################################
    # Visit JPL NASA site for Mars image
    ########################################################
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html=browser.html
    soup=bs(html,'html.parser')
    for link in soup.find_all('a',class_="button fancybox"):
        partial_link=link.get('data-fancybox-href')
    mars_dict["image"]=url2.split("/spaceimages")[0]+partial_link

    ########################################################
    # Visit Mars Twitter for the latest Weather Tweet
    ########################################################
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url3="https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    html=browser.html
    soup=bs(html,'html.parser')
    mars_dict["weather"]=soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    ########################################################
    # Visit Space Facts for Facts on Mars
    ########################################################
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url4="https://space-facts.com/mars/"
    browser.visit(url4)
    html=browser.html
    soup=bs(html,'html.parser')
    facts=[]
    for fact in soup.find_all('td', class_='column-1'):
        facts.append(fact.find("strong").text)
    values=[]
    for value in soup.find_all('td',class_="column-2"):
        values.append(value.text)
    mars_facts_df=pd.DataFrame({"Fact":facts,"Value":values})
    mars_facts_df.set_index("Fact",inplace=True)
    html_string=mars_facts_df.to_html()
    mars_dict["facts"]=html_string.replace("\n","")

    ########################################################
    # Visit Astrogeology Site for Mars Hemisphere Images
    ########################################################
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html=browser.html
    soup=bs(html,'html.parser')
    hemispheres=[]
    for hemi in soup.find_all("div",class_="item"):
        for link in hemi.find_all("img",class_="thumb"):
            part_link=link.get("src")
       
        hemispheres.append({"title": hemi.find("h3").text,"image":url5.split("/search")[0]+part_link})    
    mars_dict["hemispheres"]=hemispheres

    ###########################################################
    return mars_dict
    ###########################################################
