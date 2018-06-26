
### Web Scraping
This code extracts the latest information on Mars from 5 web sources: 
1. NASA News Site https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest
2. NASA Jet Propulsion Laboratory, California Institute of Technology https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
3. Mars Twitter Account https://twitter.com/marswxreport?lang=en
4. Mars Fact Page https://space-facts.com/mars/
5. Mars Hemispheres https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars


```python
from os import getcwd
from os.path import join
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import re
import pandas as pd
```


```python
mars_dict={"stories":[],"image":[],"weather":[],"facts":[],"hemispheres":[]}
```

#### 1. Nasa News Site


```python
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url1)
```


```python
html=browser.html
soup=bs(html,'html.parser')
```

Reference for how to write an html file if necessary:

    Html_file= open("Nasa_News_Site.html","w")
    Html_file.write(soup.prettify())
    Html_file.close()
    
    with open('Nasa_News_Site.html') as file:
        html = file.read()
        nasa_html = bs(html, 'lxml')
    stories=nasa_html.find_all('div',class_='list_text')


```python
for x in range(2):
    html = browser.html
    soup = bs(html, 'html.parser')
    
    stories=soup.find_all('div', class_='list_text') 
```


```python
for s in range(5):
        headline_date=stories[s].find('div',class_='list_date').text
        headline_title=stories[s].find('div',class_='content_title').text
        headline_p=stories[s].find('div',class_='article_teaser_body').text
        print("Date Posted:",headline_date)
        print("Story Title:",headline_title)
        print("Description:",headline_p)
        print("--------------------\n")
        mars_dict["stories"].append({"dateposted":headline_date,"title":headline_title,"paragraph":headline_p})
       
```

    Date Posted: April  6, 2018
    Story Title: Bound for Mars: Countdown to First Interplanetary Launch from California
    Description: On May 5, millions of Californians may witness the historic first interplanetary launch from America’s West Coast.
    --------------------
    
    Date Posted: March 30, 2018
    Story Title: NASA Invests in Visionary Technology 
    Description: NASA is investing in technology concepts, including several from JPL, that may one day be used for future space exploration missions.
    --------------------
    
    Date Posted: March 29, 2018
    Story Title: NASA is Ready to Study the Heart of Mars
    Description: NASA is about to go on a journey to study the center of Mars.
    --------------------
    
    Date Posted: March 28, 2018
    Story Title: ‘Marsquakes’ Could Shake Up Planetary Science
    Description: InSight, the next mission to the Red Planet, will use seismology to see into the depths of Mars.
    --------------------
    
    Date Posted: March 22, 2018
    Story Title: Mars Curiosity Celebrates Sol 2,000
    Description: NASA's Mars Curiosity rover just hit a new milestone: its two-thousandth Martian day on the Red Planet. An image mosaic taken recently offers a preview of what comes next.
    --------------------
    
    


```python
for story in mars_dict["stories"]:
    print(story["dateposted"])
    print(story["title"])
    print(story["paragraph"])

```

    April  6, 2018
    Bound for Mars: Countdown to First Interplanetary Launch from California
    On May 5, millions of Californians may witness the historic first interplanetary launch from America’s West Coast.
    March 30, 2018
    NASA Invests in Visionary Technology 
    NASA is investing in technology concepts, including several from JPL, that may one day be used for future space exploration missions.
    March 29, 2018
    NASA is Ready to Study the Heart of Mars
    NASA is about to go on a journey to study the center of Mars.
    March 28, 2018
    ‘Marsquakes’ Could Shake Up Planetary Science
    InSight, the next mission to the Red Planet, will use seismology to see into the depths of Mars.
    March 22, 2018
    Mars Curiosity Celebrates Sol 2,000
    NASA's Mars Curiosity rover just hit a new milestone: its two-thousandth Martian day on the Red Planet. An image mosaic taken recently offers a preview of what comes next.
    

#### 2. Mars Space Images


```python
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url2)
```


```python
html=browser.html
soup=bs(html,'html.parser')
```


```python
inspect=soup.find_all('a',class_="button fancybox")
inspect
```




    [<a class="button fancybox" data-description="The view was obtained during NASA's Cassini orbiter's flyby on July 24, 2012, also called the 'T85' flyby by the Cassini team. This was the most intense specular reflection that Cassini had seen to date." data-fancybox-group="images" data-fancybox-href="/spaceimages/images/mediumsize/PIA18433_ip.jpg" data-link="/spaceimages/details.php?id=PIA18433" data-title="Sunglint on a Hydrocarbon Lake" id="full_image">
     					FULL IMAGE
     				  </a>]




