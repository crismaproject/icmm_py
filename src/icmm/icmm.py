import json
import requests
import re

__author__="mscholl"
__date__ ="$14.03.2014 11:44:54$"

def get_worldstate(apiurl, domain, id):
    payload = {'deduplicate': 'true'}
    result = requests.get(
        '{}/{}.worldstates/{}'.format(apiurl, domain, id),
        params = payload
        )

    return result.json()

def put_worldstate(apiurl, domain, worldstate):
    result = requests.put(
        '{}/{}.worldstates/{}'.format(apiurl, domain, worldstate['id']),
        data = json.dumps(worldstate),                         
        headers = {'content-type':'application/json'}
        )
    
    return result

def get_next_id(apiurl, domain, entityinfo):
    params = {'limit' :  999999999}
    headers = {'content-type': 'application/json'}
    response = requests.get(
        "{}/{}.{}".format(apiurl, domain, entityinfo), 
        params = params, 
        headers = headers
        ) 

    if response.status_code != 200:
        return -1

    maxid = 0;
    collection = response.json()['$collection']
    for r in collection:
        ref = r['$ref']
        match = re.search ("/([0-9]+)$", ref)
        if (match):
            id = int (match.group(1))
            if (id > maxid):
                maxid = id
                
    return maxid + 1

def create_ref(domain, entityinfo, id):
    return '/{}.{}/{}'.format(domain, entityinfo, id)
    

class ICMMHelper:
    def __init__(self, apiurl, domain):
        self._apiurl = apiurl
        self._domain = domain
        
    def __str__(self):
        return repr('ICMMHelper: [apiurl=' + self._apiurl + '|domain=' + self._domain + ']')
    
    def create_ref(self, entityinfo, id):
        return create_ref(self._domain, entityinfo, id)
        
    def get_worldstate(self, id):
        return get_worldstate(self._apiurl, self._domain, id)
        
    def get_next_id(self, entityinfo):
        return get_next_id(self._apiurl, self._domain, entityinfo)
    
    def put_worldstate(self, worldstate):
        return put_worldstate(self._apiurl, self._domain, worldstate)  