from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import urllib.request
from file_helper import _get_content_type, get_file_extension_from_content_type

# URL of the page containing flag images
url = "https://olympics.com/en/olympic-games/tokyo-2020/medals"
print("access to : " + url)

options = webdriver.FirefoxOptions()
# options.headless = True # This is normally the first google search after people find Selenium.
driver = webdriver.Firefox(options=options)

# Grabbing a URL using the browser instance.
driver.get(url)

# Find all img elements with src starting with the specified URL
img_elements = driver.find_elements(By.XPATH, "//img[starts-with(@src, 'https://gstatic.olympics.com/s1/t_s_pog_flag/f_auto/static/flag/')]")
flag_count = len(img_elements)
print(f"{flag_count} flags found")
# Directory to store downloaded flag images
download_dir = 'flag_images'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
cpt = 1
# Extract and print the src attributes of matching img elements
for img_element in img_elements:
    img_url = img_element.get_attribute("src")
    print("image url : " + img_url)
    file_extension = get_file_extension_from_content_type(img_url)
    if file_extension != "file_extension_not_found":
        img_name = img_url.split('/')[-1]  # Extracting image name from URL
        img_name = img_name + file_extension
        print(f"Downloading : {img_name}")
        img_path = os.path.join(download_dir, img_name)

        # Download the image
        urllib.request.urlretrieve(img_url, img_path)
        print(f"OK ! - {cpt} : Downloaded: {img_path}")
        cpt = cpt + 1
    else:
        print(f"An error has occured downloading the {img_path}")

print(f"{cpt-1} downloaded out of {flag_count}")
# Closing the browser instance
driver.quit()






