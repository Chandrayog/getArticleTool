import sys
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as n
import time
from tqdm import tqdm
import re
from scraper_api import ScraperAPIClient
import requests
import logger

# ignore warning messages
import warnings
warnings.filterwarnings('ignore')

### setting output display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

_engine="Google Scholar"

def search_googleScholar(query,headers,_gs_pages,records, _title, _keyword, _abstract, scrpr_api, _from_yr,_to_yr_,logging_flag, data):
    rec = 0
    if _title:
        # request url
        url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=%22' + query + '%22&btnG='

        # response object
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        print('Searching in Google Scholar...')
        # set the counter for records count
        count = 0
        for i in tqdm(range(1)):

            ######## Find required attributes in the response object by checking tag [data-lid]'))
            for item in soup.select('[data-lid]'):
                try:
                    if bool(item.select('.gs_or_ggsm')):
                        cc = str(re.findall(r'\d+', str(item.select('.gs_fl')[1].get_text()))).split(',', 1)[0].replace(
                            '[', '')
                    else:
                        cc = str(re.findall(r'\d+', str(item.select('.gs_fl')[0].get_text()))).split(',', 1)[0].replace(
                            '[', '')

                    if bool(item.select('.gs_ct1')):
                        type = str(item.select('.gs_ct1')[0].get_text())
                    else:
                        type = str(['Research Article'])

                    resp_obj = {"entities": {"Search Engine": "Google Scholar",
                                             "Attributes found": "Title, URLs, Authors, Cited count, Type, Published date, Abstract",
                                             "items": [
                                                 {"DOI": str(['No information found']),
                                                  "Title": item.select('h3')[0].get_text(),
                                                  "URLs": item.select('a')[0]['href'],
                                                  "Authors": re.sub("[^A-Za-z]", " ",
                                                                    str(item.select('.gs_a')[0].get_text()).split('-',
                                                                                                                  1)[
                                                                        0]),
                                                  "Publication Name": str(['No information found']),
                                                  "ISSN": str(['No information found']),
                                                  "Cited count": cc,
                                                  "Affiliation": str(['No information found']),
                                                  "Type": type,
                                                  "Published date": str(re.findall(r'\d+', str(
                                                      item.select('.gs_a')[0].get_text()))).strip(),
                                                  "Abstract": item.select('.gs_rs')[0].get_text()
                                                  }
                                             ]}}
                    # append dict object data
                    count += 1
                    data.append(resp_obj)
                except Exception as e:  # raise e
                    pass
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    filename = exception_traceback.tb_frame.f_code.co_filename
                    line_number = exception_traceback.tb_lineno
                    logger.writeError(e,None, _engine, logging_flag, filename,line_number)
        time.sleep(1)

        print(f'Finished with total {count} records returned.')
        logger.writeRecords(query, None, _engine, "1", count,logging_flag)
        return data

    if _keyword or _abstract:
        if(_gs_pages!=0):
           pages = pagination(_gs_pages)
        else:
            pages=1

        # search for dates
        if (_from_yr):

            ### use of scraper api to avoid IP block issue by Google scholar
            client = ScraperAPIClient(scrpr_api)
            count = 0


            for i in tqdm(range(1)):
                print("Searching Google Scholar Engine now please wait...")
                url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + query + '&as_ylo=' + _from_yr + '&as_yhi=' + _to_yr_ + '&btnG='

                response = client.get(url, headers={'User-agent': 'your bot 0.1'})

                if response.status_code != 200:
                    print("Request failed with stauts", response.status_code)
                    logger.writeError("Logging Erorr:" + str(response.status_code), None, _engine, logging_flag)

                else:
                    soup = BeautifulSoup(response.content, 'lxml')

                    #count no of records returned by google scholar
                    for item in soup.find_all('div', class_='gs_ab_st'):
                        rec =str(item.find_all('div', id='gs_ab_md')[0].get_text()).split(' ', 1)[1].replace(',', "").split(' ', 1)[0]

                        pages=1
                        if (_gs_pages!=0):
                            pages = pagination(_gs_pages)
                        else:
                            pages = pagination(rec)


                    #check if records are greater than 1000 or not
                    if(int(pages) > 100):
                        print("NOTE:Google Scholar returns data for max 1000 records irrespective of total records. Total No of total records found :", rec, "\n Fetching records details now...")

                        pages = 100
                        for i in range(pages):

                            url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + query + '&as_ylo=' + _from_yr + '&as_yhi=' + _to_yr_ + '&btnG=&start=' + str(i) + '0'

                            #response = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers)
                            response = client.get(url, headers={'User-agent': 'your bot 0.1'})
                            soup = BeautifulSoup(response.content, 'lxml')
                            ######## Find required attributes in the response object by checking tag [data-lid]'))
                            for item in soup.select('[data-lid]'):
                                try:
                                    try:
                                        if bool(item.select('.gs_rs')[0].get_text()):
                                            abstract = item.select('.gs_rs')[0].get_text()
                                        else:
                                            abstract = str(['No information found'])
                                    except:
                                        abstract = str(['No information found'])
                                        pass
                                    try:
                                        if bool(item.select('.gs_or_ggsm')):
                                            cc = \
                                            str(re.findall(r'\d+', str(item.select('.gs_fl')[1].get_text()))).split(',',
                                                                                                                    1)[
                                                0].replace('[', '')
                                        else:
                                            cc = \
                                            str(re.findall(r'\d+', str(item.select('.gs_fl')[0].get_text()))).split(',',
                                                                                                                    1)[
                                                0].replace('[', '')
                                    except:
                                        cc = str(['No information found'])
                                        pass
                                    try:
                                        if bool(item.select('.gs_ct1')):
                                            type = str(item.select('.gs_ct1')[0].get_text())
                                        else:
                                            type = str(['Research Article'])
                                    except:
                                        type = str(['No information found'])
                                        pass

                                    # response object
                                    resp_obj = {"entities": {"Search Engine": "Google Scholar",
                                                             "Attributes found": "Title, URLs, Authors, Cited count, Type, Published date, Abstract",
                                                             "items": [
                                                                 {"DOI": str(['No information found']),
                                                                  "Title": item.select('h3')[0].get_text(),
                                                                  "URLs": item.select('a')[0]['href'],
                                                                  "Authors": re.sub("[^A-Za-z]", " ",str(item.select('.gs_a')[0].get_text()).split('-', 1)[0]),
                                                                  "Publication Name": str(['No information found']),
                                                                  "ISSN": str(['No information found']),
                                                                  "Cited count": cc,
                                                                  "Affiliation": str(['No information found']),
                                                                  "Type": type,
                                                                  "Published date": str(re.findall(r'\d+', str(item.select('.gs_a')[0].get_text()))).strip(),
                                                                   "Abstract": abstract
                                                                  }
                                                             ]}}
                                    # append dict object data
                                    count += 1
                                    data.append(resp_obj)
                                except Exception as e:  # raise e
                                    pass
                                    exception_type, exception_object, exception_traceback = sys.exc_info()
                                    filename = exception_traceback.tb_frame.f_code.co_filename
                                    line_number = exception_traceback.tb_lineno
                                    logger.writeError(e, None, _engine, logging_flag, filename, line_number)

                    else:
                        for i in range(pages):

                            url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + query + '&as_ylo=' + _from_yr + '&as_yhi=' + _to_yr_ + '&btnG=&start=' + str(
                                i) + '0'


                            response = client.get(url, headers={'User-agent': 'your bot 0.1'})
                            if response.status_code != 200:
                                print("Request failed with stauts", response.status_code)
                                logger.writeError("Logging Erorr:" + str(response.status_code), None, _engine, logging_flag)

                            else:
                                soup = BeautifulSoup(response.content, 'lxml')

                            ######## Find required attributes in the response object by checking tag [data-lid]'))
                                for item in soup.select('[data-lid]'):
                                    try:
                                        try:
                                            if bool(item.select('.gs_rs')[0].get_text()):
                                                abstract=item.select('.gs_rs')[0].get_text()
                                            else:
                                                abstract = str(['No information found'])
                                        except:
                                            abstract = str(['No information found'])
                                            pass
                                        try:
                                            if bool(item.select('.gs_or_ggsm')):
                                                cc = str(re.findall(r'\d+', str(item.select('.gs_fl')[1].get_text()))).split(',', 1)[
                                                    0].replace('[', '')
                                            else:
                                                cc = str(re.findall(r'\d+', str(item.select('.gs_fl')[0].get_text()))).split(',', 1)[
                                                    0].replace('[', '')
                                        except:
                                            cc = str(['No information found'])
                                            pass
                                        try:
                                            if bool(item.select('.gs_ct1')):
                                                type = str(item.select('.gs_ct1')[0].get_text())
                                            else:
                                                type = str(['Research Article'])
                                        except:
                                            type = str(['No information found'])
                                            pass

                                        resp_obj = {"entities": {"Search Engine": "Google Scholar",
                                                                 "Attributes found": "Title, URLs, Authors, Cited count, Type, Published date, Abstract",
                                                                 "items": [
                                                                     {"DOI": str(['No information found']),
                                                                       "Title": item.select('h3')[0].get_text(),
                                                                      "URLs": item.select('a')[0]['href'],
                                                                      "Authors": re.sub("[^A-Za-z]", " ",str(item.select('.gs_a')[0].get_text()).split('-', 1)[0]),
                                                                      "Publication Name": str(['No information found']),
                                                                      "ISSN": str(['No information found']),
                                                                      "Cited count": cc,
                                                                      "Affiliation": str(['No information found']),
                                                                      "Type": type,
                                                                      "Published date": str(re.findall(r'\d+', str(item.select('.gs_a')[0].get_text()))).strip(),
                                                                       "Abstract": abstract
                                                                      }
                                                                 ]}}
                                        # append dict object data
                                        count += 1
                                        data.append(resp_obj)
                                    except Exception as e:  # raise e
                                        pass
                                        exception_type, exception_object, exception_traceback = sys.exc_info()
                                        filename = exception_traceback.tb_frame.f_code.co_filename
                                        line_number = exception_traceback.tb_lineno
                                        logger.writeError(e, None, _engine, logging_flag, filename, line_number)
                    time.sleep(1)

                    print(f'Finished with total {count} records returned.')
                    logger.writeRecords(query, None,_engine,rec,count,logging_flag)
                    return data

        # search without dates
        else:
            print("Searching Google Scholar Engine now please wait...")
            client = ScraperAPIClient(scrpr_api)
            count = 0
            for i in tqdm(range(1)):
                for i in range(pages):
                    # request url
                    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + query + '&btnG=&start=' + str(
                        i) + '0'
                    # response object
                    response = client.get(url, headers={'User-agent': 'your bot 0.1'})

                    if response.status_code != 200:
                        print("Request failed with stauts", response.status_code)
                        logger.writeError("Logging Erorr:" + str(response.status_code), None, _engine, logging_flag)


                    soup = BeautifulSoup(response.content, 'lxml')

                    ######## Find required attributes in the response object by checking tag [data-lid]'))
                    for item in soup.select('[data-lid]'):
                        try:

                            try:
                                if bool(item.select('.gs_rs')[0].get_text()):
                                    abstract = item.select('.gs_rs')[0].get_text()
                                else:
                                    abstract = str(['No information found'])
                            except:
                                abstract = str(['No information found'])
                                pass
                            try:
                                if bool(item.select('.gs_or_ggsm')):
                                    cc = \
                                    str(re.findall(r'\d+', str(item.select('.gs_fl')[1].get_text()))).split(',', 1)[
                                        0].replace('[', '')
                                else:
                                    cc = \
                                    str(re.findall(r'\d+', str(item.select('.gs_fl')[0].get_text()))).split(',', 1)[
                                        0].replace('[', '')
                            except:
                                cc = str(['No information found'])
                                pass
                            try:
                                if bool(item.select('.gs_ct1')):
                                    type = str(item.select('.gs_ct1')[0].get_text())
                                else:
                                    type = str(['Research Article'])
                            except:
                                type = str(['No information found'])
                                pass

                            resp_obj = {"entities": {"Search Engine": "Google Scholar",
                                                     "Attributes found": "Title, URLs, Authors, Cited count, Type, Published date, Abstract",
                                                     "items": [
                                                         { "DOI": str(['No information found']),
                                                           "Title": item.select('h3')[0].get_text(),
                                                            "URLs": item.select('a')[0]['href'],
                                                            "Authors": re.sub("[^A-Za-z]", " ",str(item.select('.gs_a')[0].get_text()).split('-', 1)[0]),
                                                            "Publication Name": str(['No information found']),
                                                            "ISSN": str(['No information found']),
                                                            "Cited count": cc,
                                                            "Affiliation": str(['No information found']),
                                                            "Type": type,
                                                            "Published date": str(re.findall(r'\d+', str(item.select('.gs_a')[0].get_text()))).strip(),
                                                             "Abstract": abstract
                                                          }
                                                     ]}}
                            # append dict object data
                            count += 1
                            data.append(resp_obj)
                        except Exception as e:  # raise e
                            pass
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            filename = exception_traceback.tb_frame.f_code.co_filename
                            line_number = exception_traceback.tb_lineno
                            logger.writeError(e, None, _engine, logging_flag, filename, line_number)
            time.sleep(1)

            print(f'Finished with total {count} records returned.')
            logger.writeRecords(query, None, _engine, rec, count, logging_flag)
            return data


### method to find no of pages for webscrapping engines
def pagination(records):
    page = 1
    def_record = 10
    if (records == 10):
        page = 1
    else:
        page = round((float(records) / def_record)) + 1

    return page