from bs4 import BeautifulSoup
import os
import urllib.request
import json

from color import Color
from file_helper import get_file_extension_from_content_type


def scrape_medals_and_flags(soup: BeautifulSoup) -> list[tuple[str, str, str, int, int, int, int]]:
    # Retrieves all lines containing data
    gold_medals_count = 0
    silver_medals_count = 0
    bronze_medals_count = 0
    div_elements = soup.find_all('div', class_='line')
    print(f"{len(div_elements) - 1} line(s) found")
    if len(div_elements) > 0:
        # Directory to store downloaded flag images
        download_dir = 'flag_images'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        cpt = 1
        result: list[tuple[str, str, str, int, int, int, int]] = []
        for div_line in div_elements:
            if div_line is None:
                print(Color.WARNING, "No next line, end of treatment" + Color.ENDC)
                break
            # Index is only used for logging
            try:
                index = div_line.findNext('div').get('data-row-id').replace("country-medal-row-", "")
            except AttributeError as attr_ex:
                print(Color.WARNING, f"End of treatment, there is no more row : {attr_ex.args}" + Color.ENDC)
                break
            print(f"treatment of line number :{index}")
            flag_img = div_line.findNext("img")
            if flag_img:
                country = flag_img.get('alt')
                flag_src = flag_img.get('src')
                img_name = flag_src.split('/')[-1]
                file_extension = get_file_extension_from_content_type(flag_src)
                # File extension has been found
                if file_extension != "file_extension_not_found":
                    img_filename = img_name + file_extension
                    # Download the image
                    print(f"Downloading : {img_filename}")
                    img_path = os.path.join(download_dir, img_filename)
                    try:
                        urllib.request.urlretrieve(flag_src, img_path)
                        print(Color.OKGREEN, f"Downloaded: {img_filename}" + Color.ENDC)
                    except IOError as io_ex:
                        print(Color.WARNING, f"Could not download: {img_filename} : {io_ex}" + Color.ENDC)
                        continue
                else:
                    print(Color.WARNING, "Cannot retrieve the file extension within content type !" + Color.ENDC)
                    continue
            else:
                print("Flag image not found !")
                continue

            div_line = div_line.find_next_sibling()
            if div_line:
                tri_letter_code = div_line.findNext('div', attrs={'data-cy': 'tri-letter-code'}).text
            else:
                print(Color.WARNING, "No tri-letter code found" + Color.ENDC)
                continue
            div_line = div_line.find_next_sibling()
            if div_line:
                # Gold medals
                try:
                    gold_medals_count = div_line.findNext('div', attrs={'title': 'Gold'}).text
                    if gold_medals_count == '-':
                        gold_medals_count = '0'
                except AttributeError as attr_ex:
                    if gold_medals_count is None:
                        print(Color.WARNING, f"No gold medal found : {attr_ex}" + Color.ENDC)
                        continue

            else:
                print(Color.WARNING, "No gold medal found" + Color.ENDC)
                continue
            div_line = div_line.find_next_sibling()
            if div_line:
                try:
                    # Silver medals
                    silver_medals_count = div_line.findNext('div', attrs={'title': 'Silver'}).text
                    if silver_medals_count == '-':
                        silver_medals_count = '0'
                except AttributeError as attr_ex:
                    if silver_medals_count is None:
                        print(Color.WARNING, f"No silver medal found : {attr_ex}" + Color.ENDC)
                        continue
            else:
                print(Color.WARNING, "No silver medal found" + Color.ENDC)
                continue
            div_line = div_line.find_next_sibling()
            if div_line:
                try:
                    # Bronze medals
                    bronze_medals_count = div_line.findNext('div', attrs={'title': 'Bronze'}).text
                    if bronze_medals_count == '-':
                        bronze_medals_count = '0'
                except AttributeError as attr_ex:
                    if bronze_medals_count is None:
                        print(Color.WARNING, f"No bronze medal found : {attr_ex}" + Color.ENDC)
                        continue
            else:
                print(Color.WARNING, "No bronze medal found" + Color.ENDC)
                continue
            str_total = f"{gold_medals_count} + {silver_medals_count} + {bronze_medals_count}"
            try:
                total_medals = eval(str_total)
            except Exception as e:
                print(Color.WARNING, "An error occurred calculating the total medals number !" + Color.ENDC, e)
                continue
            cpt += 1
            print(f"{country} , "
                  f"{tri_letter_code} , "
                  f"{flag_src} , "
                  f"{img_name} , "
                  f"{img_filename} , "
                  f"{gold_medals_count} , "
                  f"{silver_medals_count} , "
                  f"{bronze_medals_count} ,"
                  f"{total_medals} ")
            result.append((tri_letter_code, country, img_filename, int(gold_medals_count), int(silver_medals_count),
                           int(bronze_medals_count), int(eval(str_total))))

            try:
                # Write results to JSON file
                with open('medals-and-flags.json', 'w') as f:
                    json.dump(result, f)

                print(Color.OKGREEN, "Results written to sports.json" + Color.ENDC)
            except Exception as e:
                print(Color.FAIL, "An error occurred while writing to medals-and-flags.json ! " + Color.ENDC, e)

        print(f"{cpt - 1} retrieved out of {len(div_elements) - 1} lines")
        return result
    else:
        print(Color.FAIL, "Cannot retrieve the information .. no lines found !" + Color.ENDC)
