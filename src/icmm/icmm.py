import requests

__author__="mscholl"
__date__ ="$14.03.2014 11:44:54$"



_api='http://crisma.cismet.de/economic-impact/icmm_api/CRISMA.worldstates/'

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
        data = worldstate,                         
        headers = {'content-type':'application/json'}
        )
    
    return result.status_code

def get_next_id(apiurl, domain, entityinfo):
    params = {'limit' :  999999999}
    headers = {'content-type': 'application/json'}
    response = requests.get(
        "{}/{}.{}".format(apiurl, domain, entityinfo), 
        params=params, 
        headers=headers
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

class ICMMHelper():
    def __init__(self, apiurl, domain):
        self.apiurl = apiurl
        self.domain = domain
    def __str__(self):
        return repr('ICMMHelper: [' + self + ']')
    
    def get_worldstate(id):
        return icmm.get_worldstate(self.apiurl, self.domain, id)