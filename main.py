from bs4 import BeautifulSoup
from selenium import webdriver
from medals_and_flags_scraper import scrape_medals_and_flags

# URL of the page containing flag images
url = "https://olympics.com/en/olympic-games/tokyo-2020/medals"
print("access to : " + url)

options = webdriver.FirefoxOptions()
options.add_argument("--start-minimized")
driver = webdriver.Firefox(options=options)

# Grabbing a URL using the browser instance.
driver.get(url)

# Get the HTML page source code
page_source = driver.page_source

# Closing the browser instance
driver.quit()
# Initialize BeautifulSoup with the page source
soup = BeautifulSoup(page_source, 'html.parser')
data_lines = scrape_medals_and_flags(soup)
for data_line in data_lines:
    print(data_line)





