#!/usr/bin/python3
######################################################################
# File Name: invoice_build_dates_unit_tests.py
#
# Description: Unit tests to verify correct functionality of the 
#              Invoice_Build class
#
# File History
# 08/26/2023 - Andrew Yoder : Initial Release
######################################################################

import sys
import datetime

sys.path.append('../python')
import pay_time

frequencies = ["monthly", "biweekly"]

unit_tests = {

    "one": {
        "title": "Period 2 Invoice when built from the start of the next month within the same year",
        "timestamp": "2023-08-01"
    },
    "two": {
        "title": "Period 2 Invoice when built at the end of the same month within the same year",
        "timestamp": "2023-07-31"
    },
    "three": {
        "title": "Period 2 Invoice built at the end of the month when the 1st falls on a Saturday",
        "timestamp": "2023-06-30"
    },
    "four": {
        "title": "Period 2 Invoice built at the end of the year sent the next year skipping New Year's Day",
        "timestamp": "2023-12-31"
    },
    "five": {
        "title": "Period 2 Invoice built at the beginning of the year for the previous December",
        "timestamp": "2024-01-01"
    },
}

for test in unit_tests.values():
    print("Test Case: " + test["title"])
    datetime_object = datetime.datetime.strptime(test["timestamp"], "%Y-%m-%d")
    print("Test Build Timestamp: " + str(datetime_object))
    print("")

    for frequency in frequencies:
        print("Test Frequency: " + frequency)

        dateobject = pay_time.Invoice_Build(datetime_object, frequency)

        print("Build Day: " + str(dateobject.build_day))
        print("Invoice Period: " + str(dateobject.period_number))
        print("Invoice Month: " + str(dateobject.invoice_month))
        print("Invoice Year: " + str(dateobject.invoice_year))
        print("Invoice Date Range: " + str(dateobject.invoice_date_range))
        print("Invoice Send Date: " + str(dateobject.invoice_send_date))
        print("")

    print("**************************************************\n")