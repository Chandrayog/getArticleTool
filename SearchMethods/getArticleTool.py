"""
  Master module to call all the search methods based on input parameters.

 * Copyright (C) Cape Breton University, Prof. Enayat Rajabi - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * without written consent from the owners.
 * Proprietary and confidential
 * Written by Chandrayog Yadav <chandrayog.2@gmail.com>, January 2021

"""

import pandas as pd
import sys
from Logging import logger

from InputArgs.ParseInput import parseInputFunc
from SearchMethods import searchAllEngines
from SearchMethods import searchSpecificEngine
from OutPut import SaveOutput

# ignore warning messages
import warnings

warnings.filterwarnings('ignore')

# setting output display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

# Input var 1- Choose search engine option
print("Enter search engine number to lookup your article from list, input multiple numbers with space only:\n 0 ALL, "
      "1 Google Scholar, 2 MS Academic, 3 CORE, 4 PubMed, 5 ACM Library, 6 PLOS ONE, 7 Academia, 8 Elsevier Scopus, "
      "9 Springer, 10 Science Direct")

x = list(map(int, input("Enter a Search Engine value: ").split()))
if len(x) == 0:
    print('Select search engine!')
    quit()

# Input Variables
query, headers, _pages, _gs_pages, _acm_pages, _els_pages, records, _title, _keyword, _abstract, _search_yr, _from_yr, _to_yr_, logging_flag, output_path, out = parseInputFunc()

# Dictionary for output
data = []


# function for search engines
def search_engines(x, data=None):
    # Call Search Modules
    try:
        if len(x) != 0:

            # call the search function for all
            try:
                if 0 in x:
                    data = searchAllEngines.search_allengines(query, headers, _pages, _gs_pages, _acm_pages, _els_pages,
                                                              records, _title, _keyword, _abstract, _search_yr,
                                                              _from_yr, _to_yr_, logging_flag, data)
                    SaveOutput.saveOutput(data, out, output_path)
            except Exception as e:  # raise e
                pass  # print('error:', e)

            try:
                if 0 not in x:
                    data = searchSpecificEngine.search_engines(x, query, headers, _pages, _gs_pages, _acm_pages,
                                                               _els_pages, records, _title, _keyword, _abstract,
                                                               _search_yr, _from_yr, _to_yr_, logging_flag, data)
                    SaveOutput.saveOutput(data, out, output_path)
            except Exception as e:  # raise e
                pass
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                logger.writeError(e, None, "Google Scholar", logging_flag, filename, line_number)
        else:
            print('Select search engine!')
            exit

    except Exception as e:  # raise e
        pass
        # print('error:', e)


# ### Call search engines
search_engines(x, data)
