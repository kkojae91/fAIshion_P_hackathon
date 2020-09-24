import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def get_book(soup):
    books_select = soup.select("#schMid_wrap > div > div.goodsList.goodsList_list > table > tbody > tr")
    # print(len(books_select))
    result = []
    base_url = "http://www.yes24.com"
    temp = ""
    field = ["python", "java", "javascript", "algorithm", "machinelearning", "deeplearning", "spring"]

    for book in books_select:
        if book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a > strong"):
            temp = book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a > strong").text
            if temp == book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a > strong").text:
                pass

            book_name = book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a > strong").text
            book_url = book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a")["href"]
            image_url = book.select_one("td.goods_img > a > img")["src"]
            result.append([field[1] ,book_name, base_url+book_url, image_url])

    # print(result[:3])
    save_csv(result[:3])


def save_csv(result):
    result = pd.DataFrame(result)
    # print(result)
    result.to_csv("C:/Users/kojaejeung/Desktop/프로젝트/해커톤프로젝트/book_data/java_data.csv", header=False, index=False, encoding="cp949")


def main():
    # input_name = input()
    driver = webdriver.Chrome("C:/Users/kojaejeung/Desktop/class/9.etc/chromedriver_win32/chromedriver")
    driver.implicitly_wait(3)
    # 검색어 파이썬
    driver.get("http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query=%C6%C4%C0%CC%BD%E3")
    # 검색어 딥러닝
    # driver.get("http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&Wcode=001_005&query=%B5%F6%B7%AF%B4%D7#")
    # 검색어 머신러닝
    # driver.get("http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query=%B8%D3%BD%C5%B7%AF%B4%D7")
    # 검색어 자바스크립트
    # driver.get("http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query=%C0%DA%B9%D9%BD%BA%C5%A9%B8%B3%C6%AE")
    # 검색어 스프링
    # driver.get("http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&qdomain=%c0%fc%c3%bc&query=%bd%ba%c7%c1%b8%b5&domain=BOOK&disp_no=001001003&scode=007_001")
    # 검색어 알고리즘
    # driver.get("http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&Wcode=001_005&query=%BE%CB%B0%ED%B8%AE%C1%F2")
    # 검색어 자바
    # driver.get("http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query=%C0%DA%B9%D9")
    # driver.get("https://www.aladin.co.kr/home/welcome.aspx")
    # driver.find_element_by_name('SearchWord').send_keys(f"{input_name}")

    response = driver.page_source
    soup = BeautifulSoup(response, "html.parser")
    get_book(soup)

main()