"""
  Module to search in all search engines with input parameters.

 * Copyright (C) Cape Breton University, Prof. Enayat Rajabi - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * without written consent from the owners.
 * Proprietary and confidential
 * Written by Chandrayog Yadav <chandrayog.2@gmail.com>, January 2021

"""

import sys
import json
from Logging import logger

from SearchEngines.GoogleScholar import search_googleScholar
from SearchEngines.MSAcademic import search_msAcademic
from SearchEngines.CORE import search_core
from SearchEngines.pubMed import search_pubMed
from SearchEngines.ACMLib import search_acmlibrary
from SearchEngines.PLOSOne import search_PlosOne
from SearchEngines.Academia import search_academia
from SearchEngines.ElseScopus import search_scopus
from SearchEngines.Springer import search_springer
from SearchEngines.SciDirect import search_sciDirect

# ignore warning messages
import warnings

warnings.filterwarnings('ignore')

# read config json file for API keys
with open("config.json") as json_data_file:
    data = json.load(json_data_file)

# scraper api key
scrpr_api = data['apikeys']['scrpr_api']

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


# dictionary object for data

# function for search engines
def search_allengines(query, headers, _pages, _gs_pages, _acm_pages, _els_pages, records, _title, _keyword, _abstract,
                      _search_yr, _from_yr, _to_yr_, logging_flag, data):
    # Search all engines
    try:
        '--- Engines for Title, Keyword and Abstract---'
        search_googleScholar(query, headers, _gs_pages, records, _title, _keyword, _abstract, scrpr_api, _from_yr, _to_yr_,
                             logging_flag, data)
        search_msAcademic(query, headers, _pages, records, _title, _keyword, _abstract, ms_api, _from_yr, _to_yr_,
                          logging_flag, data)
        search_core(query, headers, _pages, records, _title, _keyword, _abstract, core_api, _search_yr, logging_flag,
                    data)
        search_pubMed(query, headers, _pages, _title, _keyword, _abstract, _from_yr, _to_yr_, logging_flag, data)
        search_acmlibrary(query, headers, _acm_pages, records, _title, _keyword, _abstract, _from_yr, _to_yr_,
                          logging_flag, data)

        '--- Engines only for Keyword and Abstract ---'
        search_PlosOne(query, headers, _pages, records, _title, _keyword, _abstract, _from_yr, _to_yr_, logging_flag,
                       data)
        search_academia(query, headers, _pages, records, _title, _keyword, _abstract, _search_yr, logging_flag, data)
        search_scopus(query, headers, _els_pages, records, _title, _keyword, _abstract, scp_api, _from_yr, _to_yr_,
                      logging_flag, data)
        search_springer(query, headers, _pages, records, _title, _keyword, _abstract, spr_api, _search_yr, logging_flag,
                        data)
        search_sciDirect(query, headers, _pages, records, _title, _keyword, _abstract, sd1_api, sd2_api, _from_yr,
                         _to_yr_, logging_flag, data)
        return data
    except Exception as e:  # raise e
        pass
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        logger.writeError(e, None, "Search Exception :", logging_flag, filename, line_number)
