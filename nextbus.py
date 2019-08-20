# v.0.2 Get JSON data from the Metro API

# Libraries
import json
import urllib3

# Append to URL to force JSON response format
DOTJSON = "?format=json"

# API -> JSON returns 'raw_data' as a list of dictionaries
#    [{'Text': 'University of Minnesota', 'Value': '1'}, {'Text': 'Airport (MAC)', 'Value': '2'}, ...]
# Filter 'raw_data' into a list of all 'Text' items
def DictToList(listOfDicts):
    newList = []
    for dict in listOfDicts:
        newList.append(dict['Text'])
    return newList

# Program Execution, keep at end of file
def Main():
    http = urllib3.PoolManager()
    response = http.request('GET', "http://svc.metrotransit.org/nextrip/providers" + DOTJSON)
    raw_data = json.loads(response.data.decode('utf-8'))
    formatted_data = DictToList(raw_data)
    print(formatted_data)

    return 0

if __name__ == "__main__":
    Main();
