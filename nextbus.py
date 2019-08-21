# v.0.3 Find the directions available for a given route

# Libraries
import json
import sys
import urllib3

# Append to URL to force JSON response format
DOTJSON = "?format=json"

# API -> JSON returns 'raw_data' as a list of dictionaries
#    [{'Text': 'University of Minnesota', 'Value': '1'}, {'Text': 'Airport (MAC)', 'Value': '2'}, ...]
# Filter 'raw_data' into a single dictionary
#    {'University of Minnesota':'1', 'Airport (MAC)':'2', ...}
def DictToList(listOfDicts, text, id):
    newDict = {}
    for dict in listOfDicts:
        newDict[dict[text]] = dict[id]
    return newDict

# Program Execution, keep at end of file
def Main():
    # Setup program info
    args = sys.argv[1:]
    http = urllib3.PoolManager()

    # Get routes
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/Routes" + DOTJSON)
    raw_data = json.loads(response.data.decode('utf-8'))
    route_dict = DictToList(raw_data, 'Description', 'Route')
    chosen_route = route_dict[args[0]]

    # Get directions
    response = http.request('GET', "http://svc.metrotransit.org/NexTrip/Directions/" + chosen_route + DOTJSON)
    raw_data = json.loads(response.data.decode('utf-8'))
    direction_dict = DictToList(raw_data, 'Text', 'Value')
    print(direction_dict)

    return 0

if __name__ == "__main__":
    Main();
