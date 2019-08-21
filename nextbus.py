# v.0.4 Get list of departure times for a given stop, route, and direction

# Libraries
import json
import sys
import urllib3

# Constants
DOTJSON = "?format=json"
FIRST_USER_ARG = 1
ROUTE = 0
STOP = 1
DIRECTION = 2

# API -> JSON returns 'raw_data' as a list of dictionaries
#    [{'Text': 'University of Minnesota', 'Value': '1'}, {'Text': 'Airport (MAC)', 'Value': '2'}, ...]
# Filter 'raw_data' into a single dictionary
#    {'University of Minnesota':'1', 'Airport (MAC)':'2', ...}
def DictToList(listOfDicts, text, id):
    newDict = {}
    for dict in listOfDicts:
        newDict[dict[text]] = dict[id]
    return newDict

def FormatDirArg(arg):
    newArg = ""
    if arg == "north":
        newArg = "NORTHBOUND"
    elif arg == "east":
        newArg = "EASTBOUND"
    elif arg == "south":
        newArg = "SOUTHBOUND"
    elif arg == "west":
        newArg = "WESTBOUND"
    else:
        newArg = "INVALID"
    return newArg

# Program Execution, keep at end of file
def Main():
    # Setup program info
    args = sys.argv[FIRST_USER_ARG:]
    http = urllib3.PoolManager()

    args[DIRECTION] = FormatDirArg(args[DIRECTION])

    # Get routes
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/Routes%s" % DOTJSON)
    raw_data = json.loads(response.data.decode('utf-8'))
    route_dict = DictToList(raw_data, 'Description', 'Route')
    chosen_route = route_dict[args[ROUTE]]

    # Get directions
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/Directions/%s%s" % (chosen_route, DOTJSON))
    raw_data = json.loads(response.data.decode('utf-8'))
    direction_dict = DictToList(raw_data, 'Text', 'Value')
    chosen_direction = direction_dict[args[DIRECTION]]

    # Get stops
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/Stops/%s/%s%s" % (chosen_route, chosen_direction, DOTJSON))
    raw_data = json.loads(response.data.decode('utf-8'))
    stop_dict = DictToList(raw_data, 'Text', 'Value')
    chosen_stop = stop_dict[args[STOP]]

    # Get departures for given stop
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/%s/%s/%s%s" % (chosen_route, chosen_direction, chosen_stop, DOTJSON))
    raw_data = json.loads(response.data.decode('utf-8'))
    departure_dict = DictToList(raw_data, 'DepartureText', 'DepartureTime')
    print(departure_dict)

    return 0

if __name__ == "__main__":
    Main();
