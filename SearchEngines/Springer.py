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

_engine = "Springer"


def search_springer(query, headers, _pages, records, _title, _keyword, _abstract, spr_api, _search_yr, logging_flag,
                    data):
    print('Searching in Springer...')

    if not _search_yr:
        count = 0
        for i in tqdm(range(1)):

            for i in range(_pages):

                url = 'http://api.springernature.com/meta/v2/json?q=' + query + '&s=' + str(
                    i) + '&p=10&api_Key=' + spr_api

                # response object
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'lxml')
                obj = json.loads(soup.text)

                # set the counter for records count

                # Find required attributes in the response object
                for item in obj['records']:

                    if 'issn' in obj['records']:
                        issn = item['issn']
                    elif 'isbn' in obj['records']:
                        issn = item['isbn']
                    else:
                        issn = str(['No Information found'])

                        try:
                            resp_obj = {"entities": {"Search Engine": "Springer Search Engine",
                                                     "Attributes found": "DOI, Title, URLs, Authors, Publication "
                                                                         "Name, ISSN, Type, Published date, Abstract",
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
        print("Date parameter either not supported or not available in Springer API!")
        return
