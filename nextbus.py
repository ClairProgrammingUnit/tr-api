# v.0.1 Send requests to the Metro API

# Libraries
import json
import urllib3

# Append to URL to force JSON response format
DOTJSON = "?format=json"

def main():
    http = urllib3.PoolManager()
    response = http.request('GET', "http://svc.metrotransit.org/nextrip/providers" + DOTJSON)
    print(response.status)

if __name__ == "__main__":
    main();
