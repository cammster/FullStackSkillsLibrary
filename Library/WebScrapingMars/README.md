# Web Scraping Mars Facts 
This application extracts the latest information on Mars from 5 web sources:
1. [NASA News Site](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest)
2. [NASA Jet Propulsion Laboratory, California Institute of Technology](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
3. [Mars Twitter Account](https://twitter.com/marswxreport?lang=en)
4. [Mars Fact Page](https://space-facts.com/mars/)
5. [Mars Hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

![Picture of App](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/WebScrapingMars/Images/OverallSitePicture.PNG)

## Tools Used: 
* Database: MongoDB (needed for storing pictures and easy to access keys using Jinga)
* Server: Flask application using Python
* Interactivity with Database and Web: PyMongo to access database, Beautiful Soup for web scraping
* Web: HTML / Bootstrap / Jinga

## How it Works:
When the app starts up, the html index references data from the last scraping session, which is stored in the MongoDB. 
Then, upon clicking "Get the Latest on Mars" button, the application runs the /scrape route.

* The Flask App 
To see more details on the /scrape route, open the [file](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/WebScrapingMars/scrape_mars.py)

![Mars Flask App](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/WebScrapingMars/Images/MarsAppCode.PNG)

* Mongo DB
This shows the breakdown of the data stored in Mongo.
![MongoDB for Mars Dictionary](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/WebScrapingMars/Images/MarsMongoPic.PNG)

* HTML and Jinga
This shows the notation used in the html code to reference the Mars dictionary stored in Mongo. 
![HTML Code](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/WebScrapingMars/Images/MarsHTMLJinga.PNG)

## To Run the App: 
This app runs locally, so the user has to take the following steps to run it: 
1. Run mongo
* Open cmd line
* Type "mongod"
2. Run the mars_app.py
* Open anaconda prompt and navigate to folder containing the app
* Type "python mars_app.py"

## Limitations
* The /scrape route is very specific using Beautiful Soup to parse the websites as they existed when this app was built, so any 
changes to the html code could result in the app not parsing the correct information from the websites.
* Also, adding a "Last Updated" date would give tell the user the age of the information initially displayed. 


