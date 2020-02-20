import csv
import sys
import os
from datetime import datetime
import pdb

from sys import argv
from testing_argv import IncorrectCommandLine

# /Users/HomeFolder/projects/edgar-analytics/src/edgarSessions.py
absPath = os.path.abspath(__file__)
# /Users/HomeFolder/projects/edgar-analytics/src
srcPath = os.path.dirname(absPath)
# /Users/HomeFolder/projects/edgar-analytics
parentPath = os.path.dirname(srcPath)

class EdgarAnalytics(object):
    """ """

    def __init__(self):
        pass

    def convert_to_datetime(self, date, date_or_time):
        """This method takes either the date or time from each row and converts it to a
        datetime object. It returns None if there is an error in the converison.
        """
        try:
            # This will need to be modified for different data sets having
            # different date formats.
            if date_or_time == "date":
                date_time = datetime.strptime(date, '%Y-%m-%d')
            elif date_or_time == "time":
                date_time = datetime.strptime(date, '%H:%M:%S')
        except ValueError as ve:
            print(ve)
            return ''
        return date_time

    def main(self, path_to_input, path_to_inactiv, path_to_output):

        with open(path_to_inactiv) as text_file:
            csv_reader = csv.reader(text_file, delimiter=',')



            for line in csv_reader:
                inactiv_secs = line[0]

                if inactiv_secs == "":
                    return "No inactivity period provided"

        with open(path_to_input) as input_file:
            csv_reader = csv.reader(input_file, delimiter=',')
            

            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # skip column headers
                    line_count += 1
                else:
                    # extracting values from each row
                    # ip =
                    ip = row[0]
                    # cik SEC Central Index Key
                    cik = row[4]
                    # SEC document accession number
                    accession = row[5]
                    # helps determine the document being requested
                    extension = row[6]

                    date = self.convert_to_datetime(row[1], "date")
                    time = self.convert_to_datetime(row[2], "time")
                    if date == None or time == None:
                        print(f'Row with invalid date format: {row}')
                        continue

                    if ip == '' or cik == '' or accession == '' or extension == '':
                        print(f'Null values in this row: {row}')
                        continue

                    # Check for missing values from the row.
                    if len(row) < 15:
                        print(f'Row missing values: {row}')
                        continue
                    elif len(row) > 15:
                        print(f'Too many values: {row}')
                        continue




if __name__ == '__main__':
    # ba stands for border analytics
    edgarAnalytics = EdgarAnalytics()

    if len(argv) == 4:
        input = argv[1]
        inactiv_period = argv[2]
        output = argv[3]
    else:
        raise IncorrectCommandLine(argv)


    # path_to_output = parentPath+'/output/report.csv'
    # path_to_input = parentPath+'/input/log.csv'

    edgarAnalytics.main(input, inactiv_period, output)
