# web-scraping-challenge

## Background 

The purpose of this assignment was to build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The assignment was broken down into two portions: scraping and and flask application

### Scraping 

Initial scraping was completed using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

A Jupyter Notebook file called mission_to_mars.ipynb was used to complete all of the scraping and analysis tasks. The following sites were scraped for the associated information:

1. Mars News Info: https://redplanetscience.com/
2. Featured Mars Image: https://spaceimages-mars.com/
3. Mars Facts: https://galaxyfacts-mars.com/
4. Mars Hemisphere Images: https://marshemispheres.com/


### MongoDB and Flask Application

Using MongoDB with Flask, a new HTML page was created that displays all of the information that was scraped from the URLs above. The page has the following strucutre:

1. Mission to Mars button that scrapes for information from the sites above.
2. Latest Mars News Section
3. Featured Mars Image Section
4. Mars Facts Table
5. Mars Hemisphere Images 




