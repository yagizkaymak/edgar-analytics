# Table of Contents
1. [Author](README.md#author)
1. [Introduction](README.md#introduction)
1. [Introduction](README.md#dataset)
1. [Input](README.md#input)
1. [Output](README.md#output)
1. [Running The Code](README.md#running-the-code)
1. [Test Cases](README.md#test-cases)


## Author
This project developed by Yagiz Kaymak using Python 2.7 to solve Edgar Analytics coding challenge at Insight Data Science.
The code is also accessible online with the following link:
https://github.com/yagizkaymak/edgar-analytics

February 2019

## Introduction
Many investors, researchers, journalists and others use the Securities and Exchange Commission's (SEC's) Electronic Data Gathering, Analysis and Retrieval (EDGAR) system to retrieve financial documents, whether they are doing a deep dive into a particular company's financials or learning new information that a company has revealed through their filings.

This project uses EDGAR weblogs to identify the webpage visits of users as sessions. A session is identified as all webpage visits within a time interval.
It is assumed that each line of EDGAR weblogs represents a single web request for an EDGAR document that would be streamed into our application in real time.

Using the provided EDGAR weblogs data, the goal of this project is to output the user sessions. Each user session should include the duration and the number of documents requested during that visit, and then write the output to a file.

## Dataset
The SEC maintains EDGAR weblogs showing which IP addresses have accessed which documents for what company, and at what day and time this occurred.

A sample EDGAR weblog file is stored in "input" directory with the filename of "log.csv".
"log.csv" is a comma separated file with a header as its first line. These header fields are listed as follows:

*ip, date, time, zone, cik, accession, extention, code, size, idx, norefer, noagent, find, crawler, browser*

In this project we only use the following fields related to the challenge:

ip: identifies the IP address of the device requesting the data. While the SEC anonymizes the last three digits, it uses a consistent formula that allows you to assume that any two ip fields with the duplicate values are referring to the same IP address
date: date of the request (yyyy-mm-dd)
time: time of the request (hh:mm:ss)
cik: SEC Central Index Key
accession: SEC document accession number
extention: Value that helps determine the document being requested

It is assumed that the combination of cik, accession, and extention fields
uniquely identifies a single web page document request.


## Input
Two input files, "log.csv" and "inactivity_period.txt", exists in the "input" folder. As mentioned in Dataset section "log.csv" file
includes EDGAR weblogs in a comma separated format.
"inactivity_period.txt" file holde a single integer value denoting the period of inactivity (in seconds) that the
"edgar.analytics.py" script usee to identify a user session. The value can range from 1 to 86,400 (i.e., one second to 24 hours).

## Output
The output of this project is created as a text file, called "sessionization.txt", and stored in the "output" folder.
"sessionization.txt" includes the results with a comma separated format as follows:

IP address of the user exactly as found in log.csv
date and time of the first webpage request in the session (yyyy-mm-dd hh:mm:ss)
date and time of the last webpage request in the session (yyyy-mm-dd hh:mm:ss)
duration of the session in seconds
count of webpage requests during the session

Once your "edgar_analytics.py" script identifies the start and end of a session, it gathers the mentioned fields and write them out to a line in the output file, "sessionization.txt". The fields on each line are separated by a comma.


## Running The Code
In order to run the code provided in this repository, please use the shell script "run.sh" located in the root folder of this project.


## Test Cases
Six test cases can be found under "test" folder. "test_1" is the test case created by Insight Data Science. "test_x", where x denotes a number from 2 to 6, are different test cases created by Yagiz Kaymak.

To run the test cases please run "./run_tests.sh" bash script in the "test" folder.
