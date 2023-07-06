import base64

import requests
import fitz

from .contants import WIKI_IMAGE, WIKI_SUMMARY, HEADER


# This function is used to obtain the portrait of an author.
# It uses the name of the author to make a call towards Wiki API with the query:string.
# The response is iterated through and checked for 'original' and 'source' keys in the JSON response.
# If conditions are met the URL for the image is stored in the variable 'url', which is used to obtain the image data
def get_image_data(query):
    api_res = requests.get(WIKI_IMAGE + query).json()
    page = api_res['query']['pages'].values()
    for value in page:
        if 'original' in value and 'source' in value['original']:
            url = value['original']['source']
            response = requests.get(url, headers=HEADER)
            return response.content
    return None


# This function is used to obtain the summary of the Wiki page.
# It uses the title or name of the target to make a call towards Wiki API.
# We set page_id as the first key in the response dictionary.
# Then we check if the page exists (!= -1) and if it contains the key 'extract'.
# If conditions are met, we retrieve the summary as a string, if not we return a preset string.
def get_summary(query):
    response = requests.get(WIKI_SUMMARY + query).json()
    pages = response["query"]["pages"]
    page_id = next(iter(pages), None)
    if page_id != "-1" and "extract" in pages[page_id]:
        return pages[page_id]["extract"]
    return "Page not found"


# Open and read PDF via fitz library in PyMuPDF
def get_pdf_data(pdf_path):
    return fitz.open(stream=pdf_path.read(), filetype="pdf")


# Use data from get_pdf_data function to obtain a pixel map of the desired page of the PDF
# The pixel map is converted into bytes and returned for further processing
def convert_pdf_to_image(pdf_data, page):
    pix = pdf_data.load_page(page).get_pixmap(alpha=False)
    image_data = pix.tobytes("jpg")
    return image_data


# Ran into issues displaying the page image within the ReadBook view
# This decoder helps ensure that the convert_pdf_to_image is correctly encoded for Jinja
def decode_image_data(pdf_path, page):
    image_data = convert_pdf_to_image(pdf_path, page)
    return base64.b64encode(image_data).decode('ascii')


# Tool takes 4 random genres available in Genre model.
# It iterates through each genre and obtains Book model objects that fit the genre.
# The objects are ordered at random and the first 6 items are put into the dictionary as the values.

def get_books_by_genre(genre_model, book_model):
    genre_books = {}
    for genre in genre_model.objects.all().order_by('?')[:4]:
        filtered_books = book_model.objects.filter(genres=genre)
        genre_books[genre.genre] = filtered_books.order_by('?')[:6]
    return genre_books
