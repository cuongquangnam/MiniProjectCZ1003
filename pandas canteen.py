import pandas as pd
from pandas import DataFrame

df = pd.read_excel('canteen_db.xlsx')
df['Menu Item'] = df['Menu Item'].str.lower() #convert menu item column to lowercase for search

#takes in foodtype = ['Food1','food2' etc], if no input = []
#pricerange = [lower, higher as floats/int], if no input = [0,0]
#rating = int(1 to 5) or 0 if not specified
#search = string or '' if no input 
def searchfood(foodtype,pricerange,rating,search):
    #copy the dataframe to temporary. 
    search_df = df.copy()
    #filter by foodtype
    if foodtype != []: 
        foodcond = search_df['Food Type'].isin(foodtype)
        search_df = search_df[foodcond]
    # filter by price range
    if pricerange != [0,0]:
        low_price = pricerange[0]
        high_price = pricerange[1] 
        pricecond1 = search_df['Price'] >= low_price
        pricecond2 = search_df['Price'] <= high_price
        search_df = search_df[ pricecond1 & pricecond2 ]
    # filter by rating, shows all above specified rating
    if rating != 0: 
        ratingcond = search_df['Rating'] >= rating
        search_df = search_df[ ratingcond ]
    # filter by menu item
    if search != '':
        menucond = search_df['Menu Item'].str.contains(search)
        search_df = search_df[ menucond ]
    # Transform results to list 
    canteen = search_df['Canteen'].tolist()
    stall = search_df['Stall'].tolist()
    food = search_df['Food Type'].tolist()
    menu = search_df['Menu Item'].tolist()
    price = search_df['Price'].tolist()
    ratings = search_df['Rating'].tolist()
    result = []
    for i in range(len(canteen)):
        result.append([canteen[i],stall[i],food[i],menu[i],price[i],ratings[i]])
    return result
    
 #example search
 result= searchfood(['Chinese Cuisine','Korean Cuisine'],[2.0,3.6],2,'noodle')
 print(result)
