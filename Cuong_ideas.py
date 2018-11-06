import xlrd
import pandas as pd
from pandas import DataFrame
from operator import itemgetter
#loc = ("D:\Courses\CZ1003-Introduction to Computational Thinking\Project\Canteen %2F Restaurant List .xlsx")

#wb = xlrd.open_workbook(loc)
#sheet = wb.sheet_by_index(1)

#sheet.cell_value(0,0)
#print(sheet.cell_value(4,4)+3)
df = {}
types_of_food = ['Chinese', 'Vegetarian','Vietnamese']
location = ['Koufu @ Southspine','Northspine Foodcourt']
rating = ['Rating 1', 'Rating 2', 'Rating 3', 'Rating 4', 'Rating 5']
path = "D:\Courses\CZ1003-Introduction to Computational Thinking\Project\Database"
#for i in types_of_food:
#    df[i] = {}
#    for j in rating:
#        df[i][j] = {}
#        for k in location:
#            df[i][j][k] = pd.read_excel(path + '\\' + i +'\\' + j + '\\' + k+'.xlsx' )
def low_high(pricerange, lst, df):
                     for low in range (len(lst)):
                        if df[type][rank][loc]['Price'][low] >= pricerange[0]:
                           break
                     for high in range(len(lst),0):
                        if df[type][rank][loc]['Price'][high] <= pricerange[1]:
                           break
                     return(range(low,high+1))
def searchfood(foodtype, pricerange, rating, search, df):
    lst_rating = ['Rating ' + str(i) for i in range(1,6) if i >= rating]
    a=[]
    for type in foodtype:
        for rank in lst_rating:
             for loc in location:
                 df = pd.read_excel(path + '\\' + i +'\\' + j + '\\' + k+'.xlsx' )
                 x = low_high(pricerange, df['Price'])
                 for k in range(low, high +1):
                     if not(df[type][rank][loc]['Menu Item'][k].str.contains(search)):
                         x.remove(k)
                 #a[(type,rank,loc)] = DataFrame(df[type][rank][loc], index = range(low, high+1))
                 for index in x:
                     a.append([type, rank, loc,df[type][rank][loc].loc(index)])
    return a
def get_price(a):
    return a[3]['Price']
def sort_by_price(a):
    #[:n] --> get n smallest ones or n largest ones
    return sorted(a, key = get_price)[:10]
def get_rating(a):
    return a[3]['Rating']
def sort_by_rank(a):
    #[:n]--> get n smallest ones or n largest ones
    return sorted(a, key = get_rating, reverse = True)[:10]
