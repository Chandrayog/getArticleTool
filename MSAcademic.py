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

_engine="Microsoft Academic"

def search_msAcademic(query, headers, _pages,records, _title, _keyword, _abstract,ms_api,_from_yr,_to_yr_, logging_flag, data):
    q = str(re.sub('["!,*)@#%(&$_?.^]', '', query.lower()))

    # title search
    if _title:
        url1 = 'https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=Ti=%27' + q + '%27&model=latest&count=10&offset=0&attributes=DOI,Ti,Y,BT,D,W,PB,CC,AA.AuN,AA.AuId,AA.DAfN,AA.AfN,S,AW&subscription-key=' + ms_api
        # response object
        response = requests.get(url1, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        obj = json.loads(soup.text)

        print('Searching in Microsoft Academic...')
        # set the counter for records count
        count = 0
        for i in tqdm(range(1)):

            ######## Find required attributes in the response object
            for item in obj['entities']:
                try:
                    # extract abstract keywords from the response as it doesnt have a spefcific abstract attribute
                    if bool(str(item['AW'])):
                        abs_str = str(item['AW'])
                        abs_new = abs_str.replace(',', '').replace("'", '')
                    else:
                        abs_new = str(['No information found'])

                    if bool(item['S'][0]['U']):
                        urls = item['S'][0]['U']
                    else:
                        urls = str(['No information found'])

                    if bool(item['BT']):
                        if item['BT'] == 'a':
                            type = 'Journal/Article'
                        elif item['BT'] == 'b':
                            type = 'Book'
                        elif item['BT'] == 'p':
                            type = 'Conference Paper'
                        else:
                            type = str(['No information found'])
                    else:
                        type = str(['No information found'])
                    if 'DOI' not in obj:
                        doi = str(['No information found'])
                    else:
                        doi = item['DOI']
                    if 'PB' not in obj:
                        pb = str(['No information found'])
                    else:
                        pb = item['PB']

                    resp_obj = {"entities": {"Search Engine": "Microsoft Academy",
                                             "Attributes found": "DOI, Title, URLs, Authors, Publication Name, Cited count, Affiliation name, Type, Published date, Abstract",
                                             "items": [
                                                 {"DOI": doi,
                                                  "Title": item['Ti'],
                                                  "URLs": urls,
                                                  "Authors": item['AA'][0]['AuN'],
                                                  "Publication Name": pb,
                                                  "ISSN": str(['No Information found']),
                                                  "Cited count": item['CC'],
                                                  "Affiliation": item['AA'][0]['DAfN'],
                                                  "Type": type,
                                                  "Published date": item['D'],
                                                  "Abstract": abs_new

                                                  }
                                             ]}}
                    count += 1
                    # append dict object data
                    data.append(resp_obj)
                except Exception as e:  # raise e
                    pass
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    filename = exception_traceback.tb_frame.f_code.co_filename
                    line_number = exception_traceback.tb_lineno
                    logger.writeError(e, None, _engine, logging_flag, filename, line_number)

        time.sleep(1)
        logger.writeRecords(query, None, _engine, count, count, logging_flag)
        print(f'Finished with total {count} records returned.')
        return data

    if(not _from_yr):
    # keyword search
        if _keyword or _abstract:
            print('Searching in Microsoft Academic...')
            count = 0
            for i in tqdm(range(1)):
                url1 = 'https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=Composite(F.FN=%27' + q + '%27)&model=latest&count=' + str(
                    records) + '&offset=0&attributes=DOI,Ti,Y,BT,D,W,PB,CC,AA.AuN,AA.AuId,AA.DAfN,AA.AfN,S,AW&subscription-key=' + ms_api
                # response object
                response = requests.get(url1, headers=headers)
                soup = BeautifulSoup(response.content, 'lxml')
                obj = json.loads(soup.text)
                # set the counter for records count

                ######## Find required attributes in the response object
                for item in obj['entities']:
                    try:
                        # extract abstract keywords from the response as it doesnt have a spefcific abstract attribute
                        if ('AW' in item):
                            abs_str = str(item['AW'])
                            abs_new = abs_str.replace(',', '').replace("'", '')
                        else:
                            abs_new = str(['No information found'])

                        if bool('S' in item):
                            urls = item['S'][0]['U']
                        else:
                            urls = str(['No information found'])

                        if bool('BT' in item):
                            if item['BT'] == 'a':
                                type = 'Journal/Article'
                            elif item['BT'] == 'b':
                                type = 'Book'
                            elif item['BT'] == 'p':
                                type = 'Conference Paper'
                            else:
                                type = str(['No information found'])
                        else:
                            type = str(['No information found'])
                        if 'DOI' not in obj:
                            doi = str(['No information found'])
                        else:
                            doi = item['DOI']
                        if 'PB' not in obj:
                            pb = str(['No information found'])
                        else:
                            pb = item['PB']

                        resp_obj = {"entities": {"Search Engine": "Microsoft Academy",
                                                 "Attributes found": "DOI, Title, URLs, Authors, Publication Name, Cited count, Affiliation name, Type, Published date, Abstract",
                                                 "items": [
                                                     {"DOI": doi,
                                                      "Title": item['Ti'],
                                                      "URLs": urls,
                                                      "Authors": item['AA'][0]['AuN'],
                                                      "Publication Name": pb,
                                                      "ISSN": str(['No Information found']),
                                                      "Cited count": item['CC'],
                                                      "Affiliation": item['AA'][0]['DAfN'],
                                                      "Type": type,
                                                      "Published date": item['D'],
                                                      "Abstract": abs_new

                                                      }
                                                 ]}}
                        count += 1
                        # append dict object data
                        data.append(resp_obj)
                    except Exception as e:  # raise e
                        # pass
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        filename = exception_traceback.tb_frame.f_code.co_filename
                        line_number = exception_traceback.tb_lineno
                        logger.writeError(e, None, _engine, logging_flag, filename, line_number)

            time.sleep(1)
            logger.writeRecords(query, None, _engine, count, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data
    else:
        if _keyword or _abstract:

            print('Searching in Microsoft Academic...')
            count = 0
            for i in tqdm(range(1)):
                url1 = 'https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=And(Y='+ '[' + _from_yr + ','+ _to_yr_+']'+',Composite(F.FN==%27' + q + '%27))' + '&model=latest&count=' + str(
                    records) + '&offset=0&attributes=DOI,Ti,Y,BT,D,W,PB,CC,AA.AuN,AA.AuId,AA.DAfN,AA.AfN,S,AW&subscription-key=' + ms_api
                # response object
                response = requests.get(url1, headers=headers)
                soup = BeautifulSoup(response.content, 'lxml')
                obj = json.loads(soup.text)
                # set the counter for records count

                ######## Find required attributes in the response object
                for item in obj['entities']:
                    try:
                        # extract abstract keywords from the response as it doesnt have a spefcific abstract attribute
                        if ('AW' in item):
                            abs_str = str(item['AW'])
                            abs_new = abs_str.replace(',', '').replace("'", '')
                        else:
                            abs_new = str(['No information found'])

                        if bool('S' in item):
                            urls = item['S'][0]['U']
                        else:
                            urls = str(['No information found'])

                        if bool('BT' in item):
                            if item['BT'] == 'a':
                                type = 'Journal/Article'
                            elif item['BT'] == 'b':
                                type = 'Book'
                            elif item['BT'] == 'p':
                                type = 'Conference Paper'
                            else:
                                type = str(['No information found'])
                        else:
                            type = str(['No information found'])
                        if 'DOI' not in obj:
                            doi = str(['No information found'])
                        else:
                            doi = item['DOI']
                        if 'PB' not in obj:
                            pb = str(['No information found'])
                        else:
                            pb = item['PB']

                        resp_obj = {"entities": {"Search Engine": "Microsoft Academy",
                                                 "Attributes found": "DOI, Title, URLs, Authors, Publication Name, Cited count, Affiliation name, Type, Published date, Abstract",
                                                 "items": [
                                                     {"DOI": doi,
                                                      "Title": item['Ti'],
                                                      "URLs": urls,
                                                      "Authors": item['AA'][0]['AuN'],
                                                      "Publication Name": pb,
                                                      "ISSN": str(['No Information found']),
                                                      "Cited count": item['CC'],
                                                      "Affiliation": item['AA'][0]['DAfN'],
                                                      "Type": type,
                                                      "Published date": item['D'],
                                                      "Abstract": abs_new

                                                      }
                                                 ]}}
                        count += 1
                        # append dict object data
                        data.append(resp_obj)
                    except Exception as e:  # raise e
                        # pass
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        filename = exception_traceback.tb_frame.f_code.co_filename
                        line_number = exception_traceback.tb_lineno
                        logger.writeError(e, None, _engine, logging_flag, filename, line_number)

            time.sleep(1)
            logger.writeRecords(query, None, _engine, count, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data

