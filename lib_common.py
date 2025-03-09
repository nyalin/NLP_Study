#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time


ROOT_PATH = os.getcwd()
CHROMEDRIVER_PATH = os.path.join(ROOT_PATH, "chromedriver.exe")


def get_page(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read()
    response.close()
    return html


def get_naver_page_chromedriver(url, channel):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument('log-level=2')

    with webdriver.Chrome(CHROMEDRIVER_PATH, options=options) as browser:
        browser.implicitly_wait(1)
        browser.get(url)
        last_url = ""
        tmp_data = ""
        last_cnt = 0
        for i in range(40):
            time.sleep(1)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            html = browser.page_source
            soup_list = BeautifulSoup(html, features="html.parser")
            tmp_html = soup_list('ul', {'class': 'lst_total'})[0]
            list_html = tmp_html('li', {'class': 'bx'})
            tmp_url = list_html[-1].findAll('a')[0]['href']
            tmp_cnt = len(list_html)
            if tmp_cnt == last_cnt:
                break
            if i >= 33 and tmp_url == last_url:
                break
            last_url = tmp_url
            tmp_data = list_html
            last_cnt = tmp_cnt
    try:
        browser.close()
    except Exception as e:
        print(e)
        pass
    return tmp_data


def crawler_naver_news(base_url, channel):
    tmp_data = []
    max_count = 10
    cnt = 0
    while cnt < max_count:
        url = base_url + "&start=" + str(cnt * 10 + 1)
        tmp_html = get_page(url)

        tmp_html = BeautifulSoup(tmp_html, features="html.parser")
        soup_list = tmp_html('ul', {'class': 'list_news'})[0]
        soup_list = soup_list('li', {'class': 'bx'})
        print(url, "--", len(soup_list), "건 수집")

        for soup in soup_list:
            title = soup('a', {'class': 'news_tit'})[0].text.strip()
            summary_contents = soup('a', {'class': 'api_txt_lines dsc_txt_wrap'})[0].text.strip()
            try:
                link = soup('a', {'class': 'info'})[1]["href"]
            except IndexError:
                link = soup('a', {'class': 'news_tit'})[0]["href"]
            try:
                ref = soup('a', {'class': 'info press'})[0].text.replace("언론사 선정", "").strip()
            except IndexError:
                ref = soup('span', {'class': 'info press'})[0].text.replace("언론사 선정", "").strip()
            tmp_data.append([title, summary_contents, link, ref])

        cnt += 1
        time.sleep(3)

    return tmp_data


def crawler_naver_default(url, channel):
    tmp_html = get_naver_page_chromedriver(url, channel)
    # print(tmp_html)
    print(channel, "--", len(tmp_html), "건 수집")

    tmp_data = []
    for html in tmp_html:
        title = html('a', {'class': 'api_txt_lines total_tit'})[0].text.strip()
        summary_contents = html('div', {'class': 'api_txt_lines dsc_txt'})[0].text.strip()
        link = html('a', {'class': 'api_txt_lines total_tit'})[0]["href"]
        ref = ""
        tmp_data.append([title, summary_contents, link, ref])

    return tmp_data


def crawling(url, target, channel):
    tmp_data = []
    if target == "naver":
        if channel == "news":
            tmp_data = crawler_naver_news(url, channel)
        else:
            tmp_data = crawler_naver_default(url, channel)

    return tmp_data
