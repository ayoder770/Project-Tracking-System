######################################################################
# File History
# 03/14/2021 - Andrew Yoder: Initial Release
######################################################################

import fpdf, sqlite3, openpyxl, datetime, os
from fpdf import FPDF
import pay_time

class MyFPDF(FPDF):
    pass

from platform_config import this_os, pt_base_dir, db_dir, pt_db, img_dir, client_workbook, Freelance_home


# Globals
totalFromAllClients = 0

# CONSTANTS
row = 2 # Row of client spreadsheet to begin pulling data from
column_width = 95.0
column_spacing = 5
table_height = 8    #height of table cells
item_date_width = 14.0 # width of item and date table cells
task_width = 105.0  # width of task title cells
hours_rate_total_width = width = 19.0   # width of hours, rate, and total cells
title_width = 133  # width of grand total lines


# Now Time Object
now = datetime.datetime.now()


# Determine information based on the day the invoice is being built
this_day        = pay_time.get_this_day()


# Get month of invoice
# If < 4, a period 2 invoice from last month is being built
if int(this_day) < 4:
    # Since we are building a period 2 invoice for last month...
    # ... get the name and number of last month...
    invoice_month = pay_time.get_last_month_name()
    invoice_month_numb = pay_time.get_last_month_numb()
# If > 16, a period 2 invoice for current month is being built
# Otherwise, a period 1 invoice is beign built for the current month
# In either case, the same functions are called
else:
    invoice_month      = pay_time.get_month_name()
    invoice_month_numb = pay_time.get_month_numb()

# Get the year for which this invoice is being built   
this_year = pay_time.get_this_year()


# Get the period number and dates for which invoice is being built
period_number   = pay_time.get_period_number( this_day, "pdf")
this_period     = pay_time.get_this_period_dates(period_number, invoice_month)


# Get the dates for which this invoice is sent
this_sent_on = pay_time.get_send_this_date(period_number, this_day, invoice_month_numb)


###### FUNCTION TO GET ORDINAL INDICATOR OF THE DATE ######
def get_ordinal_indicator(date):
    if( (date == 1) or (date == 21) or (date == 31) ):
        return str(date)+"st"
    elif( (date == 2) or (date == 22) ):
        return str(date)+"nd"
    elif( (date == 3) or (date == 23) ):
        return str(date)+"rd"
    else:
        return str(date)+"th"
###########################################################


###### FUNCTION TO CHECK IF INVOICE SHOULD BE BUILT FOR CLIENT ######
def build_invoice_check(prefix):
    
    # Connect to client's table and get length of projects
    client_proj_table = prefix+"_projects"
    db = sqlite3.connect(pt_db)
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM '''+client_proj_table)
    allResults = cursor.fetchall()

    # Check for manual work also
    cursor.execute('''SELECT * FROM manual_work WHERE for_client = ? ''',(prefix,))
    manualResults = cursor.fetchall()

    db.close()

    if len(allResults) > 0 or len(manualResults) > 0:
        return True
    else: 
        return False


###### FUNCTION TO KICK OFF INVOICE BUILD ######
def build_invoice(pdf, prefix):
    build_invoice_header(pdf, prefix)
################################################



###### FUNCTION TO BUILD INVOICE HEADER ######
def build_invoice_header(pdf, prefix):
    
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt=invoice_month+" "+str(this_year)+" Invoice #"+str(period_number), ln=1, align="L")
    pdf.line(11,22,198,22)
    pdf.ln(6)
    pdf.set_font("Arial", size=10)
    ybefore = pdf.get_y()


    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM all_clients WHERE client_prefix=?''',(prefix,))

    for row in cursor:
        name   = str(row[1])
        addr_1 = str(row[4])
        addr_2 = str(row[5])

    db.commit()
    db.close()

    pdf.multi_cell(column_width, column_spacing, "Bill To: " + name + "\n            " + addr_1 + "\n            " + addr_2, align="L")

    # Notice we have to account for the left margin to get the spacing between 
    # columns right.

    pdf.set_xy(column_width + pdf.l_margin + column_spacing, ybefore) 

    pdf.multi_cell(column_width, column_spacing, "Billing Period: [ "+this_period+" ]\nSent On: "+this_sent_on, align="L")

    pdf.ln(15)
    print_out_client_work(pdf, prefix)
##############################################



