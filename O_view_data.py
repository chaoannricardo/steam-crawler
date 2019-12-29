import pandas as pd 

temp_data = pd.read_csv("./data/reviews_dead_or_alive_6.csv", encoding='utf-8')

print(temp_data.head())
print(temp_data.iloc[:, :7])


