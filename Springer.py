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

def search_springer(query, headers, _pages,records, _title, _keyword, _abstract,spr_api, _search_yr,data):
    print('Searching in Springer...')

    if (not _search_yr):
        count = 0
        for i in tqdm(range(1)):

            for i in range(_pages):

                url = 'http://api.springernature.com/meta/v2/json?q=' + query + '&s=' + str(i) + '&p=10&api_Key=' + spr_api
                # http://api.springernature.com/meta/v2/json?q=python&api_key=9771722066583fa9990238afde4495f1

                # response object
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'lxml')
                obj = json.loads(soup.text)

                # set the counter for records count

                ######## Find required attributes in the response object
                for item in obj['records']:

                    if 'issn' in obj['records']:
                        issn = item['issn']
                    elif 'isbn' in obj['records']:
                        issn = item['isbn']
                    else:
                        issn = str(['No Information found'])

                        try:
                            resp_obj = {"entities": {"Search Engine": "Springer Search Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, Publication Name, ISSN, Type, Published date, Abstract",
                                                     "items": [
                                                         {"DOI": item['identifier'],
                                                          "Title": item['title'],
                                                          "URLs": item['url'][0]['value'],
                                                          "Authors": item['creators'][0]['creator'],
                                                          "Publication Name": item['publicationName'],
                                                          "ISSN": issn,
                                                          "Cited count": str(['No Information found']),
                                                          "Affiliation": str(['No information found']),
                                                          "Type": item['contentType'],
                                                          "Published date": item['onlineDate'],
                                                          "Abstract": item['abstract']
                                                          }
                                                     ]}}
                            count += 1
                            # append dict object data
                            data.append(resp_obj)
                        except Exception as e:  # raise e
                            pass  # print('error:', e)

        time.sleep(1)

        print(f'Finished with total {count} records returned.')
        return data
    else:
        print("Date parameter either not suppoted or not available in Springer API!")
        return
