from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import urllib.request
from file_helper import get_file_extension_from_content_type
from typing import Dict


def download_country_flags(driver: webdriver) -> Dict[str, str]:
    # Find all img elements with src starting with the specified URL
    img_elements = driver.find_elements(By.XPATH,
                                        "//img[starts-with(@src, 'https://gstatic.olympics.com/s1/t_s_pog_flag/f_auto/static/flag/')]")
    flag_count = len(img_elements)
    print(f"{flag_count} flags found")
    # Directory to store downloaded flag images
    download_dir = 'flag_images'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    cpt = 1
    # Declaring a keymap to store the country names and its keys
    countries_keymap: Dict[str, str] = {}
    # Extract and print the src attributes of matching img elements
    for img_element in img_elements:
        country_name = img_element.get_attribute("alt")
        img_url = img_element.get_attribute("src")
        print("image url : " + img_url)
        file_extension = get_file_extension_from_content_type(img_url)
        if file_extension != "file_extension_not_found":
            img_name = img_url.split('/')[-1]  # Extracting image name from URL
            countries_keymap[img_name]=country_name
            img_name = img_name + file_extension
            print(f"Downloading : {img_name}")
            img_path = os.path.join(download_dir, img_name)

            # Download the image
            urllib.request.urlretrieve(img_url, img_path)
            print(f"OK ! - {cpt} : Downloaded: {img_path}")
            cpt = cpt + 1
        else:
            print(f"An error has occured downloading the {img_path}, file extension not found")

    print(f"{cpt - 1} downloaded out of {flag_count}")
    return countries_keymap
