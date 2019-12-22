#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Andrea Esuli (andrea@esuli.it)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import csv
import datetime
import json
import os
import re
import sys
import pandas as pd

from bs4 import BeautifulSoup


def extract_reviews(basepath, outputfile_name):
    helpfulre = re.compile(r'([0-9]+) [a-z]+? found this review helpful')
    funnyre = re.compile(r'([0-9]+) [a-z]+? found this review funny')
    ownedre = re.compile(r'([0-9]+) product')
    revre = re.compile(r'([0-9]+) review')
    timere = re.compile(r'([0-9.]+) hrs on record')
    postedre = re.compile(r'Posted: (.+)')
    idre = re.compile(r'app-([0-9]+)$')
    yearre = re.compile(r'.* [0-9][0-9][0-9][0-9]$')
    userre = re.compile(r'/(profiles|id)/(.+?)/')
    # pandas option set
    pd.options.display.max_colwidth = 100000000
    with open(outputfile_name, mode="w", encoding="utf-8", newline="") as outputfile:
        writer = csv.writer(outputfile)
        for root, _, files in os.walk(basepath):
            m = idre.search(root)
            if m:
                id_ = m.group(1)
            else:
                print('skipping non-game path ', root, file=sys.stderr)
                continue
            for file in files:
                fullpath = os.path.join(root, file)
                print('processing', fullpath)
                with open(fullpath, encoding='utf8') as f:
                    try:
                        soup = BeautifulSoup(json.loads(f.read())['html'], "html.parser")
                    except ValueError:
                        print('error on ', fullpath, file=sys.stderr)
                    # try-except to avoid Unbound local error
                    try:
                        for reviewdiv in soup.findAll('div', attrs={'class': 'review_box'}):
                            helpful = 0
                            funny = 0
                            elem = reviewdiv.find('div', attrs={'class': 'vote_info'})
                            if elem:
                                m = helpfulre.search(elem.text)
                                if m:
                                    helpful = m.group(1)
                                m = funnyre.search(elem.text)
                                if m:
                                    funny = m.group(1)
                            username = '__anon__'
                            elem = reviewdiv.find('div', attrs={'class': 'persona_name'})
                            if elem:
                                m = userre.search(str(elem.contents))
                                if m:
                                    username = m.group(2)
                            owned = 0
                            elem = reviewdiv.find('div', attrs={'class': 'num_owned_games'})
                            if elem:
                                m = ownedre.search(elem.text)
                                if m:
                                    owned = m.group(1)
                            numrev = 0
                            elem = reviewdiv.find('div', attrs={'class': 'num_reviews'})
                            if elem:
                                m = revre.search(elem.text)
                                if m:
                                    numrev = m.group(1)
                            recco = 0
                            elem = reviewdiv.find('div', attrs={'class': 'title ellipsis'})
                            if elem:
                                if elem.text == 'Recommended':
                                    recco = 1
                                else:
                                    recco = -1
                            time = 0
                            elem = reviewdiv.find('div', attrs={'class': 'hours ellipsis'})
                            if elem:
                                m = timere.search(elem.text)
                                if m:
                                    time = m.group(1)
                            posted = 0
                            elem = reviewdiv.find('div', attrs={'class': 'postedDate'})
                            if elem:
                                m = postedre.search(elem.text)
                                if m:
                                    posted = m.group(1).strip()
                                    if not yearre.match(posted):
                                        posted = posted + ", %s" % datetime.date.today().year
                            content = ''
                            elem = reviewdiv.find('div', attrs={'class': 'content'})
                            if elem:
                                content = elem.text.strip()
                            writer.writerow(
                                (id_, helpful, funny, username, owned, numrev, recco, time, posted, content))
                    except UnboundLocalError:
                        print(outputfile_name, " is a blank file, skipped.")
                '''
                # check if duplicate rows in every loop
                try:
                    # read in temp reviews data
                    temp_data = pd.read_csv("./data/reviews.csv", header=None, encoding='utf-8')
                    new_df = pd.DataFrame({
                        'game_id': temp_data.iloc[:, 0],
                        'useful_num': temp_data.iloc[:, 1],
                        'funny_num': temp_data.iloc[:, 2],
                        'user_name': temp_data.iloc[:, 3],
                        'games_owned': temp_data.iloc[:, 4],
                        'reviews_written': temp_data.iloc[:, 5],
                        'recommended': temp_data.iloc[:, 6],
                        'hours_played': temp_data.iloc[:, 7],
                        'review_date': temp_data.iloc[:, 8],
                        'text': temp_data.iloc[:, 9]
                    })
                    new_df.drop_duplicates(subset=['user_name', 'text'], keep='first', inplace=True)
                    # modify reviews data to ensure there is no duplicate rows
                    new_df.to_csv("./data/reviews.csv", header=True, index=None, encoding='utf-8')
                    new_df = pd.DataFrame()
                except pd.errors.EmptyDataError:
                    print('Review data is empty')
                '''


def main():
    parser = argparse.ArgumentParser(description='Extractor of Steam reviews')
    parser.add_argument(
        '-i', '--input', help='Input file or path (all files in subpath are processed)', default="./data/pages/reviews",
        required=False)
    parser.add_argument(
        '-o', '--output', help='Output file', default='./data/reviews.csv', required=False)
    args = parser.parse_args()

    extract_reviews(args.input, args.output)


if __name__ == '__main__':
    main()
