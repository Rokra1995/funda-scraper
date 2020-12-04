import pandas as pd

scraped_data = pd.read_csv('funda_2020.csv', sep=';')
print(scraped_data.iloc[0])
print(scraped_data)
#print(scraped_data.groupby(['image','objects']).count())
