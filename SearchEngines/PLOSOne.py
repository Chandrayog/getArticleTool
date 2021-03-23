"""
   Individual Search Engine Module.

 * Copyright (C) Cape Breton University, Prof. Enayat Rajabi - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * without written consent from the owners.
 * Proprietary and confidential
 * Written by Chandrayog Yadav <chandrayog.2@gmail.com>, January 2021

"""

import requests
import json
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

_engine = "PLOS One Engine"


def search_PlosOne(query, headers, _pages, records, _title, _keyword, _abstract, _from_yr, _to_yr_, logging_flag, data):
    if _title:
        print('Searching in PLOS ONE...')
        count = 0

        # search_PlosOne_title(query)
        url = 'http://api.plos.org/search?q=title:' + query + '&start=1&rows=' + str(records)
        # response object
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        obj = json.loads(soup.text)

        # set the counter for records count
        try:
            for i in tqdm(range(1)):

                # Find required attributes in the response object
                for item in obj['response']['docs']:
                    try:

                        resp_obj = {"entities": {"Search Engine": "PLOS Engine",
                                                 "Attributes found": "DOI, Title, URLs, Authors, ISSN, Type, "
                                                                     "Published date, Abstract",
                                                 "items": [
                                                     {"DOI": item['id'],
                                                      "Title": item['title_display'],
                                                      "URLs": 'https://doi.org/' + item['id'],
                                                      "Authors": item['author_display'],
                                                      "Publication Name": str(['No information found']),
                                                      # "Publication Name": item['publisher'],
                                                      "ISSN": item['eissn'],
                                                      "Cited count": str(['No information found']),
                                                      "Affiliation": str(['No information found ']),
                                                      "Type": item['article_type'],
                                                      "Published date": str(item['publication_date']).split('T', -1)[0],
                                                      "Abstract": str(item['abstract']).strip().replace('\n',
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
            logger.writeRecords(query, None, _engine, count, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data
        except Exception as e:  # raise e
            pass
            time.sleep(1)
            print('Some error happend in PLOS Engine!')

    if not _from_yr:
        if _keyword or _abstract:

            print('Searching in PLOS ONE...')
            _rec = round(float(records))
            count = 0
            try:
                for i in tqdm(range(1)):

                    url = 'http://api.plos.org/search?q=' + query + '&start=1&rows=' + str(_rec)
                    # response object
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    obj = json.loads(soup.text)

                    for item in obj['response']['docs']:
                        try:

                            resp_obj = {"entities": {"Search Engine": "PLOS Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, ISSN, Type, Published date, Abstract",
                                                     "items": [
                                                         {"DOI": item['id'],
                                                          "Title": item['title_display'],
                                                          "URLs": 'https://doi.org/' + item['id'],
                                                          "Authors": item['author_display'],
                                                          "Publication Name": str(['No information found']),
                                                          # "Publication Name": item['publisher'],
                                                          "ISSN": item['eissn'],
                                                          "Cited count": str(['No information found']),
                                                          "Affiliation": str(['No information found ']),
                                                          "Type": item['article_type'],
                                                          "Published date":
                                                              str(item['publication_date']).split('T', -1)[0],
                                                          "Abstract": str(item['abstract']).strip().replace('\n',
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
                logger.writeRecords(query, None, _engine, count, count, logging_flag)
                print(f'Finished with total {count} records returned.')
                return data

            except Exception as e:  # raise e
                pass
    else:
        if _keyword or _abstract:
            print('Searching in PLOS ONE...')
            _rec = round(float(records))
            count = 0
            try:
                for i in tqdm(range(1)):

                    url = 'http://api.plos.org/search?q=' + query + ' AND publication_date:[' + _from_yr + '-01-01T00:00:00Z TO ' + _to_yr_ + '-12-31T23:59:59Z]' + '&start=1&rows=' + str(
                        _rec)
                    # response object
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    obj = json.loads(soup.text)
                    for item in obj['response']['docs']:
                        try:

                            resp_obj = {"entities": {"Search Engine": "PLOS Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, ISSN, Type, Published date, Abstract",
                                                     "items": [
                                                         {"DOI": item['id'],
                                                          "Title": item['title_display'],
                                                          "URLs": 'https://doi.org/' + item['id'],
                                                          "Authors": item['author_display'],
                                                          "Publication Name": str(['No information found']),
                                                          # "Publication Name": item['publisher'],
                                                          "ISSN": item['eissn'],
                                                          "Cited count": str(['No information found']),
                                                          "Affiliation": str(['No information found ']),
                                                          "Type": item['article_type'],
                                                          "Published date":
                                                              str(item['publication_date']).split('T', -1)[0],
                                                          "Abstract": str(item['abstract']).strip().replace('\n',
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
                logger.writeRecords(query, None, _engine, count, count, logging_flag)
                print(f'Finished with total {count} records returned.')
                return data

            except Exception as e:  # raise e
                pass
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                logger.writeError(e, None, _engine, logging_flag, filename, line_number)
