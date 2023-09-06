# coding: utf-8

# import os
from datetime import datetime
from multiprocessing import Pool
from sys import getsizeof

# import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from decouple import config


ENV_SITE_URL = config("ENV_SITE_URL")
ENV_TERMS_QUERY = config("ENV_TERMS_QUERY")
ENV_CHROME_DRIVER_TARGET = config("ENV_CHROME_DRIVER_TARGET")

urls = [
    "{0}?q={1}&tbm=isch".format(ENV_SITE_URL, terms)
    for terms in ENV_TERMS_QUERY.split(",")
]


def scrapingImages(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )

    list_data_ids = []
    browser.get(url)

    html_parser = bs(browser.page_source, "html5lib")
    find_divs = html_parser.find_all("div", attrs={"data-id": True})

    # browser.implicitly_wait(2)

    for item in find_divs:
        if (
            item.attrs["data-id"]
            and 45 <= getsizeof(item.attrs["data-id"]) >= 60
        ):
            list_data_ids.append(item.attrs["data-id"])

    print(list_data_ids)
    print(len(list_data_ids))
    browser.close()


if __name__ == "__main__":
    start = datetime.now()
    print("Initial Time: ", start)
    with Pool(processes=2) as pool:
        pool.map(scrapingImages, urls)
    print("Finished Time: ", datetime.now())
    print("Total Time: ", datetime.now() - start)
