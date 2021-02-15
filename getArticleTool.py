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
sys.path.insert(1,os.getcwd())
#sys.path.insert(1,'Users/chandrayogyadav/Desktop/getArticleTool/')
from GoogleScholar import search_googleScholar
from MSAcademic import search_msAcademic
from CORE import search_core
from pubMed import search_pubMed
from ACMLib import search_acmlibrary
from PLOSOne import search_PlosOne
from Academia import search_academia
from ElseScopus import search_scopus
from Springer import search_springer
from SciDirect import search_sciDirect


# ignore warning messages
import warnings
warnings.filterwarnings('ignore')

### setting output display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Chrome/80.0.3987.149 Safari/601.3.9"

# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

# creating header for request
headers = {'User-Agent': USER_AGENT}

print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

curr_path=os.getcwd()
### read config json file for API keys
with open("config.json") as json_data_file:
    data = json.load(json_data_file)

#scraper api key
scrpr_api= data['apikeys']['scrpr_api']

# Microsoft API Key
ms_api = data['apikeys']['ms_api']

# CORE API key
core_api = data['apikeys']['core_api']

# Scopus API Key
scp_api = data['apikeys']['scp_api']

# ScienceDirect API Keys
# 1. Search All API Key
sd1_api = data['apikeys']['sd1_api']
# 2. Search Article attributes API Key
sd2_api = data['apikeys']['sd2_api']

# Springer API KEY
spr_api = data['apikeys']['spr_api']

#proxy value
#proxy_val = data['apikeys']['proxy_val']

## inital variables
search_query = ''
_title = False
_keyword = False
_abstract = False
_records = str(10)
_from_yr=''
_to_yr_=''
_gs_pages=''
# search keywords
# search_query = "Python"
records = str(0)
_search_yr =''
# Input var 1- Choose search engine option
print("Enter search engine number to lookup your article from list, input multiple numbers with space only:\n 0 ALL, 1 Google Scholar, 2 MS Academic, 3 CORE, 4 PubMed, 5 ACM Library, 6 PLOS ONE, 7 Academia, 8 Elsevier Scopus, 9 Springer, 10 Science Direct")
x = list(map(int, input("Enter a Search Engine value: ").split()))
if len(x)==0:
    print('Select search engine!')
    quit()

# Input var 2- Save output to a path option
print("Enter the path to save the JSON output file or enter to save on default location:\n E.g. (/Users/computername/Desktop/) ")
output_path = input("Path:")

# Input var 3- Dataframe output option
out=input("Do you also want Excel output? Y/N :").lower()

# Input var 4- No of records option
rec = str(input("Enter No of records to search(Minimum 10 or press enter):")).split()
if len(rec) != 0:
    records = rec[0]
    _gs_pages=records
else:
    records = str(10)
    _gs_pages=0

# Input 5- Search year parameter option
year1=str(input("Enter the FROM year (optional):")).strip()
if len(year1)!=0:
    _from_yr=year1
else:
    _from_yr=''

# Input 6- Search year parameter option
year2=str(input("Enter the TO year (optional):")).strip()
if len(year2)!=0:
    _to_yr_=year2
else:
    _to_yr_=''


# Input 7,8,9 - Title, Keyword, Abstract search options
print('Choose either Title, Keyword, or Abstract Info as options to search:')
param1 = str(input("Enter Keyword to search (if not then press enter to go to next option):")).capitalize().strip()
NoneType = type(None)
if param1 != '':
    _keyword = True
   #search_query = str(param1).replace('"', '')
    search_query= param1
else:
    param2 = str(input("Enter Abstract info to search (if not then press enter to go to next option):")).capitalize().strip()
    if param2 != '':
        _abstract = True
        search_query = str(param2).replace('"', '')
    else:
        param3 = str(input("Enter Full Title to search:")).capitalize().strip()
        if param3 != '':
            _title = True
            _param = str(param3).replace('"', '')
            search_query = urllib.parse.quote_plus(_param)
        else:
            print("Please provide some input!")

# create dictioanry object for output
data = []


