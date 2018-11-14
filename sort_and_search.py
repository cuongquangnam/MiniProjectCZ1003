import pandas as pd
import numpy as np
from pandas import DataFrame
import openpyxl
from direction import *
import datetime

df = pd.read_excel('canteen_db.xlsx')
infocan = pd.read_excel('canteen details.xlsx')
admin_data = pd.read_excel("Admin.xlsx")

infocan = infocan.set_index('Canteen')

#takes in foodtype = ['Food1','food2' etc], pricerange = [lower, higher as floats/int], the search term
# rating = int(1 to 5) or 0 if not specified
def searchfood(foodtype, pricerange, rating, search, df):
    #copy the dataframe to temporary.
    search_df = df
    #filter by foodtype
    if foodtype != []:
        foodcond = search_df['Food Type'].isin(foodtype)
        search_df = search_df[foodcond]
    # filter by price range
    search_df = searchPrice(pricerange[0], pricerange[1], search_df)
    # filter by rating, shows all above specified rating
    ratingcond = search_df['Rating'] >= rating
    if rating != 0:
        search_df = search_df[ ratingcond ]
    # filter by menu Item
    if search != ' ':
        lst = search.lower().split()
        for word in lst:
            wordcond = search_df['Menu Item'].str.lower().str.contains(word)
            search_df = search_df[wordcond]
    # return the filtered DataFrame
    return search_df
#function to sort by rating given the DataFrame filtered, the output is a list of indexes
def sort_by_rating(filter_df):
    return filter_df.sort_values("Rating")
#function to sort by price given the DataFrame filtered, the output is a list of indexes
def sort_by_price(filter_df):
    return filter_df
#function to sort by distance based on the user location, the filtered DataFrame and the DataFrame containing
#information about the canteen
def sort_by_location(user_loc, filter_df, infocan):
    search_df = filter_df.set_index('Canteen')
    lst_loc = search_df.index.unique()
    lst_dist = {}
    frames = []
    for loc in lst_loc:
        #calculate the distance
        distance = ((user_loc[0] - infocan.loc[loc]['loc x'])**2 + (user_loc[1] - infocan.loc[loc]['loc y'])**2)**(1/2)
        #convert from bitmap to km (just giving an approximate of the distance)
        distance *= 0.0025
        #create a new column in DataFrame to store all of the distances
        filter_df.at[loc,'Distance'] = distance
    # select top 10 location to show the user
    count = 1
    for loc in search_df.index.unique():
        a = search_df.loc[loc]
        if len(a.shape) == 1:
            b = pd.DataFrame(a).T
            frames.append(b)
        else:
            frames.append(a)
        if count == 10:
            break
        count += 1
    if frames !=[]:
        #concatenate all the DataFrames selected
        return pd.concat(frames)
    else:
        return pd.DataFrame()

def display10(filter_df):
    try:
        display_df = filter_df.set_index('Canteen')
    except:
        display_df = filter_df
    canteen_list_10 = display_df.index.unique()[:10]
    return display_df.loc[canteen_list_10,:]

def get_location(filter_df):
    df = filter_df
    if type(filter_df) == np.float64:
        return [df]
    else:
        return df

def binarySearch(filter_lst, target, low, high, up):
    if high - 1 == low:
        return low
    mid = (low + high)//2
    if target >= filter_lst[mid] and target <= filter_lst[mid + 1]:
        if up == False:
            if target == filter_lst[mid]:
                a = mid
                while (target == filter_lst[a]) and (a >= low):
                    a -= 1
                return a+1
            return mid + 1
        else:
            if target == filter_lst[mid + 1]:
                a = mid + 1
                while (target == filter_lst[a]) and (a <= high):
                    a += 1
                return a-1
            return mid
    elif target < filter_lst[mid]:
        return binarySearch(filter_lst, target, low, mid, up)
    else:
        return binarySearch(filter_lst, target, mid, high, up)

def searchPrice(low_price, high_price, filter_df):
    if (low_price > high_price):
        return pd.DataFrame()
    else:
        price_lst = filter_df['Price'].tolist()
        length = len(price_lst)
        if low_price > price_lst[length - 1] or high_price < price_lst[0]:
            return pd.DataFrame()
        else:
            if length < 3:
                return filter_df
            else:
                if low_price <= price_lst[0]:
                    low = 0
                else:
                    low = binarySearch(price_lst, low_price, 0,  length - 1, False)
                if high_price >= price_lst[length - 1]:
                    high = length - 1
                else:
                    high = binarySearch(price_lst, high_price, low, length - 1, True)
                return filter_df.iloc[low: high + 1]


#t = sort_by_location((441,430), result, infocan)
#print(result.iloc[3:10])
#print(df.iloc[0])

# print(type(t1[3]))
#convert from pixel to latitudes and longitudes
#result = searchfood([],[0.0,100.0],0,'pork', df)

#t = sort_by_location((333,222), result, infocan)
#print(display10(t))
#t = sort_by_price(result)
#u = sort_by_rating(result)
# print(result.loc["Canteen 9", "Stall"])
