import urllib.request
import datetime
import shutil
_cache = {}
_host_delays = {}
_host_times = {}

def cache_request(request, transformer=lambda x: x, host=None):
    if request in _cache:
        return _cache[request]
    if host in _host_delays:
        while datetime.datetime.now()-_host_delays[host] < _host_delays[host]:
            pass
        _host_times[host] = datetime.datetime.now()

    response = urllib.request.urlopen(request)
    if response.getcode() < 200 or response.getcode() > 299:
        print("HTTP Status " + response.getcode())
        return None
    response = transformer(response)
    _cache[request] = response
    return response

def register_host(host, delay):
    _host_delays[host] = delay
    _host_times[host] = datetime.datetime.now()

def download(url, filename):
    print('Downloading:',url)
    #TODO download image to file
    webData = cache_request(url)
    with open(filename, 'wb') as out:
        #TODO Converter should resize image to 488x680
        shutil.copyfileobj(webData, out)
