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
from Logging import logger

# ignore warning messages
import warnings
warnings.filterwarnings('ignore')

# setting output display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

_engine = "Academia"


def search_academia(query, headers, _pages, records, _title, _keyword, _abstract, _search_yr, logging_flag, data):
    if _title:
        print('Searching in Academia...')
        q = query.title().replace(' ', '_')
        url = 'https://www.academia.edu/search?q=' + query

        # response object
        response = requests.get(url, headers=headers, timeout=30)

        count = 0
        if response.status_code == 200:  # check for ok response
            soup = BeautifulSoup(response.content, 'html.parser')

            for i in tqdm(range(1)):
                # Find required attributes in the response object
                for item in soup.find_all('div', class_='a-fadeInDown'):
                    abs = ''
                    try:

                        # few records doesnt have summary attribute so check them
                        if bool(item.find_all('div', class_='work-card--abstract')):
                            # if 'summarized' in soup.find_all('div', class_='u-borderBottom1'):
                            abs = item.find_all('div', class_='work-card--abstract')

                        else:
                            abs = ['No information found']

                        resp_obj = {"entities": {"Search Engine": "Academia Search Engine",
                                                 "Attributes found": "Title, URLs, Authors, Abstract",
                                                 "items": [
                                                     {"DOI": ['No information found'],
                                                      "Title": item.find_all('div', class_='work-card--title')[
                                                          0].get_text(),
                                                      "URLs": item.select('a')[0]['href'],
                                                      "Authors": item.find_all('div', class_='work-card--author-name')[
                                                          0].get_text(),
                                                      "Publication Name": str(
                                                          item.find_all('div', class_='work-card--publish-wrapper')[
                                                              0].get_text()).split(',', 1)[1],
                                                      "ISSN": ['No information found'],
                                                      "Cited count": ['No information found'],
                                                      "Affiliation": ['No information found '],
                                                      "Type": ['No information found'],
                                                      "Published date": str(
                                                          item.find_all('div', class_='work-card--publish-wrapper')[
                                                              0].get_text()).split(',', 1)[0],
                                                      "Abstract": abs
                                                      }
                                                 ]}}
                        count += 1
                        data.append(resp_obj)
                        # append dict object data

                    except Exception as e:  # raise e
                        pass
                        logger.writeError("Logging Erorr:" + str(e), None, _engine, logging_flag)

            else:
                pass
            time.sleep(1)
            logger.writeRecords(query, None, _engine, count, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data

    if _keyword or _abstract:

        print('Searching in Academia...')
        if _search_yr:
            print('Date parameter search either not supported or not available in this search engine!')
        else:
            count = 0
            for i in tqdm(range(1)):

                for i in range(_pages):
                    # url = 'https://www.academia.edu/search?q=' + query
                    q = query.title().replace(' ', '_')
                    url = 'https://www.academia.edu/Documents/in/' + q + '?page=' + str(i)

                    # response object
                    response = requests.get(url, headers=headers, timeout=30)

                    if response.status_code == 200:  # check for ok response
                        soup = BeautifulSoup(response.content, 'html.parser')

                        # Find required attributes in the response object
                        for item in soup.find_all('div', class_='u-borderBottom1'):
                            abs = ''
                            try:
                                # try:
                                # few records doesnt have summary attribute so check them
                                if bool(item.select('.summarized')):
                                    # if 'summarized' in soup.find_all('div', class_='u-borderBottom1'):
                                    abs = item.select('.summarized')[0].get_text()

                                    # except Exception as e:  # raise e
                                elif bool(item.select('.summary')):
                                    abs = item.select('.summary')[0].get_text()
                                else:
                                    abs = ['No information found']

                                resp_obj = {"entities": {"Search Engine": "Academia Search Engine",
                                                         "Attributes found": "Title, URLs, Authors, Abstract",
                                                         "items": [
                                                             {"DOI": ['No information found'],
                                                              "Title": item.select('a')[0].get_text(),
                                                              "URLs": item.select('a')[0]['href'],
                                                              "Authors": item.select('.u-fw700')[0].get_text(),
                                                              "Publication Name": ['No information found'],
                                                              "ISSN": ['No information found'],
                                                              "Cited count": ['No information found'],
                                                              "Affiliation": ['No information found '],
                                                              "Type": ['No information found'],
                                                              "Published date": ['No information found'],
                                                              "Abstract": abs
                                                              }
                                                         ]}}
                                count += 1
                                data.append(resp_obj)
                                # append dict object data

                            except Exception as e:  # raise e
                                # pass
                                logger.writeError("Logging Erorr:" + str(e), None, _engine, logging_flag)

                        else:
                            pass
            time.sleep(1)
            logger.writeRecords(query, None, _engine, count, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data
