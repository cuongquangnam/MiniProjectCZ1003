from math import sqrt
#function sort by location
def sort_by_location(lst_index,user_x,user_y):
    temp_df=df.iloc[lst_index]
    
    #collect unique list of canteens from results
    canteens=temp_df['Canteen'].unique().tolist()
    
    #formula for pythagaras
    fx = lambda x: (x - user_x)**2
    fy = lambda x: (x - user_y)**2
    
    #filter by canteens
    cond = canteen_df['Canteen'].isin(canteens)
    canteen_details = canteen_df[cond]
    
    #creating new columns for calculation
    canteen_details['fx'] = canteen_details['loc x'].apply(fx) 
    canteen_details['fy'] = canteen_details['loc y'].apply(fy)
    canteen_details['distance'] = canteen_details['fx'] + canteen_details['fy']
    canteen_details['distance'] = canteen_details['distance'].apply(sqrt)
    
    #create new column in df for sorting
    df['distance']=0
    for i in lst_index:
        canteen = df.iloc[i]['Canteen']
        canteen_filter = canteen_details['Canteen'] == canteen
        #fil in new column with distance calculated
        df.at[i,'distance'] = canteen_details['distance'][canteen_filter]
    
    #create a list of [index, distance of the food of the index]
    dist = [[i, df.iloc[i]['distance']] for i in lst_index]
    lst_index_distance_sorted = sorted(dist, key = takeSecond)
    lst_distance_sorted = []
    for i in lst_index_distance_sorted:
        lst_distance_sorted.append(i[0])
    return lst_distance_sorted
