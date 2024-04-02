from bs4 import BeautifulSoup
import os
import requests

from color import Color
from file_helper import image_download, get_file_extension_from_content_type


def retrieve_sport_poster(sport_infos_url, sport_code:str) -> str:
    print(f"Scraping sport {sport_code} infos from {sport_infos_url} ...")
    # Define headers with a user-agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # Send a GET request to the URL
    response = requests.get(sport_infos_url, headers=headers, verify=True)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_url = soup.find('source')['srcset']
        if image_url is not None:
            print(f"downloading the poster {image_url}")
            download_dir = 'sports/images'
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            image_extension = get_file_extension_from_content_type(image_url)
            if image_extension is not None and image_extension !="FILE_EXTENSION_NOT_FOUND":
                image_filename = sport_code + "." + image_extension
                #Clean image_filename in case
                image_filename= image_filename.replace("..",".")
                image_path = os.path.join(download_dir, image_filename)
                if image_download(image_url, image_path, image_filename) is False:
                    print(Color.WARNING, f"Could not download the poster {image_filename} from {image_url}"+Color.ENDC)
                    return "NO POSTER"
                else:
                    print(Color.OKGREEN, f"Downloaded the poster {image_filename}"+Color.ENDC)
                    return image_filename
            else:
                print(Color.FAIL, f"Could not download the poster from {image_url} : extension not found !"+Color.ENDC)
                return "NO POSTER"
        else:
            return "NO POSTER"
    else:
        print(Color.WARNING, f"Failed to retrieve the sport poster from {sport_infos_url} ! Status code: {response.status_code}"+Color.ENDC)
        return "NO POSTER"