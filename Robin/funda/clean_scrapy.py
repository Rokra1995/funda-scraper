import pandas as pd

scraped_data = pd.read_csv('funda_2020.csv', sep=';')

for idx, img in scraped_data.iterrows():
    image_list = img.images.replace("[","").replace("]","").split("}, {")
    #print(image_list)
    string = image_list[0]
  
    Dict = dict((x.strip(), y.strip())  
             for x, y in (element.split(': ')  
             for element in string.split(', '))) 
    #print(Dict)
    path = Dict["'path'"]
    print(path)

