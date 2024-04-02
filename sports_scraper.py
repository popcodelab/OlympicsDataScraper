from bs4 import BeautifulSoup
import os
import json

from color import Color
from file_helper import image_download
from sport_poster_scraper import retrieve_sport_poster

# Module to scrap all sport names
def scrape_sports(soup: BeautifulSoup) -> list[tuple[str, str, str]]:
    li_elements = soup.find_all('li', class_='b2p-sports-wrapper__item')
    print(f"{len(li_elements) - 1} line(s) found")
    if len(li_elements) > 0:
        cpt = 1
        result: list[tuple[str, str, str]] = []
        # Directory to store downloaded flag images
        download_dir = 'sports/icons'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        for li_element in li_elements:
            print(f"Sport n° {cpt}")
            if li_element is None:
                print("No next line, end of treatment")
                break
            sport_info_url = "https://olympics.com" + li_element.findNext('a', href=True).attrs['href']
            sport_name = li_element.findNext('span').text.strip()
            sport_icon = li_element.findNext('img').attrs['src']
            # Download the icon
            icon_filename = sport_icon.replace("/images/static/sports/pictograms/v2/", "")
            icon_url = "https://olympics.com" + sport_icon
            print(f"Downloading : {icon_filename} from {icon_url}")
            icon_path = os.path.join(download_dir, icon_filename)

            if image_download(icon_url, icon_path, icon_filename) is False:
                print(Color.FAIL, "Could not download {icon_filename} from {icon_url}" + Color.ENDC)
                continue
            sport_code = icon_filename.replace(".svg", "").upper()
            poster_filename = retrieve_sport_poster(sport_info_url, sport_code)

            print(f"{sport_name} - {sport_code} - {sport_icon} - {poster_filename} - {sport_info_url}")
            result.append((sport_name, icon_filename, poster_filename))
            cpt += 1
            print(f"{cpt - 1} retrieved out of {len(li_elements)} sports")
            try:
                # Write results to JSON file
                with open('sports.json', 'w') as f:
                    json.dump(result, f)

                print(Color.OKGREEN, "Results written to sports.json" + Color.ENDC)
            except Exception as e:
                print(Color.FAIL, "An error occurred while writing to sports.json ! " + Color.ENDC, e)
        print(f"{cpt - 1} retrieved out of {len(li_elements)} sports")
        return result
    else:
        print(Color.FAIL, "No data found, end of treatment" + Color.ENDC)
