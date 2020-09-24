import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_book_image(soup):
    books_select = soup.select("#Search3_Result > div")
    image_url = []
    for book in books_select:
        image_url = book.select_one("table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > div > a > img")["src"]
    pass

def get_book(soup):
    books_select = soup.select("#Search3_Result > div")
    # print(len(books_select))
    result = []
    for book in books_select:
        book_name = book.select_one("table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li > a > b").text
        book_url = book.select_one("table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li > a")["href"]
        result.append([book_name,book_url])
    return result

def main():
    driver = webdriver.Chrome("C:/Users/kojaejeung/Desktop/chromedriver_win32/chromedriver")
    driver.implicitly_wait(3)
    driver.get("https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&KeyWord=%ED%8C%8C%EC%9D%B4%EC%8D%AC&KeyRecentPublish=0&OutStock=0&ViewType=Detail&SortOrder=2&CustReviewCount=0&CustReviewRank=0&KeyFullWord=%ED%8C%8C%EC%9D%B4%EC%8D%AC&KeyLastWord=%ED%8C%8C%EC%9D%B4%EC%8D%AC&CategorySearch=&chkKeyTitle=&chkKeyAuthor=&chkKeyPublisher=&chkKeyISBN=&chkKeyTag=&chkKeyTOC=&chkKeySubject=&ViewRowCount=25")

    response = driver.page_source
    soup = BeautifulSoup(response, "html.parser")
    print(get_book(soup))
    get_book_image(soup)

main()