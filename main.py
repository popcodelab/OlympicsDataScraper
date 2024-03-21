from bs4 import BeautifulSoup
from selenium import webdriver

from color import Color
from medals_and_flags_scraper import scrape_medals_and_flags
import sys

from sports_scraper import scrape_sports

# The first element of sys.argv is the script name itself
script_name = sys.argv[0]
# Command-line arguments start from the second element
arguments = sys.argv[1:]
# Print out the script name and arguments
print("Script Name:", script_name)
print("Arguments:", arguments)

if len(arguments) > 0:
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    if arguments[0] == "medals":
        print("scraping medals...")
        driver = webdriver.Firefox(options=options)
        #driver.minimize_window()
        # URL of the page containing flag images
        url = "https://olympics.com/en/olympic-games/tokyo-2020/medals"
        print("access to : " + url)

        # Grabbing a URL using the browser instance.
        driver.get(url)

        # Get the HTML page source code
        page_source = driver.page_source

        # Closing the browser instance
        driver.quit()

        # Initialize BeautifulSoup with the page source
        soup = BeautifulSoup(page_source, 'html.parser')
        data_lines = scrape_medals_and_flags(soup)
        if data_lines is not None:
            print("Display result list : ")
            for data_line in data_lines:
                print(data_line)
        else:
            print(Color.WARNING, "No data  found. Exit" + Color.ENDC)
    elif arguments[0] == "sports":
        print("scraping sports...")
        driver = webdriver.Firefox(options=options)
        #driver.minimize_window()
        # URL of the page containing sports information
        url = "https://olympics.com/en/sports/summer-olympics#tokyo-2020"
        print("access to : " + url)

        # Grabbing a URL using the browser instance.
        driver.get(url)

        # Get the HTML page source code
        page_source = driver.page_source

        # Closing the browser instance
        driver.quit()

        # Initialize BeautifulSoup with the page source
        soup = BeautifulSoup(page_source, 'html.parser')
        data_lines = scrape_sports(soup)
        if data_lines is not None:
            print("Display result list : ")
            for data_line in data_lines:
                if "NO POSTER" in data_line:
                    print(Color.WARNING + f"{data_line}" + Color.ENDC)
                else:
                    print(data_line)
        else:
            print(Color.FAIL, "No data  found. Exit" + Color.ENDC)
    else:
        print(Color.WARNING, "Wrong arguments" + Color.ENDC)
else:
    print("No arguments ! you should specify either : 'medals' either 'sports' as arguments")







