"""
  Module for parsing the input parameters from console.

 * Copyright (C) Cape Breton University, Prof. Enayat Rajabi - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * without written consent from the owners.
 * Proprietary and confidential
 * Written by Chandrayog Yadav <chandrayog.2@gmail.com>, January 2021

"""


import os
import urllib

def parseInputFunc():
    print("Path at terminal when executing this file")
    print(os.getcwd() + "\n")
    curr_path = os.getcwd()

    # initial variables
    search_query = ''
    _title = False
    _keyword = False
    _abstract = False
    _records = str(10)
    _from_yr = ''
    _to_yr_ = ''
    _gs_pages = ''
    records = str(0)
    _search_yr = ''

    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) " \
                 "Version/9.0.2 Chrome/80.0.3987.149 Safari/601.3.9 "

    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, " \
                        "like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36 "

    # creating header for request
    headers = {'User-Agent': USER_AGENT}

    # Input var 2- Save output to a path option
    print(
        "Enter the path to save the JSON output file or enter to save on default location:\n E.g. ("
        "/Users/computername/Desktop/) ")
    output_path = input("Path:")

    # Input var 3- Dataframe output option
    out = input("Do you also want Excel output? Y/N :").lower()

    # Input var 4- Dataframe output option
    logging_flag = input("Do you also want Logging? Y/N :").lower()

    # Input var 5- No of records option
    rec = str(input("Enter No of records to search(Minimum 10 or press enter):")).split()
    if len(rec) != 0:
        records = rec[0]
        _gs_pages = records
        _acm_pages = records
        _els_pages = records

    else:
        records = str(10)
        _gs_pages = 0
        _acm_pages = 0
        _els_pages = 0

    # Input 6- Search year parameter option
    year1 = str(input("Enter the FROM year (optional):")).strip()
    if len(year1) != 0:
        _from_yr = year1
    else:
        _from_yr = ''

    # Input 7- Search year parameter option
    year2 = str(input("Enter the TO year (optional):")).strip()
    if len(year2) != 0:
        _to_yr_ = year2
    else:
        _to_yr_ = ''

    # Input 8,9,10 - Title, Keyword, Abstract search options

    print('Choose either Title, Keyword, or Abstract Info as options to search:')
    param1 = str(input("Enter Keyword to search (if not then press enter to go to next option):")).capitalize().strip()
    NoneType = type(None)
    if param1 != '':
        _keyword = True
        # search_query = str(param1).replace('"', '')
        search_query = param1
    else:
        param2 = str(
            input("Enter Abstract info to search (if not then press enter to go to next option):")).capitalize().strip()
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

    check_DateParams(_from_yr, _to_yr_)
    _pages = pagination(_records)
    return search_query, headers, _pages, _gs_pages, _acm_pages, _els_pages, records, _title, _keyword, _abstract, _search_yr, _from_yr, _to_yr_, logging_flag, output_path, out


def check_DateParams(_from, _to):
    if len(_from) and not (_to):
        print("Search years options either entered wrong or left blank!")
        quit()
    elif not (_from) and len(_to):
        print("Search years options either wrong or left blank!")
        quit()


# method to find no of pages for webscrapping engines
def pagination(records):
    page = 1
    def_record = 10
    if records == 10:
        page = 1
    else:
        page = round((float(records) / def_record))
    return page
