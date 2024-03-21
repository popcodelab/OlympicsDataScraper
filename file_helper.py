import requests
import mimetypes

from color import Color


def _get_content_type(content_type):
    # Parse content type to get the subtype
    main_type, subtype = content_type.split('/')

    # Get the default extension corresponding to the subtype
    extension = mimetypes.guess_extension(content_type)

    # If no extension found, try to derive from subtype
    if not extension:
        if subtype == 'jpeg':
            extension = '.jpg'
        elif subtype == 'plain':
            extension = '.txt'
        else:
            extension = '.' + subtype

    return extension


def get_file_extension_from_content_type(content_url):
    response = requests.head(content_url)
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type")
        if content_type:
            file_extension = _get_content_type(content_type)
            print("Content-Type:", content_type)
            print("File Extension:", file_extension)
            return file_extension
        else:
            print(Color.WARNING,"Content-Type header not found."+Color.ENDC)
            return "file_extension_not_found"
    else:
        print(Color.FAIL, "Failed to retrieve the file extension."+Color.ENDC)
        return "FILE_EXTENSION_NOT_FOUND"


def image_download(image_url:str, download_path:str, image_filename) -> bool:
    try:
        #headers = {"User-Agent": "Mozilla/5.0"}
        # Define headers with a user-agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        # Send a GET request to the URL
        response = requests.get(image_url, headers=headers, verify=True)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a file in binary write mode
            with open(download_path, "wb") as f:
                # Write the content of the response to the file
                f.write(response.content)
            print(Color.OKGREEN, f"Image {download_path} downloaded successfully."+Color.ENDC)
        else:
            print(Color.WARNING, f"Failed to download image. Status code: {response.status_code}"+Color.ENDC)

        print(f"Downloaded: {image_filename}")
        return True
    except IOError as io_ex:
        print(Color.FAIL,f"Could not download: {image_filename} : {io_ex}"+Color.ENDC)
        return False