"""
This is the code that reads the EDGAR weblogs and inactivity_time.txt,
detects the sessions and outputs the results in 'sessionization.txt' file

Author: Yagiz Kaymak
February, 2019
"""

import csv
import date_utils as du
import operator
import sys

TIMESTAMP_FORMAT = "YYYY-mm-dd HH:MM:SS"

def read_inactivity_time(filename):
    """ Reads the incactivity_time stored in 'inactivity_time.txt' file """
    with open(filename,'r') as f:
        line = f.readline()
        inactivity_time = line.rstrip('\n')
        return inactivity_time


def read_weblog(filename):
    """
    Reads the log file (log.csv) and extract the related fields,
    such as IP address, access date, access time.
    Extracted fields are returned as a list
    """
    line_number = 0
    weblog_list = list()

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if(line_number > 0):
                weblog_list.append([row[0], row[1], row[2]]) # IP, access date, access time
            line_number = line_number + 1
        return weblog_list


def check_for_inactive_sessions(event_log_dic, date_time, inactivity_time, sessinization_file_handler):
    """
    Checks if there is an inactive session and returns the updated IP dictionary (i.e., event_log_dic).
    Input: IP dictionary so far, current date time, inactivity time, sessinization file handler to append to event_log_dic, date_time, inactivity_time, sessinization.txt
    Output: Updated IP dictionary
    """
    # Inactive sessions will be identified every time when we add or modify
    # the dictionary.
    # inactive_sessions dictionary will store the inactive sessions to be removed from the
    # the IP dictionary (i.e., event_log_dic) that stores the identified sessions so far.
    inactive_sessions = list()

    # Check if all any IP's session expired
    for IP in event_log_dic:
        first_webpage_request_datetime = event_log_dic[IP][0]
        last_webpage_request_datetime = event_log_dic[IP][1]
        count_of_webpage_requests = event_log_dic[IP][2]

        # Inactivity_gap determines whether to start a new session for this IP
        inactivity_gap = (date_time - last_webpage_request_datetime).total_seconds()

        # If the time differance between the last webpage access and the current time is larger than inactivity_time
        # session has ended for this IP. This IP has to be appended to sessionization.txt and removed from
        # existing IPs dictionary
        if inactivity_gap > inactivity_time:
            # Calculate the duration of the session
            duration_of_the_session = int((last_webpage_request_datetime - first_webpage_request_datetime).total_seconds() + 1)

            # Prepare the output format and append it to the sessionization.txt
            output = IP + ',' + du.get_datetime_as_str(first_webpage_request_datetime) + ',' + du.get_datetime_as_str(last_webpage_request_datetime) + ',' + str(duration_of_the_session) + ',' + str(count_of_webpage_requests)
            sessinization_file_handler.write("%s\n" % output)
            inactive_sessions.append(IP)


    # Remove all IPs with expired sessions from the IP dictionary
    for IP in inactive_sessions:
        del event_log_dic[IP]
        print IP + ' has been deleted from event_log_dic\n'

    return event_log_dic



def main():
    # Get the filename of log file as the first command line argument
    log_filename = sys.argv[1]

    # Read the log file from "log.csv" and store it in
    # a list called weblog_list
    weblog_list = read_weblog(log_filename)

    # Read the inactivity time from "inactivity_time.txt" and store it in
    # a variable called inactivity_time
    inactivity_period_filename = sys.argv[2]
    inactivity_time = int(read_inactivity_time(inactivity_period_filename))

    # Get the sessionization file handler to append the lines to "sessionization" whenever it is necessary.
    sessinization_file_handler = open(sys.argv[3],'w+')

    # Dictionary to store IP sessions
    event_log_dic = {}

    # Index that will be used to identify the line number of the log file
    # when we itarate through the weblog_list that stores the logs
    index = 1

    # Iterate through the weblog_list
    for log in weblog_list:

        # Concatenate date and time
        date_time_str = log[1] + ' ' + log[2]
        date_time = du.get_string_as_datetime(date_time_str)

        # Before inserting or updating check if there is an expired session
        event_log_dic = check_for_inactive_sessions(event_log_dic, date_time, inactivity_time, sessinization_file_handler)

        # If this IP address does no exist in the dictionary, this is its first apperance.
        # So create an entry for it. Initial values are
        # first access = current_time, last access = current_time, web page access count = 1
        if not log[0] in event_log_dic:
            event_log_dic[log[0]] = [date_time, date_time, 1]

        # If this IP exists in the dictionary, update its last access time and increment its web page access count by one
        else:
            event_log_dic[log[0]][1] = date_time # Update this IP's last access time with current time
            event_log_dic[log[0]][2] = event_log_dic[log[0]][2] + 1 # Increment web page access count by one

        # If we reach the end of log file, close all remaining open sessions and write them to sessionization.txt
        if index == len(weblog_list):
            # To break the ties with same start time we sort them according to their values
            # values = (first access time, last access time, session duration, and web page count)
            sorted_event_log_list = sorted(event_log_dic.items(), key=operator.itemgetter(1))

            # Itarate through the sorted IP list
            for IP in sorted_event_log_list:
                first_webpage_request_datetime = IP[1][0] # First access time
                last_webpage_request_datetime = IP[1][1] # Last access time
                duration_of_the_session = int((last_webpage_request_datetime - first_webpage_request_datetime).total_seconds() + 1)
                count_of_webpage_requests = IP[1][2] # Access count
                output = IP[0] + ',' + du.get_datetime_as_str(first_webpage_request_datetime) + ',' + du.get_datetime_as_str(last_webpage_request_datetime) + ',' + str(duration_of_the_session) + ',' + str(count_of_webpage_requests)
                sessinization_file_handler.write("%s\n" % output)

        # Increment the line index of log file by one
        index = index + 1

    # Close the file handler of "sessionization.txt"
    sessinization_file_handler.close()


if __name__ == "__main__":
    main()