###### FUNCTION TO PRINT OUT ALL WORK DONE FOR CLIENT BY CONTRACTOR ######
def print_out_client_work(pdf, prefix):
    ybefore = pdf.get_y()
    pdf.set_font("Arial", style='B', size=11)

    # SET UP TABLE HEADERS
    pdf.multi_cell(item_date_width, table_height, "Item", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 1*(item_date_width), ybefore) 
    pdf.multi_cell(item_date_width, table_height, "Date", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 2*(item_date_width), ybefore) 
    pdf.multi_cell(task_width, table_height, "Task/Project", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width, ybefore) 
    pdf.multi_cell(hours_rate_total_width, table_height, "Hours", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 1*(hours_rate_total_width), ybefore) 
    pdf.multi_cell(hours_rate_total_width, table_height, "Rate", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 2*(hours_rate_total_width), ybefore) 
    pdf.multi_cell(hours_rate_total_width, table_height, "Total", border=1, align="C")

    # PRINT OUT ALL PROJECTS FROM CLIENT'S PROJECT TABLE
    pdf.set_font("Arial", size=10)

    client_proj_table = prefix+"_projects"
    item = 1
    total_hours = 0.00
    total_cost = 0.00
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT client_hourly FROM all_clients WHERE client_prefix = ? ''',(prefix,))

    for row in cursor:
        hourly = '{0}'.format(row[0])
    cursor.execute('''SELECT * FROM '''+client_proj_table)
    
    for row in cursor:
        this_hour = round(float(row[4]),2)
        this_cost = round(this_hour*float(hourly),2)
        total_hours = total_hours + this_hour
        total_cost = total_cost + this_cost
        start = row[2]
        end = row[3]
        if start != end:
            date_string = str(start)+" - "+str(end)
        else:
            date_string = get_ordinal_indicator(start)
                                                                                                                        
        ybefore = pdf.get_y()                                                                                                                                                  

        pdf.multi_cell(item_date_width, table_height, str(item), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 1*(item_date_width), ybefore) 
        pdf.multi_cell(item_date_width, table_height, date_string, border=1, align="C")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width), ybefore) 
        pdf.multi_cell(task_width, table_height, "  "+format(row[1]), border=1, align="L")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width, ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, format(this_hour,'.2f'), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 1*(hours_rate_total_width), ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, "$"+format(float(hourly),'.2f'), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 2*(hours_rate_total_width), ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, "$"+format(this_cost,'.2f'), border=1, align="C")
        item = item + 1
    db.commit()
    db.close()
    print_subcontractor_work(pdf, prefix, item, total_hours, total_cost)
##########################################################################



####### FUNCTION TO PRINT OUT SUBCONTRACTOR WORK FOR CLIENT ######
def print_subcontractor_work(pdf, prefix, item, total_hours, total_cost):
    total_sub_hours = 0
    total_sub_cost = 0
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM subcontractors WHERE for_client = ? ''',(prefix,))
    for row in cursor:
        total_sub_hours = total_sub_hours + float(row[4])
        total_sub_cost = total_sub_cost + float(row[6])
        
        ybefore = pdf.get_y()

        pdf.multi_cell(item_date_width, table_height, str(item), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 1*(item_date_width), ybefore) 
        pdf.multi_cell(item_date_width, table_height, "-", border=1, align="C")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width), ybefore) 
        pdf.multi_cell(task_width, table_height, "  EXTERNAL: "+format(row[1])+" - "+format(row[2]), border=1, align="L")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width, ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, str(row[4]), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 1*(hours_rate_total_width), ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, "$"+str(row[5]), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 2*(hours_rate_total_width), ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, "$"+str(row[6]), border=1, align="C")
        item = item + 1

    db.commit()
    db.close()
    print_manual_work(pdf, prefix, item, total_hours, total_cost, total_sub_hours, total_sub_cost)
##################################################################



