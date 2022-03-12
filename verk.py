#!/usr/bin/env python
# coding: utf-8

# # Spørring mot verksregisteret
# 
# Oddrun Ohren 
# 
# Lars G Johnsen 

# ## Kode

# In[1]:


import json
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import dhlab.text as dh
import dhlab.api.dhlab_api as dhapi


########### Exported functions ################################

def urns_for_works(works_id):
    """Fra en verks-ID hent ut alle URNer
    param:
        works_id a work identifier - from """
    result = []
    try:
        graph = works(works_id)['@graph']
        res = [[url_to_urn(x['id']) for x in i['bibsys:url_to_content']] for i in graph if 'bibsys:url_to_content' in i]
        result = [x for y in res for x in y if x != '']
    except KeyboardInterrupt:
        return result
    except:
        pass
    return result

def find_works(forfatter="", tittel=""):
    """finn verk i registeret
    returner dem som pandas dataramme"""
    
    query_res = query_verksregister(forfatter, tittel)
    if query_res is None:
        return None
    soup = BeautifulSoup(query_res, features="lxml")
    n = soup.find("p")
    struct = json.loads(n.text)
    res = pd.DataFrame(struct['results'])
    return res

########### BASE FUNCTIONS #####################################

def query_verksregister(forfatter="", tittel="", page = 1):
    """spør mot verksregisteret 
    api for webgrensesnittet https://livedata.bibsys.no/verksregister/"""
    
    # sett opp query
    params = {
        "query" : f"(forfatter:{forfatter}) AND (tittel:{tittel})",
        "page": page
    }
    
    #utfør spørring
    res = requests.get("https://livedata.bibsys.no/works-registry-api/search/searchWorksbyTitleAndCreator", params = params)
    if res.status_code == 200:
        res = res.text
    else:
        res = None
    
    return res


def works(identifier):
    """Hent ut data om et verk fra identifikatoren"""
    
    res = requests.get(f"https://livedata.bibsys.no/works-registry-api/biblio/byWork/{identifier}")
    try:
        r = json.loads(res.text)
    except:
        r = {}
    return r

def url_to_urn(url):
    """Pell ut URN fra en URL"""

    a = re.findall("URN.*", url)
    if a != []:
        res = a[0]
    else:
        res = ''
    return res





