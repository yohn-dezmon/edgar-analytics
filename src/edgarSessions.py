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
        self.previous_datetime = ""


    def convert_to_datetime(self, date, time):
        """This method takes either the date or time from each row and converts it to a
        datetime object. It returns None if there is an error in the converison.
        """
        try:
            # This will need to be modified for different data sets having
            # different date formats.
            datetime_str = date+" "+time
            date_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

        except ValueError as ve:
            print(ve)
            return ''
        return date_time

    def write_to_file(self, path_to_output, list_row):
        with open(path_to_output, 'a+') as output:
            edgar_writer = csv.writer(output, delimiter=',', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
            # row[4] is delta and is excluded
            edgar_writer.writerow(list_row)

    def check_for_session(self, session_dict, inactiv_secs, datetime,
                            path_to_output):
        keys_to_be_deleted = []
        for key in session_dict:
            # check if current time - most recent time > 2
            # if true, return [key/ip,value[0],value[2]
            values = session_dict[key]
            mostrecent = values[1]
            # if current time - most recent is > inactivity_period
            # or if

            diff_seconds = (datetime - mostrecent).seconds
            if diff_seconds > inactiv_secs:
                duration = (values[1] - values[0]).seconds + 1
                # ip, start, stop, duration, number of requests
                row_for_output = [key,values[0],values[1], duration, values[2]]
                self.write_to_file(path_to_output, row_for_output)
                keys_to_be_deleted.append(key)

        for key in keys_to_be_deleted: del session_dict[key]
        keys_to_be_deleted.clear()

    def main(self, path_to_input, path_to_inactiv, path_to_output):

        session_dict = {}

        with open(path_to_inactiv) as text_file:
            csv_reader = csv.reader(text_file, delimiter=',')


            for line in csv_reader:
                inactiv_secs = int(line[0])

                if inactiv_secs == "":
                    return "No inactivity period provided"

        with open(path_to_input) as input_file:
            csv_reader = csv.DictReader(input_file, delimiter=',')

            for row in csv_reader:
#           sample headers: ['ip', 'date', 'time', 'zone', 'cik', 'accession', 'extention', 'code', 'size', 'idx', 'norefer', 'noagent',
# 'find', 'crawler', 'browser']

                # extracting values from each row
                ip = row['ip']
                # cik SEC Central Index Key
                cik = row['cik']
                # SEC document accession number
                accession = row['accession']
                # helps determine the document being requested
                extention = row['extention']


                datetime = self.convert_to_datetime(row['date'], row['time'])
                if datetime == None:
                    print(f'Row with invalid date format: {row}')
                    continue

                if ip == '' or cik == '' or accession == '' or extention == '':
                    print(f'Null values in this row: {row}')
                    continue

                # Check for missing values from the row.
                if len(row) < 15:
                    print(f'Row missing values: {row}')
                    continue
                elif len(row) > 15:
                    print(f'Too many values: {row}')
                    continue

                # count of the IP during the session
                count = 1

                if ip in session_dict:
                    # rewrite it to the value
                    values = session_dict[ip]
                    # most recent time for the ip
                    most_recent_time = values[1]

                    # only check for session inactivity if datetime > most_recent_time
                    if self.previous_datetime != "" and datetime > most_recent_time:
                        self.check_for_session(session_dict, inactiv_secs, datetime,
                                                path_to_output)
                    self.previous_datetime = datetime

                    # increase count
                    count = values[2]
                    count += 1
                    values[2] = count
                    # update most recent time
                    values[1] = datetime

                if ip not in session_dict:
                    # value[0] = initial datetime for session
                    # value[1] =  most recent datetime for session
                    # value[2] = count
                    session_dict[ip] = [datetime, datetime, count]

        for key in session_dict:
            values = session_dict[key]
            duration = (values[1] - values[0]).seconds + 1
            row_for_output = [key,values[0],values[1], duration, values[2]]
            self.write_to_file(path_to_output, row_for_output)
        




if __name__ == '__main__':
    # ba stands for border analytics
    edgarAnalytics = EdgarAnalytics()

    if len(argv) == 4:
        input = argv[1]
        inactiv_period = argv[2]
        output = argv[3]
        try:
            os.remove(output)
        except:
            pass
    else:
        raise IncorrectCommandLine(argv)


    # path_to_output = parentPath+'/output/report.csv'
    # path_to_input = parentPath+'/input/log.csv'

    edgarAnalytics.main(input, inactiv_period, output)
