#!/usr/bin/env python
#
# Peter.Kutschera@ait.ac.at, 2014-03-13
# Time-stamp: "2014-03-13 11:42:28 kutscherap"
#
# ID-Generator fpr ICMM ids

import json
import requests
import re


def getId (clazz):
    baseUrl = 'http://crisma.cismet.de/pilotC/icmm_api'
    params = {
        'limit' :  999999999
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{}/{}.{}".format (baseUrl, "CRISMA", clazz), params=params, headers=headers) 
    # this was the request:
    # print response.url

    if response.status_code != 200:
        return "Error accessing ICMM at {}: {}".format (response.url, response.raise_for_status())

    # Depending on the requests-version json might be an field instead of on method
    # print response.json()

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


if __name__ == "__main__":
    for c in ["worldstates", "transitions", "dataitems"]:
        print "{}: {}".format (c, getId (c)) 
