import base64

import requests
import fitz


# Wiki API for images
WIKI_IMAGE = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

# Wiki API for page summary
WIKI_SUMMARY = 'https://en.wikipedia.org/w/api.php?action=query&' \
               'format=json&prop=extracts&exintro=true&explaintext=true&titles='

# To mimic request from web browser
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'}


def get_image_data(query):
    api_res = requests.get(WIKI_IMAGE + query).json()
    page = api_res['query']['pages'].values()
    for value in page:
        if 'original' in value and 'source' in value['original']:
            url = value['original']['source']
            response = requests.get(url, headers=HEADER)
            return response.content
    return None


def get_summary(query):
    response = requests.get(WIKI_SUMMARY + query).json()
    pages = response["query"]["pages"]
    page_id = next(iter(pages), None)
    if page_id != "-1" and "extract" in pages[page_id]:
        return pages[page_id]["extract"]
    return "Page not found"


# noinspection PyUnresolvedReferences
def get_pdf_data(pdf_path):
    return fitz.open(stream=pdf_path.read(), filetype="pdf")


def convert_pdf_to_image(pdf_data, page):
    pix = pdf_data.load_page(page).get_pixmap(alpha=False)
    image_data = pix.tobytes("jpg")
    return image_data


def decode_image_data(image_data):
    return base64.b64encode(image_data).decode('ascii')
