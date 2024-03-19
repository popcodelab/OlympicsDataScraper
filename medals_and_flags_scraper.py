from bs4 import BeautifulSoup
import os
import urllib.request
from file_helper import get_file_extension_from_content_type


def scrape_medals_and_flags(soup: BeautifulSoup) -> list[tuple[str, str, str, int, int, int, int]]:
    # Retrieves all lines containing data
    global gold_medals_count, silver_medals_count, bronze_medals_count, country, flag_src, img_name, img_filename
    div_lines = soup.find_all('div', class_='line')
    print(f"{len(div_lines) - 1} line(s) found")
    if len(div_lines) > 0:
        # Directory to store downloaded flag images
        download_dir = 'flag_images'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        cpt = 1
        result: list[tuple[str, str, str, int, int, int, int]] = []
        for div_line in div_lines:
            # Find the next sibling element
            next_sibling = div_line.find_next_sibling()
            # Print the text of the next sibling element
            if next_sibling:
                # Index is only used for logging
                index = next_sibling.findNext('div').get('data-row-id').replace("country-medal-row-","")
                print(f"treatment of line number :{index}")
                flag_img = next_sibling.findNext("img")
                if flag_img:
                    country = flag_img.get('alt')
                    flag_src = flag_img.get('src')
                    img_name = flag_src.split('/')[-1]
                    file_extension = get_file_extension_from_content_type(flag_src)
                    # File extension has been found
                    if file_extension != "file_extension_not_found":
                        img_filename = img_name + file_extension
                        print(f"Downloading : {img_filename}")
                        img_path = os.path.join(download_dir, img_filename)
                        # Download the image
                        try:
                            urllib.request.urlretrieve(flag_src, img_path)
                            print(f"Downloaded: {img_filename}")
                        except IOError as io_ex:
                            print(f"Could not download: {img_filename} : ", io_ex)
                            continue
                    else:
                        print(f"Cannot retrieve the file extension within content type !")
                        continue
                else:
                    print("Flag image not found !")
                    continue
            if next_sibling is None:
                print("No next line, end of treatment")
                break
            next_sibling = next_sibling.find_next_sibling()
            if next_sibling:
                tri_letter_code = next_sibling.findNext('div', attrs={'data-cy': 'tri-letter-code'}).text
            else:
                print("No tri-letter code found")
                continue
            next_sibling = next_sibling.find_next_sibling()
            if next_sibling:
                # Gold medals
                try:
                    gold_medals_count = next_sibling.findNext('div', attrs={'title': 'Gold'}).text
                    if gold_medals_count == '-':
                        gold_medals_count = '0'
                except AttributeError as attr_ex:
                    if gold_medals_count is None:
                        print("No gold medal found : ", attr_ex)
                        continue

            else:
                print("No gold medal found")
                continue
            next_sibling = next_sibling.find_next_sibling()
            if next_sibling:
                try:
                    # Silver medals
                    silver_medals_count = next_sibling.findNext('div', attrs={'title': 'Silver'}).text
                    if silver_medals_count == '-':
                        silver_medals_count = '0'
                except AttributeError as attr_ex:
                    if silver_medals_count is None:
                        print("No silver medal found : ", attr_ex)
                        continue
            else:
                print("No silver medal found")
                continue
            next_sibling = next_sibling.find_next_sibling()
            if next_sibling:
                try:
                    # Bronze medals
                    bronze_medals_count = next_sibling.findNext('div', attrs={'title': 'Bronze'}).text
                    if bronze_medals_count == '-':
                        bronze_medals_count = '0'
                except AttributeError as attr_ex:
                    if bronze_medals_count is None:
                        print("No bronze medal found : ", attr_ex)
                        continue
            else:
                print("No bronze medal found")
                continue
            str_total = f"{gold_medals_count} + {silver_medals_count} + {bronze_medals_count}"
            try:
                total_medals = eval(str_total)
            except Exception as e:
                print("An error occurred calculating the total medals number !", e)
                continue
            cpt = cpt + 1
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

        print(f"{cpt - 1} retrieved out of {len(div_lines) - 1} lines")
        return result
    else:
        print("Cannot retrieve the information .. no lines found !")



