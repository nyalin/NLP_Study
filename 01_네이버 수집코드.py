# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
import urllib.request
import lib_common


TARGET = "naver"
ROOT_PATH = os.getcwd()
PYTHON_PATH = os.getcwd()
SAVE_DIR = os.path.join(ROOT_PATH, 'naverFile')


def crawling_data(oquery, date_str, channel):
    query = urllib.request.quote(oquery)
    base_url = "https://search.naver.com/search.naver?"
    url = base_url + "query=" + query + "&nso=so%3Ar%2Cp%3Afrom" + date_str + "to" + date_str + "%2Ca%3Aall&where=" + channel
    if channel == "cafe":
        url = base_url + "query=" + query + "&nso=so%3Ar%2Cp%3Afrom" + date_str + "to" + date_str + "%2Ca%3Aall&where=" + "article"

    SAVE_PATH = os.path.join(SAVE_DIR, oquery, date_str)
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    SAVE_FILE = os.path.join(SAVE_PATH, f"{TARGET}_{channel}_summary.txt")
    with open(SAVE_FILE, 'w', encoding="utf-8") as outfile:
        data = lib_common.crawling(url, TARGET, channel)
        for line in data:
            outfile.write("\t".join(line) + "\n")
    return


def read_textfile(path="keywords.txt"):
    tmp_data = []
    with open(path, 'r', encoding="utf8") as f:
        for line in f:
            line = line.strip("\r\n").strip()
            if line not in tmp_data:
                tmp_data.append(line)
    return tmp_data


def run_program(querylist=None, date_str=""):
    if querylist is None:
        # querylist = []
        return
    for query in querylist:
        print(TARGET, "--", query, ":", date_str)
        crawling_data(query, date_str, channel="blog")
        crawling_data(query, date_str, channel="cafe")
        crawling_data(query, date_str, channel="news")
    return


if __name__ == "__main__":
    # parameter
    crawling_summary = False
    s_date = "20220101"
    e_date = "20220102"
    queryfile = "keywords.txt"

    # setting
    sdate = datetime.strptime(s_date, "%Y%m%d")
    edate = datetime.strptime(e_date, "%Y%m%d")
    querylist = read_textfile(path=queryfile)

    date_str = sdate
    while edate >= date_str:
        run_program(querylist, date_str.strftime("%Y%m%d"))
        date_str = date_str + timedelta(days=1)
