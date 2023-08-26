#!/usr/bin/python3
######################################################################
# File Name: pay_time.py
#
# Description: Python functions to handle date/time for invoices
#
# File History
# 03/14/2021 - Andrew Yoder : Initial Release
# 09/28/2021 - Andrew Yoder : Removed commented out / dead code
# 11/06/2021 - Andrew Yoder : Specifically call out python3
# 01/01/2022 - Andrew Yoder : Fix month comparison for year rollover
#                           : Return year as integer, not string
# 01/16/2022 - Andrew Yoder : Updated for 2022 Federal Holidays
# 01/03/2023 - Andrew Yoder : Updated for 2023 Holidays
# 08/05/2023 - Andrew Yoder : Refactored to be a class
#                           : Added support for monthly invoicing : GH-5
######################################################################

import datetime

class Invoice_Build:
    """
    Class for date object surrounding invoice sending
    """

    # Month Dictionary
    _month_by_numb = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November","12":"December"}

    # Dictionary for number of days in each month
    _days_in_month = {"January":"31st","February":"28th","March":"31st","April":"30th","May":"31st","June":"30th","July":"31st","August":"31st","September":"30th","October":"31st","November":"30th","December":"31st"}

    # Dictionary for all federal holidays to not send invoices on
    _fed_holidays = {
        "01-01" : "New Year's Day",
        "01-16" : "Martin Luther King Jr. Day",
        "02-20" : "President's Day",
        "05-29" : "Memorial Day",
        "06-19" : "Juneteenth",
        "07-04" : "Independence Day",
        "09-04" : "Labor Day",
        "10-09" : "Columbus Day",
        "11-10" : "Veteran's Day",
        "11-23" : "Thanksgiving Day",
        "12-24" : "Christmas Eve",
        "12-25" : "Christmas Day",
        "12-31" : "New Year's Eve"
    }


    def __init__(self, datetime, frequency):
        self.now_build = datetime
        self.frequency = frequency
    
        # The day on which the invoice is built to determine other information
        self.build_day = int(self.now_build.strftime("%d"))
        self.period_number = self.get_period_number(self.build_day)
        self.invoice_month = self.get_invoice_month(self.build_day)
        self.invoice_year = self.get_invoice_year(self.build_day, self.invoice_month["number"])
        self.invoice_date_range = self.get_invoice_date_range(self.period_number, self.frequency, self.invoice_month["name"])
        self.invoice_send_date = self.get_invoice_send_date(self.build_day, self.period_number, self.invoice_month["number"])


    def get_period_number(self, build_day):
        """
            Return the period number for the invoice. Will either be 1 or 2 for bimonthly
            Monthly will always return period 2

            Input:
              build_day -- The numeric day the invoice is being built on
            Output:
              The period number
        """
        # If building at the end of the month or beginning of the month. Either:
        # Bimonthly: building period 2 invoice for the end of the month
        # Monthly: building monthly invoice for all month's work
        if (build_day >= 26) or (build_day <= 5):
            period_number = 2
        else:
            period_number = 1
        return period_number


    def get_invoice_month(self, build_day):
        """
            Return the Name and Number of the Invoice month

            Input:
              build_day -- The numeric day the invoice is being built on
            Output:
              Dictionary containing two values:
              'name': The name of the invoice month - January, February, etc..
              'number': The number of the invoice month - 1, 2, etc..
        """
        # If building beginning of month, the invoice month is last 
        # month relative to the build date. Else, build month is the same as the invoice month
        month_index = int(self.now_build.strftime("%m"))
        offset = 0
        if (build_day <= 5):
            offset = 1
        month_index = month_index - offset
        if (month_index == 0):
            month_index = 12
        invoice_month_name = self._month_by_numb[str(month_index)]
        invoice_month_number = str(month_index)
        return { "name": invoice_month_name, "number": invoice_month_number}

 
    def get_invoice_year(self, build_day, invoice_month):
        """
            Return the year for the invoice

            Input:
              build_day -- The numeric day the invoice is being built on
              invoice_month -- The numeric month the invoice is being built for
            Output:
              The year the invoice is being built for
        """
        offset = 0
        if (build_day <= 5 ) and (int(invoice_month) == 12):
            offset = 1
        invoice_year = int(self.now_build.year) - offset
        return invoice_year


    def get_invoice_date_range(self, period_number, frequency, invoice_month):
        """
            Return the date range this invoice covers

            Input:
              period_number -- The period number of the invoice
              frequency -- The frequency of the invoice schedule
              invoice_month -- The numeric month the invoice is being built for
            Output:
              The date range the invoice covers
        """
        if (period_number == 1):
            period_dates = invoice_month + " 1st - " + invoice_month + " 15th"
        elif (period_number == 2):
            if (frequency == "monthly"):
                period_dates = invoice_month + " 1st - " + invoice_month + " " + self._days_in_month[invoice_month]
            if (frequency == "biweekly"):
                period_dates = invoice_month + " 16th - " + invoice_month + " " + self._days_in_month[invoice_month]
        return period_dates

            
    def validate_send_date(self, ns_obj):
        """
            Validate send date to ensure not a weekend or a holiday

            Input:
              ns_obj -- The time object to validate
            Output:
              0 -- invalid date for sending the invoice
              1 -- valid date
        """
        check_day = ns_obj.strftime("%A")
        check_holiday = ns_obj.strftime("%m")+"-"+ns_obj.strftime("%d")
        if check_day == "Saturday" or check_day == "Sunday":
            print("Cannot send on Saturday or Sunday")
            return 0
        elif check_holiday in self._fed_holidays:
            print("Cannot send invoice on " + self._fed_holidays[check_holiday])
            return 0
        else:
            return 1
        

    def get_invoice_send_date(self, build_day, period, invoice_month):
        """
            Get the date the invoice will be sent on. Invoices are not sent on weekends
            or federal holidays.

            Input:
              build_day -- The numeric day the invoice is being built on
              period -- The period number of the invoice
              invoice_month -- The numeric month the invoice is being built for
            Output: 
              The send date
        """
        ts_offset = 0
        valid = 0
        # If we are building an invoice for period 1...
        if period == 1:
            # Assume the invoice is being sent on the 16th of the current month 
            ts_base = 16
            send_month = int(invoice_month)
            send_year = self.now_build.year
        # Else if we are building an invoice for period 2
        elif int(period) == 2:
            # If "build_day" is less than 16, an invoice is being built and emailed late for period 2
            # Else, assume the invoice will be sent on the first of the month
            if int(build_day) < 16:
                ts_base = int(build_day)
            else:
                ts_base = 1
            # If the invoice month is December, the send month is January, else it is month+1
            if int(invoice_month) == 12:
                send_month = 1
                if (int(build_day) <= 5):
                    send_year = self.now_build.year
                else:
                    send_year = self.now_build.year + 1
            else:
                send_month = int(invoice_month)+1
                send_year = self.now_build.year
        # Create a date object with the data gathered
        ts_obj = datetime.datetime(send_year, send_month, ts_base)
        # Now validate the date to ensure it is not a weekend or a federal holiday
        while valid == 0:
            validate = self.validate_send_date(ts_obj)
            if validate == 1:
                valid = 1
            else:
                ts_offset = ts_offset + 1
                ts_obj = datetime.datetime(int(send_year), int(send_month), ts_base+ts_offset)
        # Return the validated date string
        return ts_obj.strftime("%A")+", "+ts_obj.strftime("%b")+" "+ts_obj.strftime("%d")+", "+ts_obj.strftime("%Y")