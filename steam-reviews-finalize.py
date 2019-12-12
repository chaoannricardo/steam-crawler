import pandas as pd


if __name__ == '__main__':
    # pandas option set
    pd.options.display.max_colwidth = 100000000
    temp_data = pd.read_csv("./data/reviews_final.csv.csv", header=True, encoding='utf-8')
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
    new_df.to_csv("./data/reviews_final_checked.csv", header=True, index=None, encoding='utf-8')
