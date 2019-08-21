# v.1.0 Gets the time until the next departure from a stop with a given route and direction

# Libraries
import json
import sys
import time
import urllib3

# Constants
TWENTY_FOUR_HOURS = 60*24*24
DOT_JSON = "?format=json"
FIRST_USER_ARG = 1

ROUTE = 0
STOP = 1
DIRECTION = 2

# Filter 'raw_data' into a simple single dictionary
def DictToList(list_of_dicts, text, id):
    new_dict = {}
    for dict in list_of_dicts:
        new_dict[dict[text]] = dict[id]
    return new_dict

# Remove extra characters from JSON date format
def Converttimestamps(time_dict):
    new_dict = {}
    for timestamp in time_dict:
        new_dict[timestamp] = int(time_dict[timestamp][6:16])
    return new_dict

# UI specs and API assume different input formats. Convert UI to match API
def FormatDirArg(arg):
    new_arg = ""
    if arg == "north":
        new_arg = "NORTHBOUND"
    elif arg == "east":
        new_arg = "EASTBOUND"
    elif arg == "south":
        new_arg = "SOUTHBOUND"
    elif arg == "west":
        new_arg = "WESTBOUND"
    else:
        new_arg = "INVALID"
    return new_arg

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

def TimeUntilDeparture(departure_time):
    current_time = time.time()
    time_remaining = departure_time - current_time
    minutes_remaining = int(time_remaining / 60)
    return minutes_remaining

# Program Execution, keep at end of file
def Main():
    # Setup program info
    args = sys.argv[FIRST_USER_ARG:]
    http = urllib3.PoolManager()

    args[DIRECTION] = FormatDirArg(args[DIRECTION])

    # Get routes
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/Routes%s" % DOT_JSON)
    raw_data = json.loads(response.data.decode('utf-8'))
    route_dict = DictToList(raw_data, 'Description', 'Route')
    chosen_route = route_dict[args[ROUTE]]

    # Get directions
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/Directions/%s%s" % (chosen_route, DOT_JSON))
    raw_data = json.loads(response.data.decode('utf-8'))
    direction_dict = DictToList(raw_data, 'Text', 'Value')
    chosen_direction = direction_dict[args[DIRECTION]]

    # Get stops
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/Stops/%s/%s%s" % (chosen_route, chosen_direction, DOT_JSON))
    raw_data = json.loads(response.data.decode('utf-8'))
    stop_dict = DictToList(raw_data, 'Text', 'Value')
    chosen_stop = stop_dict[args[STOP]]

    # Get departures for given stop
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/%s/%s/%s%s" % (chosen_route, chosen_direction, chosen_stop, DOT_JSON))
    raw_data = json.loads(response.data.decode('utf-8'))
    departure_dict_raw = DictToList(raw_data, 'DepartureText', 'DepartureTime')
    departure_dict = Converttimestamps(departure_dict_raw)

    # Get next departure time and minutes until it for given stop
    next_departure = GetNextDeparture(departure_dict)
    print(next_departure)
    time_until_next_departure = TimeUntilDeparture(departure_dict[next_departure])
    print("%d minutes until next departure" % time_until_next_departure)

    return 0

if __name__ == "__main__":
    Main();
