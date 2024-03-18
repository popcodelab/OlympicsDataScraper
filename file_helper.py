import requests
import mimetypes

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
            print("Content-Type header not found.")
            return "file_extension_not_found"
    else:
        print("Failed to retrieve the file extension.")
        return "file_extension_not_found"