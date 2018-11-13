
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key= 'AIzaSyD7UsgHTKortN9wRHK13_OFtiX9VRWf2ss')
now = datetime(2018, 11, 14, 13, 00)
#convert from pixel on the NTU Campus map to latitudes and longitudes
def pixeltolatlng(x,y):
    lat = 1.356116549 - 0.000026134*y
    lng = 103.676118654 + 0.000015694*x
    return (lat,lng)

#get direction from address 1 to address 2 use certain mode of transport
def get_distance_and_duration(address1, address2, mode):
    distance_matrix = gmaps.distance_matrix(address1, address2, mode)
    elements = distance_matrix['rows'][0]['elements']
    if elements[0]['status'] != 'ZERO_RESULTS':
        #get distance
        distance = elements[0]['distance']['value'] #in meters
        #get duration
        duration = elements[0]['duration']['value'] #in second
        return [distance,duration]
    else:
        return[]


#NOTE: THERE ARE THREE MODES: 'walking', 'driving', 'transit' (transit means the combination of walking and using buses)
#get the directions from google map
def get_directions(address1, geocode2, mode):
    directions_result = gmaps.directions(address1,\
    address2, mode = mode, departure_time = now)
    return directions_result

#print the directions to the user (not transit) (meaning not using bus)
def print_directions_not_transit(directions):
    steps =  directions[0]['legs'][0]['steps']
    for step in steps:
        #print the instruction
        print(step['html_instructions'].replace('</b>','').replace('<b>','').\
          replace('</div>','').replace('<div style="font-size:0.9em">','. '))
        #print the duration of the instructions
        print(step['duration']['value']//60 ,'minutes ', step['duration']['value']%60,'seconds')
        #print the distance of the instructions
        print(step['distance']['text'])

#print out the directions to the user (transit) (meaning maybe using bus (or not))
def print_directions_transit(directions):
    #in case there is no directions, but actually there are always directions!!!
    if directions != []:
        steps = directions[0]['legs'][0]['steps']
        for step in steps:
            if step['travel_mode'] == 'TRANSIT':
                details = step['transit_details']
                print('Take ', details['line']['agencies'][0]['name'],' from',\
                      details['departure_stop']['name'],' to', details['arrival_stop']['name'])
            else:
                #just cleaning the data from google maps html
                print(step['html_instructions'].replace('</b>','').replace('<b>','').\
                      replace('</div>','').replace('<div style="font-size:0.9em">','. '))
            #print the duration of the instructions
            print(step['duration']['value']//60 ,'minutes ', step['duration']['value']%60,'seconds')
            #print the distance of the instructions
            print(step['distance']['text'])
x = float(input('x?: '))
y = float(input('y?: '))
geocode1 = pixeltolatlng(x,y)
#print(geocode1)
#directions = get_directions(geocode1,'North Spine Food Court Nanyang Technological University','transit')
#print_distance_and_duration(geocode1,'Da Nang Vietnam','transit')
#print(directions)
#print_directions_transit(directions)
#print_duration_and_time(directions)