# function for search engines
def search_engines(query, x):
    # Search all engines
        try:
            check_DateParams(_from_yr, _to_yr_)
            ## uncomment the search engine baesd your requiremnt
            if len(x)!=0:
                ### call the search fucntion for all
                try:
                     if 0 in x:

                        search_allengines(search_query)
                except Exception as e:  # raise e
                    pass  # print('error:', e)

                ###---Engines for Title, Keyword and Abstract---###
                try:
                    if 1 in x:
                       _pages = pagination(records)
                       search_googleScholar(query,headers,_gs_pages,records,_title,_keyword,_abstract, scrpr_api,_from_yr,_to_yr_, data)   # done
                except Exception as e:  # raise e
                    pass
                    #print('error:', e)
                try:
                   if 2 in x:
                       _pages = pagination(records)
                       search_msAcademic(query,headers, _pages,records,_title,_keyword,_abstract,ms_api,_from_yr,_to_yr_, data)  # done
                except Exception as e:  # raise e
                    #pass
                    print('error:', e)
                try:
                    if 3 in x:
                       _pages = pagination(records)
                       search_core(query,headers, _pages,records,_title,_keyword,_abstract,core_api,_search_yr, data)  # done
                except Exception as e:  # raise e
                    pass  # print('error:', e)
                try:
                    if 4 in x:
                       _pages = pagination(records)
                       search_pubMed(query,headers, _pages,_title,_keyword,_abstract,_from_yr,_to_yr_, data)  # done
                except Exception as e:  # raise e
                    #pass
                    print('error:', e)
                try:
                    if 5 in x:
                       _pages = pagination(records)
                       search_acmlibrary(query,headers, _pages,records,_title,_keyword,_abstract,_from_yr,_to_yr_, data)  # done
                except Exception as e:  # raise e
                     pass
                    #print('error:', e)

                ##---Engines only for Keyword and Abstract---###
                try:
                    if 6 in x:
                       _pages = pagination(records)
                       search_PlosOne(query,headers, _pages,records,_title,_keyword,_abstract,_from_yr,_to_yr_, data)  # done
                except Exception as e:  # raise e
                    #pass
                    print('error:', e)
                try:
                    if 7 in x:
                       _pages = pagination(records)
                       search_academia(query,headers, _pages,records,_title,_keyword,_abstract,_search_yr, data)
                except Exception as e:  # raise e
                    pass  # print('error:', e)
                try:
                    if 8 in x:
                       _pages = pagination(records)
                       search_scopus(query,headers, _pages,records,_title,_keyword,_abstract,scp_api,_from_yr,_to_yr_, data)  # done
                except Exception as e:  # raise e
                    pass  # print('error:', e)

                try:
                    if 9 in x:
                       _pages = pagination(records)
                       search_springer(query,headers, _pages,records,_title,_keyword,_abstract,spr_api,_search_yr, data)  # done
                except Exception as e:  # raise e
                    pass  # print('error:', e)

                try:
                    if 10 in x:
                      _pages = pagination(records)
                      search_sciDirect(query,headers, _pages,records,_title,_keyword,_abstract,sd1_api, sd2_api,_from_yr,_to_yr_, data)
                except Exception as e:  # raise e
                    pass  # print('error:', e)

            else:
                print('Select search engine!')
                exit

        except Exception as e:  # raise e
            pass  # print('error:', e)

