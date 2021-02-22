import sys
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import logger

# ignore warning messages
import warnings
warnings.filterwarnings('ignore')
### setting output display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

_engine="Elsevier Scopus"

def search_scopus(query, headers, _els_pages, records, _title, _keyword, _abstract,scp_api,_from_yr,_to_yr_, logging_flag, data):
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
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    filename = exception_traceback.tb_frame.f_code.co_filename
                    line_number = exception_traceback.tb_lineno
                    logger.writeError(e, None, _engine, logging_flag, filename, line_number)
        time.sleep(1)
        logger.writeRecords("Logging:", None, _engine, count, count, logging_flag)
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
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            filename = exception_traceback.tb_frame.f_code.co_filename
                            line_number = exception_traceback.tb_lineno
                            logger.writeError(e, None, _engine, logging_flag, filename, line_number)
            time.sleep(1)
            logger.writeRecords("Logging:", None, _engine, count, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data

    else:
        if _keyword or _abstract:
            rec=0
            if (_els_pages != 0):
                pages = pagination(_els_pages)
            else:
                pages = 1

            print('Searching in Elsevier Scopus...')
            count = 0
            for i in tqdm(range(1)):

                url = 'https://api.elsevier.com/content/search/scopus?query=' + query + '&apiKey=' + scp_api + '&date=' + _from_yr + '-' + _to_yr_ + '&start=' + str(
                    i) + '&count=10'

                # response object
                response = requests.get(url, headers=headers, timeout=30)
                soup = BeautifulSoup(response.content, 'lxml')

                # convert resonse into josn
                obj = json.loads(soup.text)
                rec = obj['search-results']['opensearch:totalResults']
                if (_els_pages != 0):
                    pages = pagination(_els_pages)
                else:
                    pages = pagination(rec)

                if(int(pages) >1000):
                    pages = 100
                    for i in range(pages):

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
                                exception_type, exception_object, exception_traceback = sys.exc_info()
                                filename = exception_traceback.tb_frame.f_code.co_filename
                                line_number = exception_traceback.tb_lineno
                                logger.writeError(e, None, _engine, logging_flag, filename, line_number)
                else:

                    for i in range(pages):

                        url = 'https://api.elsevier.com/content/search/scopus?query=' + query + '&apiKey=' + scp_api + '&date=' + _from_yr + '-' + _to_yr_ + '&start=' + str(
                            i) + '&count=10'

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
                                exception_type, exception_object, exception_traceback = sys.exc_info()
                                filename = exception_traceback.tb_frame.f_code.co_filename
                                line_number = exception_traceback.tb_lineno
                                logger.writeError(e, None, _engine, logging_flag, filename, line_number)
            time.sleep(1)
            logger.writeRecords("Logging:", None, _engine, rec, count, logging_flag)
            print(f'Finished with total {count} records returned.')
            return data

def processInputQuery(_query):
    special_characters = "+"
    if any(c in special_characters for c in _query):
        new_query = str(_query).replace("+", "AND")
        return new_query
    else:
        return _query


### method to find no of pages for webscrapping engines
def pagination(records):
    page = 1
    def_record = 10
    if (records == 10):
        page = 1
    else:
        page = round((float(records) / def_record)) + 1

    return page
