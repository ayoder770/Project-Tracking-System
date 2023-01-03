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
######################################################################

import datetime

# Month Dictionary
month_by_numb = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November","12":"December"}

# Dictionary for number of days in each month
days_in_month = {"January":"31st","February":"28th","March":"31st","April":"30th","May":"31st","June":"30th","July":"31st","August":"31st","September":"30th","October":"31st","November":"30th","December":"31st"}

# Dictionary for all federal holidays to not send invoices on
fed_holidays = {"01-01" : "New Year's Day",
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

# Get a current date/time object
now = datetime.datetime.now()


# Return number of current month ( 1 - 12 )
def get_month_numb() -> str:
    return now.strftime("%m")


# Return full name of current month ( January - December )
def get_month_name() -> str:
    return now.strftime("%B")


# Return the number of last month
def get_last_month_numb() -> str:
    this_month = get_month_numb()
    # If this month is January, then last month is December
    if ( this_month == 1 ): 
        return str(12)
    else:
        return str(int(this_month) - 1)


# Return full name of last month
def get_last_month_name() -> str:
    this_month = get_month_numb()
    # If this month is January, then last month is December
    if ( this_month == "01" ): 
        return month_by_numb[str(12)]
    else:
        return month_by_numb[str(int(this_month) - 1)]


# Return current year
def get_this_year():
    return now.year


# Return current day of month
def get_this_day():
    return now.strftime("%d")


# Return the name of the period month
def get_pay_period_month(this_day):
    if int(this_day) < 5:
        return get_last_month_name()
    else:
        return get_month_name()

    
# Return period number of pay period
def get_period_number(day, mode):
    if mode == "invoice":
        if int(day) > 15:
            period_number = 1
        else:
            period_number = 2
    elif mode == "pdf":
        if int(day) > 3 and int(day) < 18:
            period_number = 1
        else:
            period_number = 2
    return period_number


# Return the dates for this pay period
# Included in the invoice and invoice email
def get_this_period_dates(period, period_month):
    if period == 1:
        period_dates = " "+period_month+" 1st - "+period_month+" 15th "
    elif period == 2:
        period_dates = " "+period_month+" 16th - "+period_month+" "+days_in_month[period_month]+" "
    return period_dates

        
# Validate send date to ensure not weekend or holiday
def validate_send_date(ns_obj):
    check_day = ns_obj.strftime("%A")
    check_holiday = ns_obj.strftime("%m")+"-"+ns_obj.strftime("%d")
    if check_day == "Saturday" or check_day == "Sunday":
        print("Cannot send on Saturday or Sunday")
        return 0
    elif check_holiday in fed_holidays:
        print("Cannot send invoice on "+fed_holidays[check_holiday])
        return 0
    else:
        return 1
    

# Function to return the date for which this invoice is being sent
# Input Arguments:
#   period - The invoice period ( 1 or 2 )
#   this_day - The day of the month this invoice is currently being built
#   this_month - The month for which the invoice applies
def get_send_this_date(period, this_day, invoice_month):
    ts_offset = 0
    valid = 0
    # If we are building an invoice for period 1...
    if period == 1:
        # Assume the invoice is being sent on the 16th of the current month 
        ts_base = 16
        send_month = int(invoice_month)
        send_year = now.year
    # Else if we are building an invoice for period 2
    elif int(period) == 2:
        # If "this_day" is less than 16, an invoice is being built and emailed late for period 2
        # Else, assume the invoice will be sent on the first of the month
        if int(this_day) < 16:
            ts_base = int(this_day)
        else:
            ts_base = 1
        # If the invoice month is December, the send month is January, else it is month+1
        if int(invoice_month) == 12:
            send_month = 1
            send_year = now.year + 1
        else:
            send_month = int(invoice_month)+1
            send_year = now.year
    # Create a date object with the data gathered
    ts_obj = datetime.datetime(send_year, send_month, ts_base)
    # Now validate the date to ensure it is not a weekend or a federal holiday
    while valid == 0:
        validate = validate_send_date(ts_obj)
        if validate == 1:
            valid = 1
        else:
            ts_offset = ts_offset + 1
            ts_obj = datetime.datetime(int(send_year), int(send_month), ts_base+ts_offset)
    # Return the validated date string
    return ts_obj.strftime("%A")+", "+ts_obj.strftime("%b")+" "+ts_obj.strftime("%d")+", "+ts_obj.strftime("%Y")
