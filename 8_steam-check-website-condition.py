from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import requests


def get_elem_text_list(elem):
    content_list = []
    for i, j in enumerate(elem):
        elem_text = elem[i].text
        content_list.append(elem_text)
    print(content_list)
    return content_list


def check_page_condition(html):
    is_exist = ""
    is_welcome = ""
    try:
        sessions = requests.session()
        sessions.headers[
            'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/34.0.1847.131 Safari/537.36 '
        r = sessions.get(html)
        if str(r.status_code) == "200":
            is_exist = "1"
            html_text = r.text
            soup = BeautifulSoup(html_text, "html.parser")
            results = soup.select("title")
            for i, j in enumerate(results):
                if i == 0:
                    if str(j) == "<title>Welcome to Steam</title>":
                        is_welcome = "1"
                    else:
                        is_welcome = "0"
        else:
            is_exist = "0"
            is_welcome = "0"
    except requests.exceptions.ConnectionError:
        is_exist = "0"
        is_welcome = "0"
    return is_exist, is_welcome


def crawl_review_data(html):
    community_link = "https://steamcommunity.com/app/"
    html_list = html.split("/")
    app_num = html_list[4]
    review_html = community_link + str(app_num) + "/reviews/?browsefilter=toprated&snr=1_5_100010_"
    print("Now Crawling Review: ", review_html)
    try:
        sessions = requests.session()
        sessions.headers[
            'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/34.0.1847.131 Safari/537.36 '
        r = sessions.get(review_html)
        # Check whether website exists
        if str(r.status_code) == "200":
            html_text = r.text
            soup = BeautifulSoup(html_text, "html.parser")
            results = soup.select(".learnMore a")
            for a, j in enumerate(results):
                if a == 0:
                    # if the website is a review site
                    if str(j) == '<a href="http://www.steampowered.com/reviews/">About Reviews</a>':
                        # Method reference: https://cloud.tencent.com/developer/article/1085988
                        print()
    except requests.exceptions.ConnectionError:
        print()


if __name__ == '__main__':
    # check_page_condition('https://www.sagjrhl.com')
    # check_page_condition('https://store.steampowered.com/app/813780/')
    # check_page_condition('https://store.steampowered.com/app/000000/')
    # sample_html = "https://store.steampowered.com/app/1200/Red_Orchestra_Ostfront_4145/"
    sample_html = "https://store.steampowered.com/app/570/"
    crawl_review_data(sample_html)
    '''
    website_data = pd.read_csv("./AllWebsiteCondition.csv")
    for i, j in enumerate(website_data.loc[:, 'html_link']):
        crawl_review_data(j)
    '''
