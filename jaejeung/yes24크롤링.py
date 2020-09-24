import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def get_book(soup):
    books_select = soup.select("#schMid_wrap > div:nth-child(3) > div.goodsList.goodsList_list > table > tbody > tr")
    
    result = []
    base_url = "http://www.yes24.com"
    temp = ""

    for book in books_select:
        if book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a > strong"):
            temp = book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a > strong").text
            if temp == book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a > strong").text:
                pass
        
            book_name = book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a > strong").text
            book_url = book.select_one("td.goods_infogrp > p.goods_name.goods_icon > a")["href"]
            image_url = book.select_one("td.goods_img > a > img")["src"]

            result.append([book_name, base_url+book_url, image_url])

    save_csv(result[:3])


def save_csv(result):
    result = pd.DataFrame(result)
    # print(result)
    result.to_csv("C:/Users/kojaejeung/Desktop/프로젝트/해커톤프로젝트/book_data/python_data.csv", header=False, index=False, encoding="cp949")


def main():
    # input_name = input()
    driver = webdriver.Chrome("C:/Users/kojaejeung/Desktop/class/9.etc/chromedriver_win32/chromedriver")
    driver.implicitly_wait(3)
    driver.get("http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query=%C6%C4%C0%CC%BD%E3")
    # driver.get("https://www.aladin.co.kr/home/welcome.aspx")
    # driver.find_element_by_name('SearchWord').send_keys(f"{input_name}")

    response = driver.page_source
    soup = BeautifulSoup(response, "html.parser")
    get_book(soup)

main()