from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import os
import numpy as np 
    
def getFormPDF(df, formName, year):
    formTable = df.loc[formName]
    filepath = formName + '/'
    filename = formName + ' - ' + str(year) + '.pdf'
    if year in list(formTable['Revision Date']):
        response = requests.get(formTable.loc[formTable['Revision Date'] == year]['PDF'].values[0])
        try:
            with open(filepath + filename, 'wb') as outFile:
                outFile.write(response.content)
        except FileNotFoundError:
            os.mkdir(filepath)
            with open(filepath + filename, 'wb') as outFile:
                outFile.write(response.content)
        print("Tax form download successful:", filename)
    else:
        print(formName, "for year", year, "does not exist.")

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
        formNameColumn = soup.find_all('td', {"class": "LeftCellSpacer"}) # List of elements containing the <td class="LeftCellSpacer"> tag (the first column named 'Product Number' from the table) 
        df_list = []

        while errorBlock is None:
            hrefList = [link.find('a')['href'] for link in formNameColumn] # List of form PDF links grabbed from <a> tag with href attribute
            df = pd.read_html(response.content)
            df = df[len(df)-1]
            df['PDF'] = hrefList
            df_list.append(df)


            count += 200
            url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=' + str(count) + '&sortColumn=sortOrder&value=&criteria=&resultsPerPage=200&isDescending=false'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            errorBlock = soup.find('div', {"class": "errorBlock"})
            formNameColumn = soup.find_all('td', {"class": "LeftCellSpacer"})


        irs_df = pd.concat(df_list)
        irs_df.to_csv('data.csv', index = False, header=True)

        print("Scraping complete")

    irs_df.set_index('Product Number', inplace=True)

    formName = sys.argv[1]
    yearRange = range(int(sys.argv[2]), int(sys.argv[3])+1)

    print("Downloading Files")
    for year in yearRange:
        try:
            getFormPDF(irs_df, formName, year)
        except KeyError:
            print(formName, "does not exist")
            break
        
    print("\nTask Complete")