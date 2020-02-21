# Edgar Analytics Coding Challenge

## Table of Contents

1. [Purpose](https://github.com/yohn-dezmon/insight-data-eng-cc#purpose)
2. [Data Processing](https://github.com/yohn-dezmon/insight-data-eng-cc#data-processing)
3. [Directory Structure](https://github.com/yohn-dezmon/insight-data-eng-cc#directory-structure)
4. [Instructions to Run Project](https://github.com/yohn-dezmon/insight-data-eng-cc#instructions)

## Purpose:  
The Electronic Data Gathering, Analysis and Retrieval (EDGAR) is used by
journalists, investors, and others within the financial domain to retrieve
financial documents. The purpose of this application is to ingest streamed EDGAR
weblog data in order to determine how long certain users are staying on EDGAR,
and which documents they are accessing.


## Data Processing:
I ingested the data using Python's csv library from within the standard Python  
library. I transformed the data using a combination of lists and dictionaries.  
The data was aggregated based upon IP addresses, and the number of visits
within a given inactivity period given by the ```inactivity_period.txt``` file
within the input directory.

Since the data is ingested on a row-by-row basis from the input csv file,
each row has a corresponding time stamp.

Within my application there is a dictionary that stores only IPs with currently
active sessions. The session activity is determined by comparing the most recent
time of a request from that IP to the current timestamp

 If the IP for this row is already
in the dictionary storing


## Directory Structure:


## Instructions:

### Running edgarSessions.py


### Running Unit Tests


### Python Standard Library

All modules used were within Python's standard library.  
