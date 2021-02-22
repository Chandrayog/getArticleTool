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
import sys
import logger


search_query = ''
_title = False
_keyword = False
_abstract = False
_records = str(10)
_engine = "PubMed Engine"

### 2. PubMed Search Engine
def search_pubMed(query, headers, _pages, _title, _keyword, _abstract,_from_yr,_to_yr_, logging_flag, data):
    if _title:
        print('Searching in PubMed...')
        count = 0
        for i in tqdm(range(1)):

            for i in range(_pages):

                url = 'https://pubmed.ncbi.nlm.nih.gov/?term=%22' + query + '%22' + '&size=10&page=1'
                # response object
                response = requests.get(url, headers=headers, timeout=30)
                soup = BeautifulSoup(response.content, 'lxml')

                for item in soup.find_all('div', class_='article-page'):
                    try:
                        try:
                            # few records doesnt have summary attribute so check them
                            if bool(item.find_all('div', class_='abstract')[0].get_text()):
                                abs = str(item.find_all('div', class_='abstract')[0].get_text()).strip().replace('\n',
                                                                                                                 '')
                        except Exception as e:  # raise e
                            abs = ['No information found']

                        if bool(item.select('.secondary-date')):
                            pub_datestr(item.find_all('span', class_='secondary-date')[0].get_text()).split(';', -1)[0]
                        else:
                            pub_date = ['No information found']

                        resp_obj = {"entities": {"Search Engine": "PubMed Engine",
                                                 "Attributes found": "DOI,Title, URLs, Authors,Type, Published Date, Abstract",
                                                 "items": [
                                                     {"DOI": str(item.find_all('span', class_='citation-doi')[
                                                                     0].get_text()).replace('\n', ''),
                                                      "Title": str(
                                                          item.find_all('h1', class_='heading-title')[
                                                              0].get_text()).strip(),
                                                      "URLs": 'https://pubmed.ncbi.nlm.nih.gov' +
                                                              item.find_all('a', class_='id-link')[0]['href'],
                                                      "Authors": str(
                                                          item.find_all('span', class_='authors-list-item')[
                                                              0].get_text()).strip().replace('\n', ''),
                                                      "Publication Name": str(['No information found']),
                                                      "ISSN": str(['No information found']),
                                                      "Cited count": str(['No information found']),
                                                      "Affiliation": str(['No information found ']),
                                                      "Type": str(['article']),
                                                      "Published date":pub_date,
                                                      "Abstract": abs
                                                      }
                                                 ]}}
                        count += 1
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

    if _keyword or _abstract:
        print('Searching in PubMed...')
        count = 0
        authr_list=[]

        if (_from_yr):
            for i in tqdm(range(1)):
                for i in range(_pages):
                    i += 1
                    url = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + query +'&filter=years.'+_from_yr+'-'+_to_yr_ +'&format=abstract&size=10&page=' + str(i)
                    # response object
                    response = requests.get(url, headers=headers, timeout=30)
                    soup = BeautifulSoup(response.content, 'lxml')

                    for item in soup.select('div', class_='results-article'):
                        try:

                            if bool(item.find_all('span', class_='cit')):
                                pub_date= str(item.find_all('span', class_='cit')[0].get_text()).split(';', 1)[0].replace('\n', '')
                            else:
                                pub_date= str(item.find_all('span', class_='secondary-date')[0].get_text()).split('b', 1)[1].replace('\n', '')

                            if bool(item.select('.copyright')):
                                pub_name=str(item.find_all('p', class_='copyright')[0].get_text()).strip()
                            else:
                                pub_name=['No information found']

                            if bool(item.select('.authors-list')):
                                for i in range(len(item.find('div', class_='authors-list').find_all('a'))):
                                    authr_list.append(str(item.find('div', class_='authors-list').find_all('a')[i].get_text()).strip())
                            else:
                                authr_list=['No information found']

                            resp_obj = {"entities": {"Search Engine": "PubMed Engine",
                                                     "Attributes found": "DOI,Title, URLs, Authors,Type, Published Date,Publication Name,Affiliation, Abstract",
                                                     "items": [
                                                         {"DOI":str(item.find_all('span', class_='citation-doi')[0].get_text()).split('doi', 1)[1].replace('\n', ''),
                                                          "Title":str(item.find_all('h1', class_='heading-title')[0].get_text()).strip() ,
                                                          "URLs": 'https://pubmed.ncbi.nlm.nih.gov' +item.find('h1', class_="heading-title").find_all("a")[0]['href'],
                                                          "Authors": authr_list,
                                                          "Publication Name": pub_name,
                                                          "ISSN": str(['No information found']),
                                                          "Cited count": str(['No information found']),
                                                          "Affiliation": str(item.select('li[data-affiliation-id]')[0].get_text()),
                                                          "Type": str(['article']),
                                                          "Published date": pub_date,
                                                          "Abstract": str(
                                                              item.find_all('div', class_='abstract-content')[0].get_text()).strip()
                                                          }
                                                     ]}}
                            count += 1
                            data.append(resp_obj)
                            #print(data.items())

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
            for i in tqdm(range(1)):
                for i in range(_pages):
                    i += 1
                    url = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + query + '&format=abstract&size=10&page=' + str(i)
                    # response object
                    response = requests.get(url, headers=headers, timeout=30)
                    soup = BeautifulSoup(response.content, 'lxml')

                    for item in soup.select('div', class_='search-results'):
                        try:

                            if bool(item.select('.secondary-date')):
                                pub_date = \
                                str(item.find_all('span', class_='secondary-date')[0].get_text()).split('b', 1)[
                                    1].replace('\n', '')
                            else:
                                pub_date = ['No information found']

                            if bool(item.select('.copyright')):
                                pub_name = str(item.find_all('p', class_='copyright')[0].get_text()).strip()
                            else:
                                pub_name = ['No information found']

                            if bool(item.select('.authors-list')):
                                for i in range(len(item.find('div', class_='authors-list').find_all('a'))):
                                    authr_list.append(str(
                                        item.find('div', class_='authors-list').find_all('a')[i].get_text()).strip())
                            else:
                                authr_list = ['No information found']

                            resp_obj = {"entities": {"Search Engine": "PubMed Engine",
                                                     "Attributes found": "DOI,Title, URLs, Authors,Type, Published Date,Publication Name,Affiliation, Abstract",
                                                     "items": [
                                                         {"DOI": str(item.find_all('span', class_='citation-doi')[
                                                                         0].get_text()).split('doi', 1)[1].replace('\n',
                                                                                                                   ''),
                                                          "Title": str(item.find_all('h1', class_='heading-title')[
                                                                           0].get_text()).strip(),
                                                          "URLs": 'https://pubmed.ncbi.nlm.nih.gov' +
                                                                  item.find('h1', class_="heading-title").find_all("a")[
                                                                      0]['href'],
                                                          "Authors": authr_list,
                                                          "Publication Name": pub_name,
                                                          "ISSN": str(['No information found']),
                                                          "Cited count": str(['No information found']),
                                                          "Affiliation": str(
                                                              item.select('li[data-affiliation-id]')[0].get_text()),
                                                          "Type": str(['article']),
                                                          "Published date": pub_date,
                                                          "Abstract": str(
                                                              item.find_all('div', class_='abstract-content')[
                                                                  0].get_text()).strip()
                                                          }
                                                     ]}}
                            count += 1

                            data.append(resp_obj)
                            # print(data.items())

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

