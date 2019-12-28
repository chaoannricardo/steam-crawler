import numpy as np
import pandas as pd
import time
from selenium import webdriver

'''
def set_re_rules():
    # set re rules
    helpfulre = re.compile(r'([0-9]+) 個人認為這篇評論值得參考 ')
    funnyre = re.compile(r'([0-9]+) 個人認為這篇評論很有趣')
    ownedre = re.compile(r'此帳戶擁有 ([0-9]+) 款產品')
    # revre = re.compile(r'([0-9]+) review')
    timere = re.compile(r'總時數 ([0-9.]+) 小時')
    postedre = re.compile(r'張貼於：(.+)')
    # idre = re.compile(r'app-([0-9]+)$')
    # yearre = re.compile(r'.* [0-9][0-9][0-9][0-9]$')
    # userre = re.compile(r'/(profiles|id)/(.+?)/')
    return helpfulre, funnyre, ownedre, timere, postedre
'''


def crawling(name):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # tackle helpful list
        helpful_list = driver.find_elements_by_css_selector(".found_helpful")
        real_helpful_list = []
        funny_list = []
        for i, j in enumerate(helpful_list):
            check_if_two_row = j.text.split("\n")
            if len(check_if_two_row) > 1:
                # has multiple rows
                # append review list
                if check_if_two_row[0] == "目前尚未有人將此評論標記為值得參考":
                    real_helpful_list.append(0)
                else:
                    temp_list = check_if_two_row[0].split(" ")
                    real_helpful_list.append(temp_list[0])
                # append funny list
                temp_list = check_if_two_row[1].split(" ")
                funny_list.append(temp_list[0])
            else:
                # has single row
                funny_list.append(0)
                if j.text == "目前尚未有人將此評論標記為值得參考":
                    real_helpful_list.append(0)
                else:
                    split_list = j.text.split(" ")
                    real_helpful_list.append(split_list[0])
        # tackle recommend list
        rec_list = driver.find_elements_by_css_selector(".title")
        real_recommend_list = []
        for i, j in enumerate(rec_list):
            if j.text == "推薦":
                real_recommend_list.append("1")
            elif j.text == "不推薦":
                real_recommend_list.append("-1")
        # tackle posted list
        posted_list = driver.find_elements_by_css_selector(".date_posted")
        real_posted_list = []
        for i, j in enumerate(posted_list):
            temp_text = j.text.replace("張貼於：", "").replace("年", "/").replace("月", "/").replace("日", "").replace(" ", "")
            real_posted_list.append(temp_text)
        # tackle gaming hours
        gaming_hours = driver.find_elements_by_css_selector(".hours")
        real_gaming_hours = []
        for i, j in enumerate(gaming_hours):
            temp_text = j.text.replace("總時數 ", "").replace(" 小時", "")
            real_gaming_hours.append(temp_text)
        # tackle review text
        review_list = driver.find_elements_by_css_selector(".apphub_CardTextContent")
        real_review_list = []
        for i, j in enumerate(review_list):
            real_review_list.append(j.text)
        # tackle games count
        games_count = driver.find_elements_by_css_selector(".apphub_CardContentMoreLink")
        real_games_count_list = []
        for i, j in enumerate(games_count):
            temp_text = j.text.replace("此帳戶擁有 ", "").replace(" 款產品", "")
            real_games_count_list.append(temp_text)
        # create temp data
        temp_data = pd.DataFrame({
            'name': [name] * len(real_helpful_list),
            'useful_num': real_helpful_list,
            'funny_num': funny_list,
            'games_owned': real_games_count_list,
            'recommended': real_recommend_list,
            'hours_played': real_gaming_hours,
            'review_date': real_posted_list,
            'text': real_review_list
        })
        # append process
        temp_data.to_csv("./data/reviews.csv", mode='a', header=False, encoding='utf8', index=None)
        # Scroll down to bottom
        # reference: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        SCROLL_PAUSE_TIME = 2
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


if __name__ == '__main__':
    pd.options.display.max_colwidth = 100000000
    driver = webdriver.Firefox(executable_path='./geckodriver')

    # Left 4 dead 2
    html = 'https://steamcommunity.com/app/550/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=tchinese'
    driver.get(html)
    # age verification
    elem = driver.find_element_by_css_selector("#age_gate_btn_continue span")
    elem.click()
    crawling("Left 4 Dead 2")

    # Gears 5
    html = 'https://steamcommunity.com/app/1097840/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=tchinese'
    driver.get(html)
    # age verification
    elem = driver.find_element_by_css_selector("#age_gate_btn_continue span")
    elem.click()
    crawling("Gears 5")

    # DEAD OR ALIVE 6
    html = 'https://steamcommunity.com/app/838380/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=tchinese'
    driver.get(html)
    # age verification
    elem = driver.find_element_by_css_selector("#age_gate_btn_continue span")
    elem.click()
    crawling("DEAD OR ALIVE 6")

    # Garry's Mod
    html = 'https://steamcommunity.com/app/4000/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=tchinese'
    driver.get(html)
    crawling("Garry's Mod")

    # 真・三國無雙８
    html = 'https://steamcommunity.com/app/730310/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=tchinese'
    driver.get(html)
    crawling("真・三國無雙８")


