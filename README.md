# Edgar Analytics Coding Challenge

## Table of Contents

1. [Purpose](https://github.com/yohn-dezmon/edgar-analytics#purpose)
2. [Definitions For Data Model](https://github.com/yohn-dezmon/edgar-analytics#definitions-for-data-model)
3. [SEC Weblog Schema](https://github.com/yohn-dezmon/edgar-analytics#sec-weblog-schema)
4. [Data Processing](https://github.com/yohn-dezmon/edgar-analytics#data-processing)
5. [Output File](https://github.com/yohn-dezmon/edgar-analytics#output-file)
6. [Directory Structure](https://github.com/yohn-dezmon/edgar-analytics#directory-structure)
7. [Instructions](https://github.com/yohn-dezmon/edgar-analytics#instructions)

## Purpose:  
The Electronic Data Gathering, Analysis and Retrieval (EDGAR) is used by
journalists, investors, and others within the financial domain to retrieve
financial documents. The purpose of this application is to ingest streamed EDGAR
weblog data in order to determine how long certain users are staying on EDGAR,
and how many documents they are accessing within that period.


## Definitions For Data Model:

Each line of the incoming data represents a single web request for an EDGAR  
document. The IP address uniquely identifies a given user.

**Session** = Sessions are specific to a particular user (IP), a session begins
when a user requests one or more documents. The session continues so long
as the user continues to request documents within the inactivity period.
**Inactivity Period** = A period of time in seconds , supplied by the the  ```inactivity_period.txt``` file within the input directory. If a user makes
a request and does not make another request after the entire inactivity period  
has passed, that user session is considered complete.
**EndOfInput** = When you reach the end of the input file, ```log.csv```,  
the last timestamp of the log.csv should signal the end of all current
sessions.

If the same user requests another document after their previous session has
ended, this is considered the start of a new session.

The moment a user's session has ended, that session will be output to an
output file, ```sessionization.txt``` within the output directory.

## SEC Weblog Schema:

**ip** --> any two ip fields with duplicate values are referring to the same IP address  
**date** --> date of the request (yyyy-mm-dd)  
**time** --> time of the request (hh:mm:ss)  
**cik** --> SEC Central Index Key  
**accession** --> SEC document accession number  
**extension** --> value that helps determine the document being requested  

The combination of cik, accession, and extension fields uniquely identifies a single web page document request. These fields can contain numbers, letters, hyphens, periods or other characters.

The first line of the ```log.csv``` is a HEADER.

## Data Processing:
I ingested the data using Python's csv library from within the standard Python library.  
Within my application there is a dictionary that stores only IPs with currently
active sessions. The session activity is determined by comparing the most recent
time of a request from that IP to the current timestamp. If the difference
in time in seconds between these two times is greater than the inactivity period  
then the the key value pair is returned and output to the ```sessionization.txt```  
file. Otherwise each time a new row with the same IP was found, as long as it was still   within the session, the count of documents requested was increased by one.

Dictionary Structure:
key: IP address
values: an array list of start time, most recent time, and count of documents requested  
within the session.


## Output file:
The output file is ```sessionization.txt``` within the output direcotry.
There is no header for this file, and the output consists of the following columns:

**IP**: The IP of the user making the document request
**DateTime - Start**: The time of the first document request, initiates the session
(yyyy-mm-dd hh:mm:ss)
**DateTime - Stop**: Most recent document request within the session
(yyyy-mm-dd hh:mm:ss)
**Duration**: Duration of the session in seconds
**Count**: Count of webpage requests during the session

If the program detects multiple user sessions ending at the same time, it will
write the results to the sessionization.txt output file in the same order as the  
user's first request for that session appeared in the log.csv file.


## Directory Structure:

```
.
├── README.md
├── input
│   ├── inactivity_period.txt
│   └── log.csv
├── insight_testsuite
│   ├── results.txt
│   ├── run_tests.sh
│   ├── temp
│   │   ├── input
│   │   │   ├── inactivity_period.txt
│   │   │   └── log.csv
│   │   ├── output
│   │   │   └── sessionization.txt
│   │   ├── run.sh
│   │   └── src
│   │       ├── __pycache__
│   │       │   └── testing_argv.cpython-38.pyc
│   │       ├── edgarSessions.py
│   │       ├── run.sh
│   │       └── testing_argv.py
│   └── tests
│       └── test_1
│           ├── README.md
│           ├── input
│           │   ├── inactivity_period.txt
│           │   └── log.csv
│           └── output
│               └── sessionization.txt
├── output
│   └── sessionization.txt
├── run.sh
└── src
    ├── __pycache__
    │   └── testing_argv.cpython-38.pyc
    ├── edgarSessions.py
    ├── run.sh
    └── testing_argv.py

```

## Instructions:

You can run the application by either using the ```./run.sh``` file in the root  
folder of the repository or to run unit tests, cd to insight_testsuite and  
run ```./run_tests.sh```.

### Python Standard Library

All modules used were within Python's standard library.  
