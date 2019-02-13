import csv
import datetime
import date_utils as du

TIMESTAMP_FORMAT = "YYYY-mm-dd HH:MM:SS"

sessinization_file_handler = open('../output/sessionization.txt','w+')


def read_inactivity_time(filename):
    with open(filename,'r') as f:
        line = f.readline()
        inactivity_time = line.rstrip('\n')
        return inactivity_time


def read_weblog(filename):
    line_number = 0
    weblog_list = list()

    with open('../input/log.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if(line_number > 0):
                weblog_list.append([row[0], row[1], row[2]]) # IP, access date, access time
            line_number = line_number + 1
        return weblog_list

def append_to_sessinization(item):
    sessinization_file_handler.write("%s\n" % item)


inactivity_period_filename = "../input/inactivity_period.txt"
inactivity_time = int(read_inactivity_time(inactivity_period_filename))

log_filename = "../input/log.csv"
weblog_list = read_weblog(log_filename)


event_log_dic = {}
index = 1


for log in weblog_list:

    date_time_str = log[1] + ' ' + log[2] # Concatenate date and time
    date_time = du.get_string_as_datetime(date_time_str)


    # If this IP does not exist in the dictionary
    if not log[0] in event_log_dic:

        # If an IP address is used as a key for the first time in the dictionary
        # this means that the first and last access datetimes can be used as the same
        # Every time an IP address that exists in the dictionary accesses another webpage
        # its last access time is updated.
        event_log_dic[log[0]] = [date_time, date_time, 1]

        # format: IP (key):  first_webpage_request_datetime, last_webpage_request_datetime, count_of_webpage_requests
        # count_of_webpage_requests is initially one.

    # If this IP already exists in the dictionaty, update its last access datetime, increase its count_of_webpage_requests
    # and check the time differance between last_webpage_request_datetime and first_webpage_request_datetime is
    # larger than inactivity_time. If so write this key:value pair to sessionization.txt and
    # start a new session (i.e, overwrite its first and last webpage access times)
    else:
        first_webpage_request_datetime = event_log_dic[log[0]][0]
        last_webpage_request_datetime = event_log_dic[log[0]][1]
        count_of_webpage_requests = event_log_dic[log[0]][2]

        # Inactivity_gap determines whether to start a new session or not
        inactivity_gap = (date_time - last_webpage_request_datetime).total_seconds()


        # If the time differance between current and first webpage access is larger than inactivity_time
        # session has ended for the current IP and has to be appended to sessionization.txt
        if inactivity_gap > inactivity_time:
            # Calculate the duration of the session
            duration_of_the_session = int((last_webpage_request_datetime - first_webpage_request_datetime).total_seconds() + 1)

            # Prepate the output format and append it to the sessionization.txt
            output = log[0] + ',' + du.get_datetime_as_str(first_webpage_request_datetime) + ',' + du.get_datetime_as_str(last_webpage_request_datetime) + ',' + str(duration_of_the_session) + ',' + str(count_of_webpage_requests)
            append_to_sessinization(output)

            # A new session has started for the same IP. Update the start of a new session.
            event_log_dic[log[0]][0] = date_time
            event_log_dic[log[0]][1] = date_time
            event_log_dic[log[0]][2] = 1


        # If a webpage has been accessed by the same IP within within inactivity_time, update last_webpage_request_datetime
        # and increment count_of_webpage_requests by 1
        else:
            event_log_dic[log[0]][1] = date_time
            event_log_dic[log[0]][2] = count_of_webpage_requests + 1

    # If we reach the end of log file, close all remaining sessions and write them to sessionization.txt
    if index == len(weblog_list):
        for IP in event_log_dic:
            first_webpage_request_datetime = event_log_dic[IP][0]
            last_webpage_request_datetime = event_log_dic[IP][1]
            duration_of_the_session = int((last_webpage_request_datetime - first_webpage_request_datetime).total_seconds() + 1)
            count_of_webpage_requests = event_log_dic[IP][2]
            output = IP + ',' + du.get_datetime_as_str(first_webpage_request_datetime) + ',' + du.get_datetime_as_str(last_webpage_request_datetime) + ',' + str(duration_of_the_session) + ',' + str(count_of_webpage_requests)
            append_to_sessinization(output)

    # Increment the line index of log file by one
    index = index + 1

sessinization_file_handler.close()
