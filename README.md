# STEAM crawler

## Introduction

The repository is forked from the original branch by [aesuli](https://github.com/aesuli)/**[steam-crawler](https://github.com/aesuli/steam-crawler)** 

Within this edition, several editions and add-ons are made, which include revisions of, 0_view_data.py, 4_steam-review-extractor.py, 7_steam-review-check-duplicate.py, 8_steam-selenium-extractor.py, 9_steam-check-website-condition.py. 

Further details of the repository are written below.

<br/>

## Further Details of the Code
This set of scripts crawls STEAM website to download game reviews.

These scripts are aimed at students that want to experiment with text mining on review data.

The script have an order of execution.

  * **1_steam-game-crawler.py** download pages that lists games into ./data/games/

  * **2_steam-game-extractor.py** extracts games ids from the downloaded pages, saving them into ./data/games.csv
  
  * **3_steam-review-crawler.py** uses the above list to download game reviews pages into ./data/reviews
    This process can take a long time (it's a lot of data and the script sleeps between requests to be fair with the server).
    When the script is stopped and restarted it will skip games for which all reviews have been downloaded on the previous run (it does not downloads new reviews for such games).
  
  * **4_steam-review-extractor.py** extracts reviews and other info from the downloaded pages, saving them into ./data/reviews.csv 

  * **5_steam-reviews-stats.py**  is a sample script that processes the review.csv file and outputs some basic info and stats in json files.

  * **6_steam-review-check-duplicate.py** checks whether there are duplicated rows in the crawled data, and removing all while keeping the first record of them.

  * **7_steam-selenium-extractor.py** extracts traditional chinese review data of  given steam website, the process is facilitated by selenium package.

  * **8_steam-check-website-condition.py** check whether the game-id exists and would export a csv file which includes the games-id of those are valid.

Column in the reviews.csv file:
  * game id
  * number of people that found the review to be useful
  * number of people that found the review to be funny
  * username of the reviewer
  * number of games owned by the reviewer
  * number of reviews written by the reviewer
  * 1=recommended, -1=not recommended
  * hours played by the reviewer on the game
  * date of creation of the review
  * text of the review

The last script _steam-reviews-stats.py_ is a sample script that processes the review.csv file and outputs some basic info and stats in json files:

  * _./data/games.json_ number of reviews and played hours for every game.
  
  * _./data/users.json_ number of game owned (as reported by user's badge on STEAM) and number of played hours.
  
  * _./data/summary.json_ number of reviews, number of played hours, number of users, number of games.

On March 15, 2018 those last statistics are:

```
reviews        6614765
played hours 554702535
users          2720777
games            26677
```

