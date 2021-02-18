from logging import error
import uuid
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
from concurrent.futures import ThreadPoolExecutor

BASE_URL = os.environ.get("BASE_URL")


def generate_search_url(req, search_type):
    """
    Generate Search URL
    @param req: search string requested
    @param search_type: default(Book)=def or Author=Author
    @return: url string
    """

    params = {
        "res": 100,
        "req": req,
        "view": "detailed",
        "column": search_type,
        "sort": "def",
        "sortmode": "ASC",
        "page": 1,
    }

    url = f"{BASE_URL}/search.php?&res={params['res']}&req={params['req']}&phrase=1&view={params['view']}&column={params['column']}&sort={params['sort']}&sortmode={params['sortmode']}&page={params['page']}"

    return url


def test_url(url):
    """
    test the generated url
    @param url: generated search url
    @return: boolean
    """
    try:
        html = urlopen(url)
        BeautifulSoup(html, "lxml")

    except:
        return False

    return True


def get_book_data(table):
    book = {
        "ID": "",
        "Title": "",
        "Authors": "",
        "Language": "",
        "Publisher": "",
        "Year": "",
        "ISBN": "",
        "Edition": "",
        "No_of_Pages": "",
        "Size": "",
        "Extension": "",
        "Image_Url": "",
        "Quick_Download_Url": "",
    }

    # Get Book ID
    book["ID"] = str(uuid.uuid4())

    # Get Book Title
    data = str(table.find_all("td")[3])
    book["Title"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Author
    data = str(table.find_all("td")[6])
    book["Authors"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Publisher
    data = str(table.find_all("td")[12])
    book["Publisher"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Year
    data = str(table.find_all("td")[16])
    book["Year"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Edition
    data = str(table.find_all("td")[18])
    book["Edition"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Language
    data = str(table.find_all("td")[20])
    book["Language"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Pages
    data = str(table.find_all("td")[22])
    book["No_of_Pages"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book ISBN
    data = str(table.find_all("td")[24])
    book["ISBN"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Size
    data = str(table.find_all("td")[32])
    book["Size"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Extension
    data = str(table.find_all("td")[34])
    book["Extension"] = BeautifulSoup(data, "lxml").get_text()

    # Get Book url
    data = table.find_all("img")[0]
    book["Image_Url"] = f"{BASE_URL}{data.attrs['src']}"

    # Get Book QUick download url
    data = table.find_all("a")[0]
    book["Quick_Download_Url"] = f"{BASE_URL}{data.attrs['href']}"

    return book


def search_book(req, search_type):
    """
    search book
    @param url: generated search url
    @return: book object
    """
    # Define the response object

    class Books(object):
        records = []
        status = {"status_code": "", "reason": ""}
        record_num = ""

    url = generate_search_url(req, search_type)

    if test_url(url):
        print("True")
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        tables = soup.find_all("table", rules="cols")
        count = soup.find_all("font", color="grey", size="1")
        Books.record_num = count[0].get_text().split()[0]

        if len(tables) == 0:
            Books.status["status_code"] = 403
            Books.status["reason"] = "No books found, search for another book"

        else:
            tables = soup.find_all("table", rules="cols")
            for table in tables:
                try:
                    Books.records.append(get_book_data(table))
                    Books.status["status_code"] = 200
                    Books.status["reason"] = "Books found"

                except IndexError:
                    pass
    else:
        print("False")
        Books.status["status_code"] = 503
        Books.status["reason"] = "Service temporarily unavailable"

    return Books


# search_book(req = "docker", search_type = "def")
#
