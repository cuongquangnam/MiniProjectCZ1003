from canteen_database import canteen_db 

# list of all canteens and stalls
filtered_list=[('Food Court 1', 'Stall 101'), ('Food Court 1', 'Stall 102'), ('Food Court 1', 'Stall 103'), ('Food Court 1', 'Stall 104'), ('Food Court 1', 'Stall 105'), ('Food Court 1', 'Stall 106'), ('Food Court 1', 'Stall 107'), ('Food Court 1', 'Stall 108'), ('Food Court 1', 'Stall 109'), ('Food Court 2', 'Stall 201'), ('Food Court 2', 'Stall 202'), ('Food Court 2', 'Stall 203'), ('Food Court 2', 'Stall 204'), ('Food Court 2', 'Stall 205'), ('Food Court 2', 'Stall 206'), ('Food Court 2', 'Stall 207'), ('Food Court 2', 'Stall 208'), ('Food Court 2', 'Stall 209'), ('Food Court 2', 'Stall 210'), ('Food Court 9', 'Stall 901'), ('Food Court 9', 'Stall 902'), ('Food Court 9', 'Stall 903'), ('Food Court 9', 'Stall 904'), ('Food Court 9', 'Stall 905'), ('Food Court 9', 'Stall 906'), ('Food Court 9', 'Stall 907'), ('Food Court 9', 'Stall 908'), ('Food Court 9', 'Stall 909'), ('Food Court 11', 'Stall 1101'), ('Food Court 11', 'Stall 1102'), ('Food Court 11', 'Stall 1103'), ('Food Court 11', 'Stall 1104'), ('Food Court 11', 'Stall 1105'), ('Food Court 11', 'Stall 1106'), ('Food Court 13', 'Stall 1301'), ('Food Court 13', 'Stall 1302'), ('Food Court 13', 'Stall 1303'), ('Food Court 13', 'Stall 1304'), ('Food Court 13', 'Stall 1305'), ('Food Court 13', 'Stall 1306'), ('Food Court 13', 'Stall 1307'), ('Food Court 13', 'Stall 1308'), ('Food Court 14', 'Stall 1401'), ('Food Court 14', 'Stall 1402'), ('Food Court 14', 'Stall 1403'), ('Food Court 14', 'Stall 1404'), ('Food Court 14', 'Stall 1405'), ('Food Court 14', 'Stall 1406'), ('Food Court 16', 'Stall 1601'), ('Food Court 16', 'Stall 1602'), ('Food Court 16', 'Stall 1603'), ('Food Court 16', 'Stall 1604'), ('Food Court 16', 'Stall 1605'), ('Foodgle Food Court', 'Foodgle 1'), ('Foodgle Food Court', 'Foodgle 2'), ('Foodgle Food Court', 'Foodgle 3'), ('Foodgle Food Court', 'Foodgle 4'), ('Foodgle Food Court', 'Foodgle 5'), ('Foodgle Food Court', 'Foodgle 6'), ('Foodgle Food Court', 'Foodgle 7'), ('Foodgle Food Court', 'Foodgle 8'), ('Foodgle Food Court', 'Foodgle 9'), ('North Hill Food Court', 'NH 1'), ('North Hill Food Court', 'NH 2'), ('North Hill Food Court', 'NH 3'), ('North Hill Food Court', 'NH 4'), ('North Hill Food Court', 'NH 5'), ('North Hill Food Court', 'NH 6'), ('North Hill Food Court', 'NH 7'), ('North Hill Food Court', 'NH 8'), ('Pioneer Food Court', 'Pioneer 1'), ('Pioneer Food Court', 'Pioneer 2'), ('Pioneer Food Court', 'Pioneer 3'), ('Pioneer Food Court', 'Pioneer 4'), ('Pioneer Food Court', 'Pioneer 5'), ('Pioneer Food Court', 'Pioneer 6'), ('Pioneer Food Court', 'Pioneer 7'), ('Pioneer Food Court', 'Pioneer 8'), ('Pioneer Food Court', 'Pioneer 9'), ('Pioneer Food Court', 'Pioneer 10'), ('Pioneer Food Court', 'Pioneer 11'), ('Pioneer Food Court', 'Pioneer 12')]
# various options of food types
foodtype=('Halal','Vegetarian','Indian','Vietnamese','Western','Chinese','Indian Vegetarian','Japanese','Korean')

