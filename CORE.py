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
import sys
from scraper_api import ScraperAPIClient
import logger

# ignore warning messages
import warnings
warnings.filterwarnings('ignore')
### setting output display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

_engine="CORE Engine"

def search_core(query, headers, _pages,records, _title, _keyword, _abstract,core_api,_search_yr,logging_flag, data):
        if _title:
            print('Searching in CORE...')
            url = 'https://core.ac.uk:443/api-v2/articles/search/%22' + query + '%22?page=1&pageSize=10&apiKey=' + core_api
            # response object
            response = requests.get(url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.content, 'lxml')

            # convert soup object into json
            obj = json.loads(soup.text)


            # set the counter for records count
            count = 0
            for i in tqdm(range(1)):

                if obj['data'] is not None:

                    ######## Find required attributes in the response object
                    for item in obj['data']:
                        try:
                            if 'publisher' not in obj:
                                publisher = ['No Information']
                            else:
                                publisher = item['publisher']

                            resp_obj = {"entities": {"Search Engine": "CORE Search Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, Publication Name,Type, Published Date",
                                                     "items": [{"DOI": item['oai'],
                                                                "Title": item['title'],
                                                                "URLs": item['downloadUrl'],
                                                                "Authors": item['authors'],
                                                                "Publication Name": publisher,
                                                                "ISSN": ['No Information'],
                                                                "Cited count": ['No Information'],
                                                                "Affiliation": ['No Information'],
                                                                "Type": ['Article'],
                                                                # "Keywords": item['topics'],
                                                                "Published Date": item['datePublished'],
                                                                "Abstract": ['No Information']
                                                                }]}}
                            count += 1
                            # append dict object data
                            data.append(resp_obj)
                        except Exception as e:  # raise e
                            pass
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            filename = exception_traceback.tb_frame.f_code.co_filename
                            line_number = exception_traceback.tb_lineno
                            logger.writeError(e, None, _engine, logging_flag, filename, line_number)
                else:
                    pass
                    # print('error core:', e)
            time.sleep(1)
            logger.writeRecords("Logging", None, _engine, count, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data

        if (not _search_yr):
            if _keyword or _abstract:
                print('Searching in CORE...')
                count = 0
                for i in tqdm(range(1)):
                    for i in range(_pages):
                        i += 1
                        url = 'https://core.ac.uk:443/api-v2/search/' + query + '?page=' + str(i) + '&pageSize=20&year='+ _search_yr +'&apiKey=' + core_api

                        # response object
                        response = requests.get(url, headers=headers, timeout=30)
                        soup = BeautifulSoup(response.content, 'lxml')

                        # convert soup object into json
                        obj = json.loads(soup.text)

                        # set the counter for records count

                        if obj['data'] is not None:

                            ######## Find required attributes in the response object
                            for item in obj['data']:
                                try:
                                    resp_obj = {"entities": {"Search Engine": "CORE Search Engine",
                                                             "Attributes found": "DOI, Title, URLs, Authors,Publication Name, IISN, Cited Count,Type, Published Date, Abstract",
                                                             "items": [{"DOI": item['_source']['doi'],
                                                                        "Title": item['_source']['title'],
                                                                        "URLs": item['_source']['urls'],
                                                                        "Authors": item['_source']['authors'],
                                                                        "Publication Name": item['_source']['publisher'],
                                                                        "ISSN": item['_source']['issn'],
                                                                        "Cited count": item['_source']['citationCount'],
                                                                        "Affiliation": ['No Information'],
                                                                        "Type": item['_type'],
                                                                        # "Keywords": item['topics'],
                                                                        "Published Date": str(item['_source']['datePublished']).split('T',1)[0],
                                                                        "Abstract": str(item['_source']['description']).replace('\n', '')
                                                                        }]}}
                                    count += 1
                                    # append dict object data
                                    data.append(resp_obj)
                                except Exception as e:  # raise e
                                    pass
                                    exception_type, exception_object, exception_traceback = sys.exc_info()
                                    filename = exception_traceback.tb_frame.f_code.co_filename
                                    line_number = exception_traceback.tb_lineno
                                    logger.writeError(e, None, _engine, logging_flag, filename, line_number)
                        else:
                            pass

                time.sleep(1)
                logger.writeRecords("Logging", None, _engine, count, count, logging_flag)
                print(f'Finished with total {count} records returned.')
                return data
        else:
         print('Searching in CORE...')
         print("Date Parameter not supported in this CORE API!")


