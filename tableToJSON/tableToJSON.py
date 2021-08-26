from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import json
import os
import numpy as np 
from datetime import datetime

def makeFormEntry(df, formName):
    formTable = df.loc[formName]
    entry = {
        "form_number": formName,
        "form_title": formTable['Title'] if isinstance(formTable, pd.Series) else formTable['Title'][0],
        "min_year": int(formTable['Revision Date']) if isinstance(formTable, pd.Series) else min(formTable['Revision Date']),
        "max_year": int(formTable['Revision Date']) if isinstance(formTable, pd.Series) else max(formTable['Revision Date'])
    }
    return entry

if __name__ == "__main__":
    if os.path.exists('data.csv') is True:
        irs_df = pd.read_csv('data.csv')
    else:
        print("Data file not found\nScraping table information")
        count = 0
        url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=' + str(count) + '&sortColumn=sortOrder&value=&criteria=&resultsPerPage=200&isDescending=false'

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        errorBlock = soup.find('div', {"class": "errorBlock"}) # Checker for while loop. Used to determine of webpage has a table of forms.
        df_list = []

        while errorBlock is None:
            df = pd.read_html(response.content)
            df = df[len(df)-1]
            df_list.append(df)

            count += 200
            url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=' + str(count) + '&sortColumn=sortOrder&value=&criteria=&resultsPerPage=200&isDescending=false'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            errorBlock = soup.find('div', {"class": "errorBlock"})

        irs_df = pd.concat(df_list)
        irs_df.to_csv('data.csv', index = False, header=True)

        print("Scraping complete")

    irs_df.set_index('Product Number', inplace=True)
    now = datetime.now()
    timestamp = now.strftime("%m%d%y%H%M%S")
    filepath = 'results/'
    filename = 'result_' + timestamp + '.json'
    result = []
    entry = {}

    for arg in sys.argv[1:]:
        print("Test case file:", arg)
        formList = [form.strip('\n') for form in open(arg, 'r').readlines()]
        wrongFormList = []

        for formName in formList:
            try:
                entry = makeFormEntry(irs_df, formName)
                result.append(entry)
            except KeyError as e:
                wrongFormList.append(formName)
        try:
            with open(filepath + filename, 'w') as outfile:
                json.dump(result, outfile)
        except FileNotFoundError:
            os.mkdir(filepath)
            with open(filepath + filename, 'w') as outfile:
                json.dump(result, outfile)
        
        if(len(wrongFormList) > 0):
            print("The following forms do not exist in the Prior Products Page.")
            for i in range(len(wrongFormList)):
                print("%d.)" % (i+1), wrongFormList[i])
        print("Test Complete\n")
    
    print("Task Complete")