# function that asks user for input of food type
# user input int value of 0 to 9
# returns string of the corresponding food type
def foodtype_input():
  # lists of food types for displaying in a neat 3 x 3 table
  foodtype_print=[['1 - Halal','2 - Vegetarian','3 - Indian'],['4 - Vietnamese','5 - Western','6 - Chinese'],['7 - Indian Vegetarian','8 - Japanese','9 - Korean'],['0 - All Food']]
  col_width = max(len(word) for row in foodtype_print for word in row) + 2  # padding
  print("What kinds of food do you want to eat? Enter [Foodtype1] [Foodtype2] etc")
  #print food options in 3 column table
  #ljust = left justified for the amount of characters col_width
  # str.join(seq) will join sequence of strings together with str
  for row in foodtype_print:
    print ("".join(word.ljust(col_width) for word in row)) 
  #loop to only accept integer values between 0 and 9, else print error message
  food_choice=[]
  while True:
    food_input_str=input("My choice:")
    print('')
    try: 
      food_input_int=list(map(int,food_input_str.rstrip().split()))
      if 0 not in food_input_int and len(food_input_int)>=1:
        food_choice = [foodtype[c-1] for c in food_input_int if c in range(1,10)]
        break
        # if user selects all food, add 
      elif food_input_int[0]==0 and len(food_input_int)==1:
        print("Showing selections for all food")
        print('')
        return foodtype
      else: 
        print("Invalid input \n")
    except:
      print("Invalid input \n")
  print('Showing selections for ', end='')
  print(', '.join(food for food in food_choice), end='')
  print(' food \n')
  return food_choice
    
# function that asks user for input of price range, 
# accepts min and max amount as integers separated by space
# returns [min,max]        
def pricerange_input():
  print("Please input your budget ($) \n       [min amount] [max amount]")
  while True:
    price_range_str=input("My budget is:" )
    print('')
    try: 
      price_range=list(map(int,price_range_str.rstrip().split()))
      # map(function,iterable) applies function to each iterable
      # rstrip strips whitespace from end of the string
      # split turns string into list, separated by space 
      if price_range[0]>price_range[1]:
        print("Invalid input")
      else:
        return price_range #output return as [min pice,max price]
    except: 
      print("Invalid input")

# function to print all info of stalls given the canteen and stall name as input
def print_stall_data(db,canteen,stallname):
  stall_rating=db[canteen]['Stalls'][stallname][0]
  stall_price=db[canteen]['Stalls'][stallname][2]  
  stall_foodtype=db[canteen]['Stalls'][stallname][1]
  print(canteen)
  print(' Stall Name:',stallname)
  print(' Food:',stall_foodtype)
  print(' Rating:',stall_rating)
  print(' Price:',stall_price)
  print("")

# function to print data of all stalls within price range
# and returns list of stalls in price range in the format
# [[canteen, stallname],[canteen2, stallname2]]
def search_by_price(pricerange,filter_db,db):
  stalls_by_price=[]  
  print("You searched for price between",pricerange[0],'and',pricerange[1],'dollars.\n')
  have_result=False
  for canteen, stall in filter_db:
    if db[canteen]['Stalls'][stall][2] in range(pricerange[0],1+pricerange[1]):
      print_stall_data(db,canteen,stall)
      stalls_by_price.append((canteen,stall))
      have_result=True
  if not have_result:
    print("No results found.")
    return []
  return stalls_by_price


# function to search only filtered stalls, 
# input filter_db must be [canteen:stall_name]
# returns food filtered by foodtype
def search_by_food(foodname,filter_db,db):
  food_filtered=[]
  if filter_db==[]:
    print("No results found.")
  for canteen , stall in filter_db:
    if db[canteen]['Stalls'][stall][1] in foodname:
      print_stall_data(db,canteen,stall)
      food_filtered.append((canteen,stall))
  return food_filtered

# function to sort by rating from list with [canteen:stall_name]
def sort_by_rating(filter_db,db):
  if filter_db==[]:
    print('No results found.')
  stalls_rating_db={}
  print("Showing results with highest rating first\n")
  for canteen , stall in filter_db:
    stalls_rating_db[stall]=db[canteen]['Stalls'][stall][0]
  sorted_list_by_rating=[(k, stalls_rating_db[k]) for k in sorted(stalls_rating_db, key=stalls_rating_db.get, reverse=True)]
  # sorted will sort the dict based on the key, key=dict.get retrieves the values from each key, reverse=True will be descending.
  for stalls,rating in sorted_list_by_rating:
    for canteen_name in db.keys():
      for stall_name in db[canteen_name]['Stalls'].keys():
        if stall_name==stalls:
          print_stall_data(db,canteen_name,stall_name)    

##################################
######## TO DO 
# function to filter by rating
# function to sort by price


#foodname=foodtype_input()
# searchprice = pricerange_input()
# filtered_list=search_by_price(searchprice,filtered_list,canteen_db)
# filtered_list=search_by_food(foodname,filtered_list,canteen_db)
# sort_by_rating(filtered_list,canteen_db)
