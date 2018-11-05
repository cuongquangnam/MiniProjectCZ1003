from canteen_database import *
import math
# this create a short version of the database for using
# function to print data of all stalls within price range
# and returns list of stalls in price range in the format
# [[canteen, stallname],[canteen2, stallname2]]
def search_by_price(pricerange,filter_db,db):
  stalls_by_price=[]
  for canteen in filter_db:
      for stall in filter_db[canteen]:
          if db[canteen]['Stalls'][stall][2] in range(pricerange[0],1+pricerange[1]):
              stalls_by_price.append((canteen,stall))
  return stalls_by_price
#function to filter by rating
def filter_by_rating(filter_rating,filter_db,db):
    for canteen in filter_db:
        for stall in filter_db[canteen]:
            if db[canteen]["Stalls"][stall][0] < filter_rating:
                 filter_db.remove((canteen,stall))
    return filter_db
# function to search only filtered stalls,
# input filter_db must be [canteen:stall_name]
# returns food filtered by foodtype
def search_by_food(foodname,filter_db,db):
  food_filtered=[]
  for canteen in filter_db:
      for stall in filter_db[canteen]:
         if db[canteen]['Stalls'][stall][1] in foodname:
             food_filtered.append((canteen,stall))
  return food_filtered
#function to sort by price from list with [canteen,stall_name]
def sort_by_price(filter_db,db):
    stalls_price_db = {}
    for canteen, stall in filter_db:
        stalls_price_db[(canteen,stall)] = db[canteen]['Stalls'][stall][2]
    sorted_list_by_price=[k for k in sorted(stalls_price_db, key= stalls_price_db.get,reverse=False)]
    return sort_by_price_filtered
# function to sort by rating from list with [canteen:stall_name]
def sort_by_rating(filter_db,db):
  stalls_rating_db={}
  for canteen , stall in filter_db:
    rating=db[canteen]['Stalls'][stall][0]
    stalls_rating_db[(canteen,stall)]=db[canteen]['Stalls'][stall][0]
  sorted_list_by_rating=[k for k in sorted(stalls_rating_db, key=stalls_rating_db.get, reverse=True)]
  # sorted will sort the dict based on the key, key=dict.get retrieves the values from each key, reverse=True will be descending.
  return sort_by_rating_filtered
#function to sort by distance from list with [canteen,stall_name]
def sort_distance(filter_db, user_distance,db):
    stalls_distance_db = {}
    for canteen, stall in filter_db:
        stalls_distance_db[(canteen,stall)] = math.sqrt((db[canteen]['Location'][0] - user_distance[0])**2 + (db[canteen]['Location'][1] - user_distance[1])**2)
    sorted_list_by_distance=[k for k in sorted(stalls_distance_db, key= stalls_distance_db.get, reverse=False)]
    return sorted_list_by_distance
##################################
########
######################################
#######
#foodname=foodtype_input()
#searchprice = pricerange_input()
#filtered_list=search_by_price(searchprice,filtered_list,canteen_db)
#filtered_list=search_by_food(foodname,filtered_list,canteen_db)
# sort_by_rating(filtered_list,canteen_db)
#fastfood, cake, drink,