####### FUNCTION TO PRINT OUT MANUAL/FIXED WORK FOR CLIENT ######
def print_manual_work(pdf, prefix, item, total_hours, total_cost, total_sub_hours, total_sub_cost):
    total_man_hours = 0
    total_man_cost = 0
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM manual_work WHERE for_client = ? ''',(prefix,))
    for row in cursor:
        # Check the data type before adding to the total time
        if type(row[4]) is float:
            total_man_hours = total_man_hours + float(row[4])

        if type(row[6]) is float:
            total_man_cost = total_man_cost + float(row[6])
        
        ybefore = pdf.get_y()

        pdf.multi_cell(item_date_width, table_height, str(item), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 1*(item_date_width), ybefore) 
        pdf.multi_cell(item_date_width, table_height, str(row[2]), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width), ybefore) 
        pdf.multi_cell(task_width, table_height, "  "+format(row[3]), border=1, align="L")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width, ybefore) 
        if type(row[4]) is float: 
            pdf.multi_cell(hours_rate_total_width, table_height, str(format(row[4],'.2f')), border=1, align="C")
        else:
            pdf.multi_cell(hours_rate_total_width, table_height, str(row[4]), border=1, align="C")

        # Print total number of hours ... or applicable cell content
        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 1*(hours_rate_total_width), ybefore)
        if type(row[5]) is not str:
            pdf.multi_cell(hours_rate_total_width, table_height, "$"+str(format(row[5],'.2f')), border=1, align="C")
        else:
            pdf.multi_cell(hours_rate_total_width, table_height, str(row[5]), border=1, align="C")

        pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 2*(hours_rate_total_width), ybefore) 

        if type(row[6]) is str:
            pdf.multi_cell(hours_rate_total_width, table_height, str(row[6]), border=1, align="C")
        else:
            pdf.multi_cell(hours_rate_total_width, table_height, "$"+str(format(row[6],'.2f')), border=1, align="C")
           
        item = item + 1
    db.commit()
    db.close()
    print_blank_table_row(pdf, prefix, total_hours, total_cost, total_sub_hours, total_sub_cost, total_man_hours, total_man_cost)
##################################################################



###### FUNCTION TO PRINT OUT ONE BLANK TABLE ROW ######
def print_blank_table_row(pdf, prefix, total_hours, total_cost, total_sub_hours, total_sub_cost, total_man_hours, total_man_cost):
    ybefore = pdf.get_y()
    pdf.multi_cell(item_date_width, table_height, "", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 1*(item_date_width), ybefore) 
    pdf.multi_cell(item_date_width, table_height, "", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 2*(item_date_width), ybefore) 
    pdf.multi_cell(task_width, table_height, "", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width, ybefore) 
    pdf.multi_cell(hours_rate_total_width, table_height, "", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 1*(hours_rate_total_width), ybefore) 
    pdf.multi_cell(hours_rate_total_width, table_height, "", border=1, align="C")

    pdf.set_xy(pdf.l_margin + 2*(item_date_width) + task_width + 2*(hours_rate_total_width), ybefore) 
    pdf.multi_cell(hours_rate_total_width, table_height, "", border=1, align="C")
    print_contractor_and_subcontrator_totals(pdf, prefix, total_hours, total_cost, total_sub_hours, total_sub_cost, total_man_hours, total_man_cost)
#######################################################



###### FUNCTION TO PRINT OUT SEPARATE TOTAL LINES FOR CONTRACTOR AND SUBCONTRACTOR ######
def print_contractor_and_subcontrator_totals(pdf, prefix, total_hours, total_cost, total_sub_hours, total_sub_cost, total_man_hours, total_man_cost):
    if ( (total_sub_hours != 0) and (total_sub_cost != 0) ):
        # LINE FOR ANDREWS WORK
        pdf.set_font("Arial", size=11)
        ybefore = pdf.get_y()
        pdf.multi_cell(title_width, table_height, "Totals for " + provider_name + "'s Support Work     ", border=1, align="R")

        pdf.set_xy(pdf.l_margin + title_width, ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, str(total_hours+total_man_hours), border=1, align="C")

        pdf.set_xy(pdf.l_margin + title_width + 1*(hours_rate_total_width), ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, "", border=1, align="C")

        pdf.set_xy(pdf.l_margin + title_width + 2*(hours_rate_total_width), ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, "$"+str(total_cost+total_man_cost), border=1, align="C")

        # LINE FOR SUBCONTRACTORS
        ybefore = pdf.get_y()
        pdf.multi_cell(title_width, table_height, "Totals for External Support Work     ", border=1, align="R")

        pdf.set_xy(pdf.l_margin + title_width, ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, str(total_sub_hours), border=1, align="C")

        pdf.set_xy(pdf.l_margin + title_width + 1*(hours_rate_total_width), ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, "", border=1, align="C")

        pdf.set_xy(pdf.l_margin + title_width + 2*(hours_rate_total_width), ybefore) 
        pdf.multi_cell(hours_rate_total_width, table_height, "$"+str(total_sub_cost), border=1, align="C")
        
    print_grand_total_line(pdf, prefix, total_hours, total_cost, total_sub_hours, total_sub_cost, total_man_hours, total_man_cost)
#########################################################################################



###### FUNCTION TO PRINT OUT GRAND TOTAL LINE ######
def print_grand_total_line(pdf, prefix, total_hours, total_cost, total_sub_hours, total_sub_cost, total_man_hours, total_man_cost):
    pdf.set_font("Arial", style='B', size=11)
    ybefore = pdf.get_y()
    pdf.multi_cell(title_width, table_height, "Grand Total     ", border=1, align="R")

    pdf.set_xy(pdf.l_margin + title_width, ybefore)
    if ( (total_sub_hours != 0) and (total_sub_cost != 0) ):
        pdf.multi_cell(hours_rate_total_width, table_height, str(format(total_sub_hours + total_hours + total_man_hours,'.2f')), border=1, align="C")
    else:
        pdf.multi_cell(hours_rate_total_width, table_height, str(format(total_hours + total_man_hours,'.2f')), border=1, align="C")

    pdf.set_xy(pdf.l_margin + title_width + 1*(hours_rate_total_width), ybefore) 
    pdf.multi_cell(hours_rate_total_width, table_height, "", border=1, align="C")

    pdf.set_xy(pdf.l_margin + title_width + 2*(hours_rate_total_width), ybefore) 
    if ( (total_sub_hours != 0) and (total_sub_cost != 0) ):
        pdf.multi_cell(hours_rate_total_width, table_height, "$"+str(format(total_cost + total_sub_cost + total_man_cost,'.2f')), border=1, align="C")
    else:
        pdf.multi_cell(hours_rate_total_width, table_height, "$"+str(format(total_cost + total_man_cost,'.2f')), border=1, align="C")
    print_button_and_thank_you(pdf, prefix, total_cost, total_sub_cost, total_man_cost)
####################################################



###### FUNCTION TO PRINT OUT PAYPAL BUTTON AND THANK YOU ######
def print_button_and_thank_you(pdf, prefix, total_cost, total_sub_cost, total_man_cost):
    grand_total = total_cost + total_sub_cost + total_man_cost
    pay_link = paypal_link + str(grand_total)
    pdf.ln(6)
    pdf.image(img_dir+'paypal_button.jpg', x = 145.5, y = None, w = 55, h = 0, type = 'JPG', link = pay_link)
    pdf.ln(2)
    ybefore = pdf.get_y()
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt="Thank you for your business. I am proud to be working with you!        ", ln=1, align="R")
    print_footer(pdf, prefix, grand_total)
###############################################################



###### FUNCTION TO PRINT OUT INVOICE FOOTER ######
def print_footer(pdf, prefix, grand_total):
    
    pdf.set_y(-43)
    pdf.set_font("Arial", size=16)

    pdf.cell(200, 10, txt=provider_name + " - " + provider_title, ln=1, align="L")
    pdf.line(11,264,198,264)

    pdf.ln(2)
    pdf.set_font("Arial", size=10)
    ybefore = pdf.get_y()
    pdf.multi_cell(column_width, column_spacing, "Tel: " + provider_phone + "\nEmail: " + provider_email, align="L")

    # Notice we have to account for the left margin to get the spacing between 
    # columns right.

    pdf.set_xy(column_width + pdf.l_margin + column_spacing, ybefore) 

    pdf.multi_cell(column_width, column_spacing, provider_location, align="L")
    
    pdf.line(11,279,198,279)
    
    # Wrap up stuff
    global totalFromAllClients
    totalFromAllClients = totalFromAllClients + float(grand_total)
    print("Invoice Built for Client "+prefix+": Total Charges: $"+str(format(grand_total,'.2f')))
##################################################
 
    
    
    
    
 
    
    
    
#### MAIN PROGRAM ####

# PULL IN EXCEL DOC DATA  HERE
invoice_info = openpyxl.load_workbook(client_workbook)
sheet = invoice_info["Sheet1"]

# counter for loop
i = 0

# Loop over clients
while True:
    
    # Get prefix of client
    prefix   = sheet.cell(row=i+row, column = 2).value
    if prefix == None:
        break
   
    # Get the client folder
    client_folder   = sheet.cell(row=i+row, column = 3).value
  
    #Check if client has any projects to build an invoice with
    if ( build_invoice_check(prefix) ):
        pdf=MyFPDF()
        pdf.add_page()    
        build_invoice(pdf, prefix)
        doc_path = Freelance_home + client_folder+"/Invoices/"
        doc_name = prefix+"_"+invoice_month+"_"+str(this_year)+"_Invoice_"+str(period_number)+".pdf"
        doc_build = doc_path+doc_name
        pdf.output(doc_build)
        if ( this_os == "Linux" ):
            os.system("xdg-open "+doc_build)
        elif ( this_os == "Windows" ):
            os.system("start " + doc_build)
    else:
        print("No Invoice Built for Client "+prefix)
    i = i + 1
  

# Print out closing comments
print("")
print("Total charges this billing period: $"+str(format(totalFromAllClients,'.2f')))
