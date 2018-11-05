import pandas as pd
from pandas import DataFrame

df = pd.read_excel('canteen_db.xlsx')
df['Menu Item'] = df['Menu Item'].str.lower() #convert menu item column to lowercase for search
#takes in foodtype = ['Food1','food2' etc], pricerange = [lower, higher as floats/int], rating = int(1 to 5) or 0 if not specified
def searchfood(foodtype, pricerange, rating, search):
    #copy the dataframe to temporary.
    search_df = df.copy()
    #filter by foodtype
    if foodtype != []:
        foodcond = search_df['Food Type'].isin(foodtype)
        search_df = search_df[foodcond]
    # filter by price range
    if pricerange != []:
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
    # Transform results to List
    return search_df.index.values.tolist()
#function to take the second value of a list
def takeSecond(i):
    return i[1]
#function to sort by rating given the list of index searched, the output is a list of indexes
def sort_by_rating(lst_index):
    #create a list of [index, Rating of the food on index]
    rate = [[i, df.loc[i]['Rating']] for i in lst_index]
    #sort list [index , Rating] with the key being Rating
    lst_inded_rating_sorted = sorted(rate, key = takeSecond, reverse = True)
    lst_rating_sorted = []
    for i in lst_index_rating_sorted:
        lst_rating_sorted.append(i[0])
    return lst_rating_sorted
#function to sort by price given the list of index searched, the output is a list of indexes
def sort_by_price(lst_index):
    #create a list of [index, Price of the food of index]
    rate = [[i, df.loc[i]['Price']] for i in lst_index]
    #sort list [index , Price] with the key being Price
    lst_index_rating_sorted = sorted(rate, key = takeSecond)
    lst_rating_sorted = []
    for i in lst_index_rating_sorted:
        lst_rating_sorted.append(i[0])
    return lst_rating_sorted
#reduce the list to only ten
def reduce_list(lst_index):
    return lst_index[0:9]
#testing the functions
result = searchfood(['Chinese Cuisine','Korean Cuisine'],[2.0,4.0],2,'noodle')
result = sort_by_price(result)
result = reduce_list(result)
#from index --> DataFrame
print(DataFrame(df, index = result))
