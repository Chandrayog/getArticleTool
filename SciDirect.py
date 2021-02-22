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

_engine ="Science Direct Engine"


def search_sciDirect(query, headers, _pages,records, _title, _keyword, _abstract,sd1_api,sd2_api,_from_yr,_to_yr_, logging_flag, data):
    if (_pages > 3):
        _pages=3

    if _title:
        url = 'https://www.sciencedirect.com/search/api?qs=%22' + query + '%22&apiKey=' + sd1_api

        # response object
        response = requests.get(url, headers={'User-agent': 'your bot 0.1'}, timeout=30)
        soup = BeautifulSoup(response.content, 'lxml')
        obj = json.loads(soup.text)

        print('Searching in Science Direct...')
        # set the counter for records count
        count = 0
        for i in tqdm(range(1)):

            ######## Find required attributes in the response object
            for item in obj['searchResults']:
                try:
                    publish_date = str(item['publicationDate'])

                    # get document ID from the result first
                    doi = item['doi']

                    # call again api with DOI to the get the attriutes
                    url2 = 'https://api.elsevier.com/content/article/doi/' + doi + '?apiKey=' + sd2_api
                    response1 = requests.get(url2, headers=headers, timeout=30)
                    soup1 = BeautifulSoup(response1.content, 'lxml')
                    if "prism:Issn" and "prism:issn" "prism:eIssn" and "prism:eissn" not in soup1.find_all('coredata'):
                        issn = str(['No information found'])
                    ######## Find required attributes in the response object
                    for item in soup1.find_all('coredata'):
                        resp_obj = {"entities": {"Search Engine": "Science Direct Search Engine",
                                                 "Attributes found": "DOI, Title, URLs, Authors, Publication Name, ISSN, Type, Published date, Abstract",
                                                 "items": [
                                                     {"DOI": item.find_all('prism:doi')[0].get_text(),
                                                      "Title": item.find_all('dc:title')[0].get_text().strip(),
                                                      "URLs": item.find_all('prism:url')[0].get_text(),
                                                      "Authors": item.find_all('dc:creator')[0].get_text(),
                                                      "Publication Name": item.find_all('prism:publicationname')[
                                                          0].get_text(),
                                                      "ISSN": issn,
                                                      # "ISSN": item.find_all('prism:issn')[0].get_text(),
                                                      "Cited count": str(['No information found']),
                                                      "Affiliation": str(['No information found ']),
                                                      "Type": item.find_all('document-type'),
                                                      "Published date": publish_date,
                                                      "Abstract": str(item.find_all('dc:description')[
                                                                          0].get_text().strip()).replace('\n',
                                                                                                         '').replace(
                                                          '  ', '')
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
        logger.writeRecords("Logging", None, _engine, count, count, logging_flag)
        print(f'Finished with total {count} records returned.')
        return data
    if (not _from_yr):
        if _keyword or _abstract:
            for j in tqdm(range(1)):
                print('Searching in Science Direct...')
                # set the counter for records count
                count = 0
                for i in range(_pages):
                    url = 'https://api.elsevier.com/content/search/sciencedirect?query=' + query + '&apiKey=' + sd1_api +'&start=' + str(i) + '&count=10'

                    # response object
                    response = requests.get(url, headers={'User-agent': 'your bot 0.1'})
                    soup = BeautifulSoup(response.content, 'lxml')
                    obj = json.loads(soup.text)

                    if 'entry' in obj['search-results']:
                            ######## Find required attributes in the response object
                            for item in obj['search-results']['entry']:
                                try:
                                    publish_date = str(item['load-date']).split('T', -1)[0]

                                    # get document ID from the result first
                                    doi = item['prism:doi']

                                    # call again api with DOI to the get the attriutes
                                    url2 = 'https://api.elsevier.com/content/article/doi/' + doi + '?apiKey=' + sd2_api
                                    response1 = requests.get(url2, headers=headers)
                                    soup1 = BeautifulSoup(response1.content, 'lxml')
                                    if "prism:Issn" and "prism:issn" "prism:eIssn" and "prism:eissn" not in soup1.find_all(
                                            'coredata'):
                                        issn = str(['No information found'])
                                    ######## Find required attributes in the response object
                                    for item in soup1.find_all('coredata'):
                                        resp_obj = {"entities": {"Search Engine": "Science Direct Search Engine",
                                                                 "Attributes found": "DOI, Title, URLs, Authors, Publication Name, ISSN, Type, Published date, Abstract",
                                                                 "items": [
                                                                     {"DOI": item.find_all('prism:doi')[0].get_text(),
                                                                      "Title": item.find_all('dc:title')[0].get_text().strip(),
                                                                      "URLs": item.find_all('prism:url')[0].get_text(),
                                                                      "Authors": item.find_all('dc:creator')[0].get_text(),
                                                                      "Publication Name": item.find_all('prism:publicationname')[
                                                                          0].get_text(),
                                                                      "ISSN": issn,
                                                                      # "ISSN": item.find_all('prism:issn')[0].get_text(),
                                                                      "Cited count": str(['No information found']),
                                                                      "Affiliation": str(['No information found ']),
                                                                      "Type": item.find_all('document-type'),
                                                                      "Published date": publish_date,
                                                                      "Abstract": str(item.find_all('dc:description')[
                                                                                          0].get_text().strip()).replace('\n',
                                                                                                                         '').replace(
                                                                          '  ', '')
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
        logger.writeRecords("Logging", None, _engine, count, count, logging_flag)
        print(f'Finished with total {count} records returned.')
        return data
    else:
        if _keyword or _abstract:
            for i in tqdm(range(1)):
                print('Searching in Science Direct...')

                # set the counter for records count
                count = 0
                for i in range(_pages):
                    url = 'https://api.elsevier.com/content/search/sciencedirect?query=' + query + '&date=' + _from_yr+'-'+_to_yr_ + '&apiKey=' + sd1_api +'&start=' + str(i) + '&count=10'

                    # response object
                    response = requests.get(url, headers={'User-agent': 'your bot 0.1'})
                    soup = BeautifulSoup(response.content, 'lxml')
                    obj = json.loads(soup.text)
                    if 'entry' in obj['search-results']:
                            ######## Find required attributes in the response object
                            for item in obj['search-results']['entry']:
                                try:
                                    publish_date = str(item['load-date']).split('T', -1)[0]

                                    # get document ID from the result first
                                    doi = item['prism:doi']

                                    # call again api with DOI to the get the attriutes
                                    url2 = 'https://api.elsevier.com/content/article/doi/' + doi + '?apiKey=' + sd2_api
                                    response1 = requests.get(url2, headers=headers)
                                    soup1 = BeautifulSoup(response1.content, 'lxml')
                                    if "prism:Issn" and "prism:issn" "prism:eIssn" and "prism:eissn" not in soup1.find_all(
                                            'coredata'):
                                        issn = str(['No information found'])
                                    ######## Find required attributes in the response object
                                    for item in soup1.find_all('coredata'):
                                        resp_obj = {"entities": {"Search Engine": "Science Direct Search Engine",
                                                                 "Attributes found": "DOI, Title, URLs, Authors, Publication Name, ISSN, Type, Published date, Abstract",
                                                                 "items": [
                                                                     {"DOI": item.find_all('prism:doi')[0].get_text(),
                                                                      "Title": item.find_all('dc:title')[0].get_text().strip(),
                                                                      "URLs": item.find_all('prism:url')[0].get_text(),
                                                                      "Authors": item.find_all('dc:creator')[0].get_text(),
                                                                      "Publication Name":
                                                                          item.find_all('prism:publicationname')[
                                                                              0].get_text(),
                                                                      "ISSN": issn,
                                                                      # "ISSN": item.find_all('prism:issn')[0].get_text(),
                                                                      "Cited count": str(['No information found']),
                                                                      "Affiliation": str(['No information found ']),
                                                                      "Type": item.find_all('document-type'),
                                                                      "Published date": publish_date,
                                                                      "Abstract": str(item.find_all('dc:description')[
                                                                                          0].get_text().strip()).replace('\n',
                                                                                                                         '').replace(
                                                                          '  ', '')
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
            logger.writeRecords("Logging", None, _engine, count, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data


