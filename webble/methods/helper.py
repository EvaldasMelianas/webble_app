import base64

import requests
import fitz

from .contants import WIKI_IMAGE, WIKI_SUMMARY, HEADER


def get_image_data(query):
    """
    This function is used to obtain the portrait of an author.

    :param query: Name of the author
    :return: Image data as response content
    """
    api_res = requests.get(WIKI_IMAGE + query).json()
    page = api_res['query']['pages'].values()
    for value in page:
        if 'original' in value and 'source' in value['original']:
            url = value['original']['source']
            response = requests.get(url, headers=HEADER)
            return response.content
    return None


def get_summary(query):
    """
    This function is used to obtain the summary of the Wiki page.

    :param query: Title or name of the target
    :return: Summary of the Wiki page or string if not 'extract'.
    """
    response = requests.get(WIKI_SUMMARY + query).json()
    pages = response["query"]["pages"]
    page_id = next(iter(pages), None)
    if page_id != "-1" and "extract" in pages[page_id]:
        return pages[page_id]["extract"]
    return "Page not found"


def get_pdf_data(pdf_path):
    """
    Open and read PDF via fitz library in PyMuPDF

    :param pdf_path: Path to the PDF file
    :return: PDF data
    """
    return fitz.open(stream=pdf_path.read(), filetype="pdf")


def convert_pdf_to_image(pdf_data, page):
    """
    Use data from get_pdf_data function to obtain a pixel map of the desired page of the PDF
    The pixel map is converted into bytes and returned for further processing

    :param pdf_data: PDF data
    :param page: Desired page number
    :return: Image data as bytes
    """
    pix = pdf_data.load_page(page).get_pixmap(alpha=False)
    image_data = pix.tobytes("jpg")
    return image_data


def decode_image_data(pdf_path, page):
    """
    This decoder helps ensure that the convert_pdf_to_image is correctly encoded for Jinja.

    :param pdf_path: Path to the PDF file
    :param page: Page number
    :return: Encoded image data
    """
    image_data = convert_pdf_to_image(pdf_path, page)
    return base64.b64encode(image_data).decode('ascii')


def get_books_by_genre(genre_model, book_model):
    """
    Tool takes 4 random genres available in Genre model.

    :param genre_model: Genre model
    :param book_model: Book model
    :return: Dictionary containing genres and 6 filtered books for each genre
    """
    genre_books = {}
    for genre in genre_model.objects.all().order_by('?')[:3]:
        filtered_books = book_model.objects.filter(genres=genre)
        genre_books[genre.genre] = filtered_books.order_by('?')[:6]
    return genre_books
