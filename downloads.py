import urllib.request
import datetime
import shutil
import atexit
import pickle
import os.path

_cache_file_name = "_cache.pkl"

if os.path.exists(_cache_file_name):
    with open(_cache_file_name, 'rb') as cache_file:
        _cache = pickle.load(cache_file)
else:
    _cache = {}

def _dump_cache():
    with open(_cache_file_name, 'wb') as cache_file:
        pickle.dump(_cache, cache_file)

atexit.register(_dump_cache)

_host_delays = {}
_host_times = {}

def no_cache_request(request, transformer=lambda x: x, host=None):
    if host in _host_delays:
        while datetime.datetime.now()-_host_delays[host] < _host_delays[host]:
            pass
        _host_times[host] = datetime.datetime.now()

    response = urllib.request.urlopen(request)
    if response.getcode() < 200 or response.getcode() > 299:
        print("HTTP Status " + response.getcode())
        return None
    response = transformer(response)
    return response

def cache_request(request, transformer=lambda x: x, host=None):
    if request in _cache:
        return _cache[request]
    response = no_cache_request(request, transformer, host)
    _cache[request] = response
    return response

def register_host(host, delay):
    _host_delays[host] = delay
    _host_times[host] = datetime.datetime.now()

def download(url, filename):
    webData = no_cache_request(url)
    with open(filename, 'wb') as out:
        shutil.copyfileobj(webData, out)
