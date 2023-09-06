# coding: utf-8

import os
from sys import getsizeof

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from decouple import config


ENV_SITE_URL = config("ENV_SITE_URL")
ENV_TERMS_QUERY = config("ENV_TERMS_QUERY")
ENV_CHROME_DRIVER_TARGET = config("ENV_CHROME_DRIVER_TARGET")

links = [
    "{0}?q={1}&tbm=isch".format(ENV_SITE_URL, terms)
    for terms in ENV_TERMS_QUERY.split(",")
]

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("--headless")
browser = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options,
)

list_data_ids = []

for url in links:
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

browser.close()
