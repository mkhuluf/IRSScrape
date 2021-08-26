# IRSScrape

## Background
This is a take home interview problem that I did for a fintech company looking into hiring Software Engineers for their Integrations time. For the interview, I was required to write two tasks that searches through the Prior Year Products webpage from the IRS website, https://apps.irs.gov/, and do the following:
1. Taking a list of tax forms, generating a JSON object with a list of dictionary objects with information regarding the tax forms including
	- Tax form name
	- Tax form description
	- Minimum and maximum years available for download
2. Taking a tax form name and a range of years, download all available PDF forms and save it into a directory based on the tax form name

## Requirements
- Python 3.9.5
- Python Libraries
	- beautifulsoup4 - 4.9.3
	- requests - 2.25.1
	- pandas - 1.2.4
	- numpy - 1.20.3
	- lxml - 4.6.3

## Instructions
1. Run the requirements.txt file in the folder "Pinwheel_Interview_Problem"
```cmd
pip install -r requirements.txt
```
2. Task 1: tableToJSON
	- Run the first task of the problem from the folder "Pinwheel_Interview_Problem/tableToJSON". The script tableToJSON.py takes in command line arguments as input parameters where the arguments are text files for test cases which are located in the folder "Pinwheel_Interview_Problem/tableToJSON/test_cases". 
	- After running the script, the JSON object is saved in the folder "Pinwheel_Interview_Problem/tableToJSON/results". If a list has an incorrect tax form name, the script with print out the incorrect forms for review. 
	
	```cmd
		python tableToJSON.py [test case text file] [test case text file] ...
	```
	 Example
	```cmd
		$ python tableToJSON.py "test_cases/test1.txt"
		Test case file: test_cases/test1.txt
		Test Complete

		Task Complete
	```
	
	```cmd		
		$ python tableToJSON.py "test_cases/test2.txt" "test_cases/test6.txt"
		Test case file: test_cases/test2.txt
		Test Complete

		Test case file: test_cases/test6.txt
		The following forms do not exist in the Prior Products Page.
		1.) Form W-111211
		2.) Form 990-T (Schedule RR)
		3.) Form 392B2
		4.) Form 439999
		Test Complete

		Task Complete		
	```
	
	3. Task 2: formPDFDownload
		- Run the second task of the problem from the folder "Pinwheel_Interview_problem/formPDFDownload". The script, formPDFDownload.py, takes in command line arguments as input parameters where the arguements are the following:
			- The tax form name
			- Start year for range
			- End year for range
		- After running the script, the tax forms are downloaded into a folder named after the tax form name. The script also prints the files that don't exist within the year range or in the website.

	```cmd
		python formPDFDownload.py [tax form name] [startYear] [endYear]
	```
	 Example
	```cmd
		$ python formPDFDownload.py "Form W-2" 2017 2021
		Downloading Files
		Tax form download successful: Form W-2 - 2017.pdf
		Tax form download successful: Form W-2 - 2018.pdf
		Tax form download successful: Form W-2 - 2019.pdf
		Tax form download successful: Form W-2 - 2020.pdf
		Tax form download successful: Form W-2 - 2021.pdf

		Task Complete
	```
	
	```cmd
		$ python formPDFDownload.py "Form 1040" 2020 2022
		Downloading Files
		Tax form download successful: Form 1040 - 2020.pdf
		Form 1040 for year 2021 does not exist.
		Form 1040 for year 2022 does not exist.

		Task Complete
	```
	
	```cmd
		$ python formPDFDownload.py "Form B-14" 2001 2010
		Downloading Files
		Form B-14 does not exist

		Task Complete
	```
	
	
