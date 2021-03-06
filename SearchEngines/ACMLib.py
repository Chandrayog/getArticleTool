"""
   Individual Search Engine Module.

 * Copyright (C) Cape Breton University, Prof. Enayat Rajabi - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * without written consent from the owners.
 * Proprietary and confidential
 * Written by Chandrayog Yadav <chandrayog.2@gmail.com>, January 2021

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import sys
from Logging import logger

# ignore warning messages
import warnings

warnings.filterwarnings('ignore')
# setting output display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

_engine = "ACM Library"


def search_acmlibrary(query, headers, _acm_pages, records, _title, _keyword, _abstract, _from_yr, _to_yr_, logging_flag,
                      data):
    query = processInputQuery(query)
    if _title:

        url = 'https://dl.acm.org/action/doSearch?AllField=%22' + query + '%22'

        # response object
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        # obj = json.loads(soup.text)

        print('Searching in ACM Library...')
        # set the counter for records count
        count = 0
        for i in tqdm(range(1)):

            ######## Find required attributes in the response object
            for item in soup.select('li', class_='search__item issue-item-container'):
                try:
                    resp_obj = {"entities": {"Search Engine": "ACM Library Search Engine",
                                             "Attributes found": "DOI, Title, URLs, Authors, Citation count, Type, Published date, Abstract",
                                             "items": [
                                                 {"DOI": item.find("span", class_='hlFld-Title').find_all('a')[0][
                                                     'href'],
                                                  "Title": item.find_all("h5", class_='issue-item__title')[
                                                      0].get_text().strip(),
                                                  "URLs": item.find_all("a", class_='issue-item__doi')[0]['href'],
                                                  "Authors": item.find_all("ul", class_='truncate-list')[
                                                      0].get_text().strip().replace('\n', ''),
                                                  "Publication Name": str(['No information found']),
                                                  "ISSN": str(['No information found']),

                                                  "Cited count": item.find("span", class_='citation').find_all('span')[
                                                      0].get_text(),
                                                  "Affiliation": str(['No information found ']),
                                                  "Type": item.find_all("div", class_='issue-heading')[0].get_text(),
                                                  "Published date":
                                                      item.find("span", class_='dot-separator').find_all('span')[
                                                          0].get_text(),
                                                  "Abstract": str(item.find_all("div", class_='issue-item__abstract')[
                                                                      0].get_text()).strip().replace('\n', '').replace(
                                                      '  ',
                                                      '')
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

    if _keyword or _abstract:

        print('Searching in ACM Library...')
        if (_acm_pages != 0):
            pages = pagination(_acm_pages)
        else:
            pages = 1

        if len(_from_yr) != 0:
            count = 0
            for i in tqdm(range(1)):

                url = 'https://dl.acm.org/action/doSearch?AllField=' + query + '&AfterYear=' + _from_yr + '&BeforeYear=' + _to_yr_ + '&pageSize=20&startPage=' + str(
                    i)

                # response object
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'lxml')

                # count no of records returned by engine
                for item in soup.find_all('span', class_='hitsLength'):
                    rec = str(soup.find_all('span', class_='hitsLength')[0].get_text()).replace(',', '').replace(" ",
                                                                                                                 "")

                    pages = 1
                    if (_acm_pages != 0):
                        pages = pagination(_acm_pages)
                    else:
                        pages = pagination(int(rec))

                if int(pages) > 100:
                    print(
                        "NOTE:ACM Library returns data for max 2000 records irrespective of total records. Total No of total records found :",
                        rec, "\n Fetching records details now...")

                    pages = 50
                    for i in range(pages):
                        url = 'https://dl.acm.org/action/doSearch?AllField=' + query + '&AfterYear=' + _from_yr + '&BeforeYear=' + _to_yr_ + '&pageSize=20&startPage=' + str(
                            i)

                        response = requests.get(url, headers=headers)
                        soup = BeautifulSoup(response.content, 'lxml')
                        # Find required attributes in the response object
                        for item in soup.select('li', class_='search__item issue-item-container'):
                            try:
                                resp_obj = {"entities": {"Search Engine": "ACM Library Search Engine",
                                                         "Attributes found": "DOI, Title, URLs, Authors, Citation count, Type, Published date, Abstract",
                                                         "items": [
                                                             {"DOI":
                                                                  item.find("span", class_='hlFld-Title').find_all('a')[
                                                                      0][
                                                                      'href'],
                                                              "Title": item.find_all("h5", class_='issue-item__title')[
                                                                  0].get_text().strip(),
                                                              "URLs": item.find_all("a", class_='issue-item__doi')[0][
                                                                  'href'],
                                                              "Authors": item.find_all("ul", class_='truncate-list')[
                                                                  0].get_text().strip().replace('\n', ''),
                                                              "Publication Name": str(['No information found']),
                                                              "ISSN": str(['No information found']),

                                                              "Cited count":
                                                                  item.find("span", class_='citation').find_all('span')[
                                                                      0].get_text(),
                                                              "Affiliation": str(['No information found']),
                                                              "Type": item.find_all("div", class_='issue-heading')[
                                                                  0].get_text(),
                                                              "Published date":
                                                                  item.find("span", class_='dot-separator').find_all(
                                                                      'span')[
                                                                      0].get_text(),
                                                              "Abstract": str(
                                                                  item.find_all("div", class_='issue-item__abstract')[
                                                                      0].get_text()).strip().replace('\n', '').replace(
                                                                  '  ',
                                                                  '')
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
            else:
                for i in range(pages):
                    ######## Find required attributes in the response object
                    for item in soup.select('li', class_='search__item issue-item-container'):
                        try:
                            resp_obj = {"entities": {"Search Engine": "ACM Library Search Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, Citation count, Type, Published date, Abstract",
                                                     "items": [
                                                         {"DOI":
                                                              item.find("span", class_='hlFld-Title').find_all('a')[0][
                                                                  'href'],
                                                          "Title": item.find_all("h5", class_='issue-item__title')[
                                                              0].get_text().strip(),
                                                          "URLs": item.find_all("a", class_='issue-item__doi')[0][
                                                              'href'],
                                                          "Authors": item.find_all("ul", class_='truncate-list')[
                                                              0].get_text().strip().replace('\n', ''),
                                                          "Publication Name": str(['No information found']),
                                                          "ISSN": str(['No information found']),

                                                          "Cited count":
                                                              item.find("span", class_='citation').find_all('span')[
                                                                  0].get_text(),
                                                          "Affiliation": str(['No information found']),
                                                          "Type": item.find_all("div", class_='issue-heading')[
                                                              0].get_text(),
                                                          "Published date":
                                                              item.find("span", class_='dot-separator').find_all(
                                                                  'span')[
                                                                  0].get_text(),
                                                          "Abstract": str(
                                                              item.find_all("div", class_='issue-item__abstract')[
                                                                  0].get_text()).strip().replace('\n', '').replace(
                                                              '  ',
                                                              '')
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

        else:
            count = 0
            for i in tqdm(range(1)):

                for i in range(pages):

                    url = 'https://dl.acm.org/action/doSearch?AllField=' + query + '&pageSize=20&startPage=' + str(i)
                    # response object
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.content, 'lxml')
                    # obj = json.loads(soup.text)

                    # set the counter for records count

                    # Find required attributes in the response object
                    for item in soup.select('li', class_='search__item issue-item-container'):
                        try:
                            resp_obj = {"entities": {"Search Engine": "ACM Library Search Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, Citation count, Type, Published date, Abstract",
                                                     "items": [
                                                         {"DOI":
                                                              item.find("span", class_='hlFld-Title').find_all('a')[0][
                                                                  'href'],
                                                          "Title": item.find_all("h5", class_='issue-item__title')[
                                                              0].get_text().strip(),
                                                          "URLs": item.find_all("a", class_='issue-item__doi')[0][
                                                              'href'],
                                                          "Authors": item.find_all("ul", class_='truncate-list')[
                                                              0].get_text().strip().replace('\n', ''),
                                                          "Publication Name": str(['No information found']),
                                                          "ISSN": str(['No information found']),

                                                          "Cited count":
                                                              item.find("span", class_='citation').find_all('span')[
                                                                  0].get_text(),
                                                          "Affiliation": str(['No information found']),
                                                          "Type": item.find_all("div", class_='issue-heading')[
                                                              0].get_text(),
                                                          "Published date":
                                                              item.find("span", class_='dot-separator').find_all(
                                                                  'span')[
                                                                  0].get_text(),
                                                          "Abstract": str(
                                                              item.find_all("div", class_='issue-item__abstract')[
                                                                  0].get_text()).strip().replace('\n', '').replace(
                                                              '  ',
                                                              '')
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


def processInputQuery(_query):
    special_characters = "+"
    if any(c in special_characters for c in _query):
        new_query = str(_query).replace("+", "%2B%2B")
        return new_query
    else:
        return _query


# method to find no of pages for webscrapping engines
def pagination(records):
    page = 1
    def_record = 10
    if (records == 10):
        page = 1
    else:
        page = round((float(records) / def_record)) + 1

    return page
