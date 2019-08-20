# v.0.1 Send requests to the Metro API
import urllib3

def main():
    http = urllib3.PoolManager()
    response = http.request('GET', "http://svc.metrotransit.org/")
    print(response.status)

if __name__ == "__main__":
    main();
