import csv
import datetime
import date_utils as du
import operator
import sys

TIMESTAMP_FORMAT = "YYYY-mm-dd HH:MM:SS"

def read_inactivity_time(filename):
    with open(filename,'r') as f:
        line = f.readline()
        inactivity_time = line.rstrip('\n')
        return inactivity_time


def read_weblog(filename):
    """ Reads the log file and extract the related fields,
    such as IP address, access date, access time """
    line_number = 0
    weblog_list = list()

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if(line_number > 0):
                weblog_list.append([row[0], row[1], row[2]]) # IP, access date, access time
            line_number = line_number + 1
        return weblog_list


def main():

    #log_filename = "../input/log.csv"
    log_filename = sys.argv[1]

    weblog_list = read_weblog(log_filename)

    #inactivity_period_filename = "../input/inactivity_period.txt"
    inactivity_period_filename = sys.argv[2]
    inactivity_time = int(read_inactivity_time(inactivity_period_filename))

    #sessinization_file_handler = open('../output/sessionization.txt','w+')
    sessinization_file_handler = open(sys.argv[3],'w+')

    # Dictionary to store IP sessions
    event_log_dic = {}
    index = 1

    for log in weblog_list:

        date_time_str = log[1] + ' ' + log[2] # Concatenate date and time
        date_time = du.get_string_as_datetime(date_time_str)

        # If this IP address does no exist in the dictionary, this is its first apperance
        # so create an entry for it. Initial values are first access = current_time,
        # last access = current_time, web page access count = 1
        if not log[0] in event_log_dic:
            event_log_dic[log[0]] = [date_time, date_time, 1]

        # If this IP exists in the dictionary, update its last access time and increment its web page access count
        else:
            event_log_dic[log[0]][1] = date_time # Update this IP's last access time with current time
            event_log_dic[log[0]][2] = event_log_dic[log[0]][2] + 1 # Increment web page access count by one

        # Stores sessions to be removed
        to_be_removed = list()

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
                to_be_removed.append(IP)

        # Remove all IP with expired sessions from the IP dictionary
        for IP in to_be_removed:
            del event_log_dic[IP]


        # If we reach the end of log file, close all remaining open sessions and write them to sessionization.txt
        if index == len(weblog_list):

            # To break the ties with same start time we sort them according to their values
            sorted_event_log_list = sorted(event_log_dic.items(), key=operator.itemgetter(1))

            for IP in sorted_event_log_list:
                first_webpage_request_datetime = IP[1][0] # First access time
                last_webpage_request_datetime = IP[1][1] # Last access time
                duration_of_the_session = int((last_webpage_request_datetime - first_webpage_request_datetime).total_seconds() + 1)
                count_of_webpage_requests = IP[1][2] # Access count
                output = IP[0] + ',' + du.get_datetime_as_str(first_webpage_request_datetime) + ',' + du.get_datetime_as_str(last_webpage_request_datetime) + ',' + str(duration_of_the_session) + ',' + str(count_of_webpage_requests)
                sessinization_file_handler.write("%s\n" % output)

        # Increment the line index of log file by one
        index = index + 1


    sessinization_file_handler.close()


if __name__ == "__main__":
    main()