```python
for link in soup.find_all('a',class_="button fancybox"):
    partial_link=link.get('data-fancybox-href')
print(partial_link)

```

    /spaceimages/images/mediumsize/PIA18433_ip.jpg
    


```python
full_link=url2.split("/spaceimages")[0]+partial_link
full_link
```




    'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA18433_ip.jpg'




```python
mars_dict["image"]=full_link
mars_dict["image"]
```




    'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA18433_ip.jpg'



#### 3. Mars Twitter Account - Get Latest Tweet


```python
url3="https://twitter.com/marswxreport?lang=en"
```


```python
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url3="https://twitter.com/marswxreport?lang=en"
browser.visit(url3)
```


```python
html=browser.html
soup=bs(html,'html.parser')
```


```python
first_tweet=soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
first_tweet
```




    'Sol 2024 (April 16, 2018), Sunny, high -7C/19F, low -76C/-104F, pressure at 7.20 hPa, daylight 05:26-17:21'




```python
mars_dict["weather"]=first_tweet
mars_dict["weather"]
```




    'Sol 2024 (April 16, 2018), Sunny, high -7C/19F, low -76C/-104F, pressure at 7.20 hPa, daylight 05:26-17:21'



#### 4. Mars Facts


```python
url4="https://space-facts.com/mars/"
```


```python
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url4="https://space-facts.com/mars/"
browser.visit(url4)
```


```python
html=browser.html
soup=bs(html,'html.parser')
```


```python
facts=[]
for fact in soup.find_all('td', class_='column-1'):
    facts.append(fact.find("strong").text)
facts
```




    ['Equatorial Diameter:',
     'Polar Diameter:',
     'Mass:',
     'Moons:',
     'Orbit Distance:',
     'Orbit Period:',
     'Surface Temperature: ',
     'First Record:',
     'Recorded By:']




```python
values=[]
for value in soup.find_all('td',class_="column-2"):
    values.append(value.text)
values
```




    ['6,792 km\n',
     '6,752 km\n',
     '6.42 x 10^23 kg (10.7% Earth)',
     '2 (Phobos & Deimos)',
     '227,943,824 km (1.52 AU)',
     '687 days (1.9 years)\n',
     '-153 to 20 °C',
     '2nd millennium BC',
     'Egyptian astronomers']




```python
mars_facts_df=pd.DataFrame({"Fact":facts,"Value":values})
mars_facts_df.set_index("Fact",inplace=True)
mars_facts_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Fact</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Equatorial Diameter:</th>
      <td>6,792 km\n</td>
    </tr>
    <tr>
      <th>Polar Diameter:</th>
      <td>6,752 km\n</td>
    </tr>
    <tr>
      <th>Mass:</th>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>Moons:</th>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>Orbit Distance:</th>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>Orbit Period:</th>
      <td>687 days (1.9 years)\n</td>
    </tr>
    <tr>
      <th>Surface Temperature:</th>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>First Record:</th>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>Recorded By:</th>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
mars_dict["facts"]=mars_facts_df.to_html()
mars_dict["facts"]
```




    '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Value</th>\n    </tr>\n    <tr>\n      <th>Fact</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km\\n</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km\\n</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)\\n</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'



#### 5. Mars Hemispheres


```python
url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
```


```python
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url5)
```


```python
html=browser.html
soup=bs(html,'html.parser')
```


```python
hemispheres=[]
for hemi in soup.find_all("div",class_="item"):
    for link in hemi.find_all("img",class_="thumb"):
        part_link=link.get("src")
       
    hemispheres.append({"title": hemi.find("h3").text,"image":url5.split("/search")[0]+part_link})    
mars_dict["hemispheres"]=hemispheres
mars_dict["hemispheres"]
```




    [{'image': 'https://astrogeology.usgs.gov/cache/images/dfaf3849e74bf973b59eb50dab52b583_cerberus_enhanced.tif_thumb.png',
      'title': 'Cerberus Hemisphere Enhanced'},
     {'image': 'https://astrogeology.usgs.gov/cache/images/7677c0a006b83871b5a2f66985ab5857_schiaparelli_enhanced.tif_thumb.png',
      'title': 'Schiaparelli Hemisphere Enhanced'},
     {'image': 'https://astrogeology.usgs.gov/cache/images/aae41197e40d6d4f3ea557f8cfe51d15_syrtis_major_enhanced.tif_thumb.png',
      'title': 'Syrtis Major Hemisphere Enhanced'},
     {'image': 'https://astrogeology.usgs.gov/cache/images/04085d99ec3713883a9a57f42be9c725_valles_marineris_enhanced.tif_thumb.png',
      'title': 'Valles Marineris Hemisphere Enhanced'}]




```python

    
```




    []


