import pandas as pd


if __name__ == '__main__':
    # pandas option set
    pd.options.display.max_colwidth = 100000000
    temp_data = pd.read_csv("./data/reviews.csv", encoding='utf-8')
    temp_data.drop_duplicates(subset=['text'], keep='first', inplace=True)
    temp_data.to_csv("./data/reviews_final_checked.csv", header=True, index=None, encoding='utf-8')
