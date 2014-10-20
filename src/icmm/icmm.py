import datetime
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

def get_def_icc_category_id(apiurl, domain):
    params = {'filter' : 'key:icc_data'}
    headers = {'content-type': 'application/json'}
    response = requests.get(
        "{}/{}.{}".format(apiurl, domain, 'categories'), 
        params = params, 
        headers = headers
        )
        
    if response.status_code != 200:
        return None
    
    collection = response.json()['$collection']
    
    return extract_first_id(collection)
    
def get_def_icc_datadescriptor_id(apiurl, domain):
    params = {'filter' : 'name:ICC Data Vector descriptor'}
    headers = {'content-type': 'application/json'}
    response = requests.get(
        "{}/{}.{}".format(apiurl, domain, 'datadescriptors'), 
        params = params, 
        headers = headers
        )
        
    if response.status_code != 200:
        return None
    
    collection = response.json()['$collection']
    
    return extract_first_id(collection)
    
def extract_first_id(collection):
    if len(collection) == 0:
        return None
    else:
        ref = collection[0]['$ref']
        
        return re.search ("/([0-9]+)$", ref).group(1)
    
def create_icc_dataitem(name, description, icc_data, helper, ddId = None, catId = None):
    dataitem = {}
    dataitem['id'] = helper.get_next_id('dataitems')
    dataitem['$self'] = helper.create_ref('dataitems', dataitem['id'])
    dataitem['name'] = name
    dataitem['description'] = description
    dataitem['lastmodified'] = datetime.datetime.isoformat(datetime.datetime.now())
    dataitem['actualaccessinfocontenttype'] = 'application/json'
    dataitem['actualaccessinfo'] = json.dumps(icc_data)
    
    dataitem['datadescriptor'] = {}
    dataitem['categories'] = {}
    
    id = catId
    if id is None:
        id = helper.get_def_icc_category_id()
        if id is None:
            raise NoDefaultEntryException('cannot find id of ICC dataitem default category')
    dataitem['categories']['$ref'] = '/CRISMA.categories/' + str(id)
    
    id = ddId
    if id is None:
        id = helper.get_def_icc_datadescriptor_id()
        if id is None:
            raise NoDefaultEntryException('cannot find id of ICC dataitem default datadescriptor')
        
    dataitem['datadescriptor']['$ref'] = '/CRISMA.datadescriptors/' + str(id);
    
    return dataitem

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
    
    def create_icc_dataitem(self, name, description, icc_data, ddId = None, catId = None):
        return create_icc_dataitem(name, description, icc_data, self, ddId, catId)
    
    def get_def_icc_category_id(self):
        return get_def_icc_category_id(self._apiurl, self._domain)
        
    def get_def_icc_datadescriptor_id(self):
        return get_def_icc_datadescriptor_id(self._apiurl, self._domain)

class NoDefaultEntryException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
