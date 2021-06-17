"""
  Module for formatting and saving the output returend by the tool.

 * Copyright (C) Cape Breton University, Prof. Enayat Rajabi - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * without written consent from the owners.
 * Proprietary and confidential
 * Written by Chandrayog Yadav <chandrayog.2@gmail.com>, January 2021

"""

import os
import json
import pandas as pd


### Function to save JSON output to a file
def save_ToJSON(output, output_path):
    print(output)
    if output_path:
        writepath = output_path
        mode = 'a' if os.path.exists(writepath) else 'w+'
        with open(writepath + "/data.json", mode) as f:
            f.close()
            f.write(output)
            print('JSON file saved!')
    else:
        try:
            if os.path.exists("./OutPut/data.json"):
                os.remove("./OutPut/data.json")
                f = open("./OutPut/data.json", "x")
                f.write(output)
                f.close()
                print('JSON file saved!')
            else:
                f = open("./OutPut/data.json", "x")
                f.write(output)
                f.close()
                print('JSON file saved!')
        except Exception as e:  # raise e
            # pass
            print("Output file:", e)


def saveOutput(data, out, output_path):
    # check if the output received or not then create further dataframe
    if bool(data):
        # convert dict object into JSON:
        json_output = json.dumps(data, indent=2, sort_keys=True)

        # print(json_output)
        save_ToJSON(json_output, output_path)
        if out == 'y':
            # convert json into dataframe
            df = pd.json_normalize(data)

            '-----creating final output------'
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
            if os.path.exists("./OutPut/search_results.xlsx"):
                # save final output to csv
                result.to_excel('./OutPut/search_results.xlsx', index=False)
                print('Spreadsheet saved.')
            else:
                result.to_excel('./OutPut/search_results.xlsx', index=False)
                print('Spreadsheet saved.')
                # print(result)
        else:
            exit
    else:
        print("No data saved in file!")