# function for search engines
def search_allengines(query):
    # Search all engines
        try:
            try:
            ###---Engines for Title, Keyword and Abstract---###
                    _pages = pagination(records)
                    search_googleScholar(query, headers, _pages, records, _title, _keyword, _abstract, scrpr_api,_from_yr,_to_yr_, data)  # done
            except Exception as e:  # raise e
                pass  # print('error:', e)
            try:
                    _pages = pagination(records)
                    search_msAcademic(query, headers, _pages, records, _title, _keyword, _abstract, ms_api,_from_yr,_to_yr_,data)  # done
            except Exception as e:  # raise e
                 pass
                #print('error:', e)
            try:
                    _pages = pagination(records)
                    search_core(query, headers, _pages, records, _title, _keyword, _abstract, core_api,_search_yr, data)  # done
            except Exception as e:  # raise e
                pass  # print('error:', e)
            try:
                    _pages = pagination(records)
                    search_pubMed(query, headers, _pages, _title, _keyword, _abstract, _from_yr,_to_yr_,data)  # done
            except Exception as e:  # raise e
                 pass
                #print('error:', e)
            try:
                    _pages = pagination(records)
                    search_acmlibrary(query, headers, _pages, records, _title, _keyword, _abstract,_from_yr,_to_yr_, data)  # done
            except Exception as e:  # raise e
                pass
                # print('error:', e)

            ##---Engines only for Keyword and Abstract---###
            try:
                    _pages = pagination(records)
                    search_PlosOne(query, headers, _pages, records, _title, _keyword, _abstract, _from_yr,_to_yr_,data)  # done
            except Exception as e:  # raise e
                pass
                #print('error:', e)
            try:
                    _pages = pagination(records)
                    search_academia(query, headers, _pages, records, _title, _keyword, _abstract,_search_yr, data)
            except Exception as e:  # raise e
                pass  # print('error:', e)
            try:
                    _pages = pagination(records)
                    search_scopus(query, headers, _pages, records, _title, _keyword, _abstract, scp_api,_from_yr,_to_yr_, data)  # done
            except Exception as e:  # raise e
                pass  # print('error:', e)

            try:
                    _pages = pagination(records)
                    search_springer(query, headers, _pages, records, _title, _keyword, _abstract, spr_api,_search_yr, data)  # done
            except Exception as e:  # raise e
                pass  # print('error:', e)

            try:
                    _pages = pagination(records)
                    search_sciDirect(query, headers, _pages, records, _title, _keyword, _abstract, sd1_api, sd2_api,_from_yr,_to_yr_, data)
            except Exception as e:  # raise e
                pass  # print('error:', e)

        except Exception as e:  # raise e
            pass  # print('error:', e)

### method to find no of pages for webscrapping engines
def pagination(records):
    page = 1
    def_record = 10
    if (records == 10):
        page = 1
    else:
        page = round((float(records) / def_record))
    return page

def check_DateParams(_from, _to):
    if(len(_from_yr) and not(_to)):
        print("Both years search options either entered or leave blank!")
        quit()
    elif(not(_from_yr) and len(_to)):
        print("Both years search options either entered or leave blank!")
        quit()
    ###------Main Call to search-------####
### Call search engines
search_engines(search_query,x)
# print the dict output
print(data)


### Function to save JSON output to a file
def save_output(output):
    if output_path:
        #writepath = "/Users/chandrayogyadav/Desktop/data.json"  ### define path to you desired location for file
        writepath = output_path
        mode = 'a' if os.path.exists(writepath) else 'w+'
        with open(writepath+"/data.json", mode) as f:
            f.close()
            f.write(output)
    else:
        try:
            if os.path.exists("data.json"):
                os.remove("data.json")
                f = open("data.json", "x")
                f.write(output)
                f.close()
            else:
                f = open("data.json", "x")
                f.write(output)
                f.close()
        except Exception as e:  # raise e
            #pass
             print("Output file:", e)

# check if the output received or not then create further dataframe
if bool(data):
    # convert dict object into JSON:
    json_output = json.dumps(data, indent=2, sort_keys=True)

    # print(json_output)
    save_output(json_output)
    if out == 'y':
        #convert json into datafrme
        df = pd.json_normalize(data)

        #####-----creating final output------#####
        # drop nested columns and keep 1st attribute
        df.drop(["entities.items"], axis=1, inplace=True)

        # create required temp objets
        d1 = pd.DataFrame([])
        result = pd.DataFrame([])

        # split nested attributes into separate columns and stored output in a temp object d1
        i = 0
        for i in range(0, len(data)):
            d = pd.json_normalize(data[i]['entities']['items'])
            d1 = d1.append(d, True)

            # concatenate both dataframes into one
            result = pd.concat([df, d1], axis=1)
            # print('Output in Dataframe format with columns ')
            # print(result)
        if os.path.exists("search_results.xlsx"):
            # save final output to csv
            result.to_excel('search_results.xlsx', index=False)
            print('Spreadsheet saved.')
        else:
            result.to_excel('search_results.xlsx', index=False)
            print('Spreadsheet saved.')
            # print(result)
    else:
        exit
else:
    print("No record found!")
