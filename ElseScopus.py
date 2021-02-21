import requests
import json
import urllib3
import urllib
from requests import get
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as n
import time
from time import sleep
from openpyxl import load_workbook
from tqdm import tqdm
import re
import os
from scraper_api import ScraperAPIClient

# ignore warning messages
import warnings
warnings.filterwarnings('ignore')
### setting output display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)


def search_scopus(query, headers, _pages, records, _title, _keyword, _abstract,scp_api,_from_yr,_to_yr_, data):
    query = processInputQuery(query)
    if _title:
        url = 'https://api.elsevier.com/content/search/scopus?query=%22' + query + '%22&apiKey=' + scp_api

        # response object
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'lxml')

        # convert resonse into josn
        obj = json.loads(soup.text)

        print('Searching in Elsevier Scopus...')
        # set the counter for records count
        count = 0
        for i in tqdm(range(1)):

            ######## Find required attributes in the response object
            for item in obj['search-results']['entry']:
                try:
                    if "prism:Issn" and "prism:issn" not in obj:
                        issn = item['prism:eIssn']
                    else:
                        issn = item['prism:issn']

                    resp_obj = {"entities": {"Search Engine": "Elsevier SCOPUS Search Engine",
                                             "Attributes found": "DOI, Title, URLs, Authors, Publication Name, ISSN, Cited count, Affiliation name, Type, Published date, Abstract",
                                             "items": [
                                                 {"DOI": item['prism:doi'],
                                                  "Title": item['dc:title'],
                                                  "URLs": item['prism:url'],
                                                  "Authors": item['dc:creator'],
                                                  "Publication Name": item['prism:publicationName'],
                                                  "ISSN": issn,
                                                  "Cited count": item['citedby-count'],
                                                  "Affiliation": item['affiliation'][0]['affilname'],
                                                  "Type": item['subtypeDescription'],
                                                  "Published date": item['prism:coverDate'],
                                                  "Abstract": item['prism:publicationName']
                                                  }
                                             ]}}
                    count += 1
                    # append dict object data
                    data.append(resp_obj)
                except Exception as e:  # raise e
                    pass
                    # print('error scopus:', e)
        time.sleep(1)

        print(f'Finished with total {count} records returned.')
        return data
    if (not _from_yr):
        if _keyword or _abstract:

            print('Searching in Elsevier Scopus...')
            count = 0
            for i in tqdm(range(1)):

                for i in range(_pages):

                    url = 'https://api.elsevier.com/content/search/scopus?query=' + query + '&apiKey=' + scp_api + '&start=' + str(i) + '&count=10'

                    # response object
                    response = requests.get(url, headers=headers, timeout=30)
                    soup = BeautifulSoup(response.content, 'lxml')

                    # convert resonse into josn
                    obj = json.loads(soup.text)

                    # set the counter for records count

                    ######## Find required attributes in the response object
                    for item in obj['search-results']['entry']:
                        try:
                            if "prism:eIssn" in item:
                                issn = item['prism:eIssn']
                            elif "prism:Issn" or "prism:issn" in item:
                                issn = item['prism:issn']
                            else:
                                issn = str(['No information found'])

                            resp_obj = {"entities": {"Search Engine": "Elsevier SCOPUS Search Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, Publication Name, ISSN, Cited count, Affiliation name, Type, Published date, Abstract",
                                                     "items": [
                                                         {"DOI": item['prism:doi'],
                                                          "Title": item['dc:title'],
                                                          "URLs": item['prism:url'],
                                                          "Authors": item['dc:creator'],
                                                          "Publication Name": item['prism:publicationName'],
                                                          "ISSN": issn,
                                                          "Cited count": item['citedby-count'],
                                                          "Affiliation": item['affiliation'][0]['affilname'],
                                                          "Type": item['subtypeDescription'],
                                                          "Published date": item['prism:coverDate'],
                                                          "Abstract": item['prism:publicationName']
                                                          }
                                                     ]}}
                            count += 1
                            # append dict object data
                            data.append(resp_obj)
                        except Exception as e:  # raise e
                            pass
                            print('error scopus:', e)
            time.sleep(1)

            print(f'Finished with total {count} records returned.')
            return data

    else:
        if _keyword or _abstract:

            print('Searching in Elsevier Scopus...')
            count = 0
            for i in tqdm(range(1)):

                for i in range(_pages):

                    url = 'https://api.elsevier.com/content/search/scopus?query=' + query + '&apiKey=' + scp_api + '&date=' + _from_yr+'-'+_to_yr_ +'&start=' + str(i) + '&count=10'

                    # response object
                    response = requests.get(url, headers=headers, timeout=30)
                    soup = BeautifulSoup(response.content, 'lxml')

                    # convert resonse into josn
                    obj = json.loads(soup.text)

                    # set the counter for records count

                    ######## Find required attributes in the response object
                    for item in obj['search-results']['entry']:
                        try:
                            if "prism:eIssn" in item:
                                issn = item['prism:eIssn']
                            elif "prism:Issn" or "prism:issn" in item:
                                issn = item['prism:issn']
                            else:
                                issn = str(['No information found'])

                            resp_obj = {"entities": {"Search Engine": "Elsevier SCOPUS Search Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, Publication Name, ISSN, Cited count, Affiliation name, Type, Published date, Abstract",
                                                     "items": [
                                                         {"DOI": item['prism:doi'],
                                                          "Title": item['dc:title'],
                                                          "URLs": item['prism:url'],
                                                          "Authors": item['dc:creator'],
                                                          "Publication Name": item['prism:publicationName'],
                                                          "ISSN": issn,
                                                          "Cited count": item['citedby-count'],
                                                          "Affiliation": item['affiliation'][0]['affilname'],
                                                          "Type": item['subtypeDescription'],
                                                          "Published date": item['prism:coverDate'],
                                                          "Abstract": item['prism:publicationName']
                                                          }
                                                     ]}}
                            count += 1
                            # append dict object data
                            data.append(resp_obj)
                        except Exception as e:  # raise e
                            pass
                            #print('error scopus:', e)
            time.sleep(1)

            print(f'Finished with total {count} records returned.')
            return data

def processInputQuery(_query):
    special_characters = "+"
    if any(c in special_characters for c in _query):
        new_query = str(_query).replace("+", "AND")
        return  new_query
