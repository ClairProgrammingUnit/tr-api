# v.0.5 Gets the next departure time for a given stop, route, and direction

# Libraries
import json
import sys
import time
import urllib3

# Constants
TWENTY_FOUR_HOURS = 60*24*24
DOTJSON = "?format=json"
FIRST_USER_ARG = 1

ROUTE = 0
STOP = 1
DIRECTION = 2

# Filter 'raw_data' into a simple single dictionary
def DictToList(listOfDicts, text, id):
    newDict = {}
    for dict in listOfDicts:
        newDict[dict[text]] = dict[id]
    return newDict

# Remove extra characters from JSON date format
def ConvertTimeStamps(timeDict):
    newDict = {}
    for timeStamp in timeDict:
        newDict[timeStamp] = int(timeDict[timeStamp][6:16])
    return newDict

# UI specs and API assume different input formats. Convert UI to match API
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

def GetNextDeparture(departures):
    current_time = time.time()
    next_departure = ""
    next_departure_time = current_time + TWENTY_FOUR_HOURS

    for departure_time in departures:
        if current_time < departures[departure_time] and departures[departure_time] < next_departure_time:
            next_departure = departure_time
            next_departure_time = departures[departure_time]
        else:
            continue
    return next_departure

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
    departure_dict_raw = DictToList(raw_data, 'DepartureText', 'DepartureTime')
    departure_dict = ConvertTimeStamps(departure_dict_raw)

    # Get next departure time for given stop
    next_departure = GetNextDeparture(departure_dict)
    print(next_departure)

    return 0

if __name__ == "__main__":
    Main();
