#!/usr/bin/python
######################################################################
# File History
# 03/14/2021 - Andrew Yoder: Initial Release
######################################################################

import sys
import sqlite3
import time
import datetime
import types

from platform_config import pt_base_dir, db_dir, pt_db



one_tab   = '\t'
two_tab   = '\t\t'
three_tab = '\t\t\t'
four_tab  = '\t\t\t\t'
five_tab  = '\t\t\t\t\t'
six_tab  = '\t\t\t\t\t\t'


################################################################################

def get_tabs(len_diff):
    if len_diff <= 5:
        tab = one_tab
    elif len_diff <= 14:
        tab = two_tab
    elif len_diff <= 21:
        tab = three_tab
    elif len_diff <= 27:
        tab = four_tab
    elif len_diff <= 34:
        tab = five_tab
    elif len_diff <= 39:
        tab = six_tab
    else:
        tab = six_tab
    return tab

def wait():
    print('')
    print("Track A Current Project: T")
    print("Add A New Project: NP")
    print("Add A New Client: NC")
    print("View Client Reports: R")
    print("Delete Project(s): D")
    print("Add Subcontractor Work: S")
    print("Add Manual/Fixed Task: M")
    print("Edit a Current Project: E")
    print("Quit Program: Q")
    action = input("What Would You Like To Do? ")
    if (action == "T" or action == "t"):
        track_current_project()
    elif (action == "NC" or action == "nc"):
        add_new_client()
    elif (action == "NP" or action == "np"):
        add_new_project()
    elif (action == "R" or action == "r"):
        view_reports()
    elif (action == "Q" or action == "q"):
        return "quit"
    elif (action == "D" or action == "d"):
        delete_project_s()
    elif (action == "S" or action == "s"):
        add_subcontractor()
    elif (action == "M" or action == "m"):
        add_manual_job()
    elif (action == "E" or action == "e"):
        update_project()
    elif action == "U":
        deploy_updates()
    else:
        print('')
        print("Did not recognize that option, please try again")
        wait()
    

#FUNCTION TO ADD A NEW CLIENT TO THE SYSTEM
def add_new_client():
    print('')
    print("*********************************************************************************************************************************")
    print("******************************************************** ADDING NEW CLIENT ******************************************************")
    print("*********************************************************************************************************************************")
    new_client_name = input("Enter New Client Full Name: ")
    new_client_pre  = input("Enter New Client Prefix: ")
    new_client_hourly = input("Enter New Client's Hourly Rate: ")
    new_client_address_1 = input("Enter New Client's Address Line 1: ")
    new_client_address_2 = input("Enter New Client's Address Line 2: ")
    new_client_proj_table = new_client_pre+"_projects"
    #connect to db
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    # Insert New Client
    cursor.execute('''INSERT INTO all_clients(client_name,client_prefix,client_hourly,address_1,address_2)
                  VALUES(?,?,?,?,?)''', (new_client_name,new_client_pre,new_client_hourly,new_client_address_1,new_client_address_2))
    # Create table for new client's projects
    cursor.execute('''CREATE TABLE '''+new_client_proj_table+'''(id INTEGER PRIMARY KEY, proj_name TEXT, date_start INTEGER, date_end INTEGER, proj_time FLOAT)''')
    db.commit()
    db.close()
    print('New Client '+new_client_name+' Has Been Successfully Added')
    print("*********************************************************************************************************************************")
    print('')
    #wait()
    

# FUNCTION TO ADD A NEW PROJECT FOR A CLIENT
def add_new_project():
    print('')
    print("*********************************************************************************************************************************")
    print("******************************************************* ADDING NEW PROJECT ******************************************************")
    print("*********************************************************************************************************************************")
    prefix = input("Enter Prefix of Client With New Project: ")
    new_proj_name = input("Enter Name of New Task/Project: ")
    if (new_proj_name == "x" or new_proj_name == "X"):
        return
    client_proj_table = prefix+"_projects"
    today = datetime.datetime.today().day
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    # Insert New Client
    cursor.execute('''INSERT INTO '''+client_proj_table+'''(proj_name,date_start,date_end,proj_time) VALUES(?,?,?,?)''', (new_proj_name,today,today,0.00))
    db.commit()
    db.close()
    print('New Project '+new_proj_name+' Has Been Successfully Added For Client '+prefix)
    print("*********************************************************************************************************************************")
    print('')
    #wait()
    
    
# FUNCTION TO ADD SUBCONTRACTOR WORK
def add_subcontractor():
    print('')
    print("*********************************************************************************************************************************")
    print("*************************************************** ADDING SUBCONTRACTOR WORK ***************************************************")
    print("*********************************************************************************************************************************")
    sc_name = input("Enter Name of Subcontractor: ")
    sc_job = input("Enter Project/Task of Subcontractor: ")
    sc_client = input("Enter Prefix of Client Job Done For: ")
    sc_hours = input("Enter Hours Worked: ")
    sc_rate = input("Enter Subcontractor's Rate: ")
    sc_cost = input("Enter Total Cost: ")
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''INSERT INTO subcontractors(sub_name,sub_job,for_client,sub_hours,sub_rate,sub_cost) VALUES(?,?,?,?,?,?)''',(sc_name,sc_job,sc_client,sc_hours,sc_rate,sc_cost))
    db.commit()
    db.close()
    print('')
    print("Work Successfully Added For Subcontractor "+sc_name)
    print("*********************************************************************************************************************************")
    print('')
    

###### FUNCTION TO ADD MANUAL PROJECTS ######   
def add_manual_job():
    print('')
    print("*********************************************************************************************************************************")
    print("************************************************* ADDING MANUAL/FIXED COST ITEM *************************************************")
    print("*********************************************************************************************************************************")
    man_for = input("Enter Prefix of Client Job Done For: ")
    man_date = input("Enter Item Date(s): ")
    man_job = input("Enter Name of Task: ")
    man_hours = input("Enter Hours for Task: ")
    man_rate = input("Enter Rate for Task: ")
    man_total = input("Enter Total Cost: ")
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''INSERT INTO manual_work(for_client,man_date,man_job,man_hours,man_rate,man_cost) VALUES(?,?,?,?,?,?)''',(man_for,man_date,man_job,man_hours,man_rate,man_total))
    db.commit()
    db.close()
    print('')
    print("Manual/Fixed Cost Item Successfully Added For Client "+man_for)
    print("*********************************************************************************************************************************")
    print('')
############################################# 
    

    
###### FUNCTION TO UPDATE INFORMATION FOR A CURRENT PROJECT
def update_project():
    print('')
    print("*********************************************************************************************************************************")
    print("**************************************************** EDITING CURRENT PROJECT ****************************************************")
    print("*********************************************************************************************************************************")
    client_edit = input("Enter Prefix of Client With Job to Edit: ")
    client_proj_table = client_edit+"_projects"
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM '''+client_proj_table)
    print("ID\tProject Name\t\tStart Date\tEnd Date\tTotal Time")
    for row in cursor:
        this_hour = round(float(row[4]),2)
        print('{0}:\t{1}\t\t{2}\t\t{3}\t\t{4} hrs'.format(row[0],row[1],row[2],row[3],this_hour))
    client_edit = input("Enter ID of Job to Edit: ")
    new_name = input("Enter New Name for Project (or x to cancel): ")
    new_hours = input("Enter updated total hours spent on the project (or x to cancel): ")
    if ( new_name != 'x' and new_name != 'X' ):
        cursor.execute('''UPDATE '''+client_proj_table+''' SET proj_name = ? WHERE id = ? ''',(new_name, client_edit))
    if ( new_hours != 'x' and new_hours != 'X' ):
        cursor.execute('''UPDATE '''+client_proj_table+''' SET proj_time = ? WHERE id = ? ''',(new_hours, client_edit))
    db.commit()
    db.close()
    print("*********************************************************************************************************************************")
    print('')
#############################################    
    
    
    

# FUNCTION TO PICK CLIENT AND PROJECT TO TRACK
def track_current_project():
    print('')
    print("*********************************************************************************************************************************")
    print("******************************************************* PROJECT TRACKING ********************************************************")
    print("*********************************************************************************************************************************")
    prefix = input("Enter Prefix of Client to Track: ")
    if ( prefix == 'X' or prefix == 'x' ):
        return 
    client_proj_table = prefix+"_projects"
    #connect to db
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM '''+client_proj_table)
    for row in cursor:
        print('{0}: {1}'.format(row[0],row[1]))
    db.commit()
    db.close()
    ptt = input("Select ID Number of Project to Track: ")
    if ( ptt == 'X' or ptt == 'x' ):
        return
    begin_tracking_project(prefix, ptt)
    
    
# FUNCTION TO STOP TRACKING PROJECT    
def end_tracking_project(prefix_in,ptt_in,hours_in):
    client_proj_table = prefix_in+"_projects"
    today = datetime.datetime.today().day
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT proj_time FROM '''+client_proj_table+''' WHERE id = ? ''',(ptt_in,))
    for row in cursor:
        current = '{0}'.format(row[0])
    new_time = float(current) + hours_in
    cursor.execute('''UPDATE '''+client_proj_table+''' SET proj_time = ? WHERE id = ? ''',(new_time, ptt_in))
    cursor.execute('''UPDATE '''+client_proj_table+''' SET date_end = ? WHERE id = ? ''',(today, ptt_in))
    db.commit()
    db.close()
    print("*********************************************************************************************************************************")
    print('')

    
                                                                                       
## FUNCTION TO BEGIN TRACKING TIME FOR A CURRENT PROJECT                                
def begin_tracking_project(prefix_in, ppt_in):

    # Timestamp when work begins
    startTime = datetime.datetime.now()
    print("")
    print("Start Time: "+str(startTime.strftime("%H:%M:%S")))
    input("Press Enter to Stop Tracking...") 
    # Timestamp when work ends
    endTime = datetime.datetime.now()
    print("End Time: "+str(endTime.strftime("%H:%M:%S")))
    
    # Figure the total time worked
    totalTime = endTime - startTime
    seconds= totalTime.total_seconds()
    hoursWorked = seconds/3600
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    totalString = "Total Time Added - "
    if hours >= 1:
        totalString = totalString + "Hours: "+str(round(hours,2))+" ,"
    
    print(totalString+" Minutes: "+str(round(minutes,2))+" , Seconds: "+str(round(seconds,2)))
    db = sqlite3.connect(pt_db)
    cursor = db.cursor()
    cursor.execute('''SELECT client_hourly FROM all_clients WHERE client_prefix = ? ''',(prefix_in,))
    for row in cursor:
        hourly = '{0}'.format(row[0]) 
    db.commit()
    db.close()
    print("Total Charges: $" + str(round(hoursWorked * float(hourly),2)))
    end_tracking_project(prefix_in,ppt_in,hoursWorked)

      
# FUNCTION TO PRINT OUT A PAYPERIOD REPORT FOR SPECIFIED CLIENT    
def view_reports():
    print('')
    print("*********************************************************************************************************************************")
    print("******************************************* VIEWING REPORTS FOR CURRENT BILLING PERIOD ******************************************")
    print("*********************************************************************************************************************************")
    prefix = input("Enter Prefix of Client to Get Pay Period Report: ")
    if( prefix == 'x' or prefix == 'X' ):
        return
    print('')
    client_proj_table = prefix+"_projects"
    index = 1
    long_len = 0
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
        this_len = len(row[1])
        if this_len > long_len:
            long_len = this_len
    # Get lengths of manual tasks
    cursor.execute('''SELECT * FROM manual_work WHERE for_client = ? ''',(prefix,))   
    for row in cursor:
        this_len = len(row[3])
        if this_len > long_len:
            long_len = this_len       
    title_tab = get_tabs(long_len - 12 )
    #print( long_len - 12)
    print("ID\tProject Name"+title_tab+"Start\tEnd\tTotal Time\tTotal Cost")
    cursor.execute('''SELECT * FROM '''+client_proj_table)
    for row in cursor:
        len_diff = int(long_len) - int(len(row[1]))
        tab = get_tabs(len_diff)
        #print(len_diff)
        this_hour = round(float(row[4]),2)
        this_cost = round(this_hour*float(hourly),2)
        total_hours = total_hours + this_hour
        total_cost = total_cost + this_cost
        print('{0}:\t{1}'.format(index,row[1])+tab+'{0}\t{1}\t{2} hrs\t${3}'.format(row[2],row[3],format(this_hour, '.2f'),format(this_cost,'.2f')))
        index = index + 1
    db.commit()
    db.close()
    
    # Get Manual Hours/costs
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM manual_work WHERE for_client = ? ''',(prefix,))
    for row in cursor:
        len_diff = int(long_len) - int(len(row[3]))
        tab = get_tabs(len_diff)
        #print(len_diff)
        
        # Check if the type is a string and do not convert to float
        if isinstance(row[4], str):
            this_hour = str(row[4])
        else:
            this_hour = round(float(row[4]),2)
            this_hour = format(this_hour, '.2f')
            total_hours = round(float(total_hours),2) + round(float(this_hour),2)
        
        if isinstance(row[6],str):
            this_cost = str(row[6])
            print('{0}:\t{1}'.format(index,row[3])+tab+'-\t-\t{0}\t{1}'.format(this_hour,format(this_cost)))
        else:
            this_cost = round(float(row[6]),2)
            total_cost = total_cost + this_cost
            print('{0}:\t{1}'.format(index,row[3])+tab+'-\t-\t{0} hrs\t${1}'.format(this_hour,format(this_cost,'.2f')))
        index = index + 1
    db.commit()
    db.close()
        
    print('')
    print("Total Hours Worked This Pay Period: " + str(total_hours) + " Hours")
    print("Total Charges This Pay Period: $" + str(total_cost))
    print("*********************************************************************************************************************************")
    print('')
    #wait()
    
    
###### FUNCTION TO DELETE PROJECTS ######      
def delete_project_s():
    print('')
    db = sqlite3.connect(pt_db)
    # Get a cursor object
    cursor = db.cursor()
    prefix = input("Enter Prefix of Client to Delete Project(s): ")
    print('')
    client_proj_table = prefix+"_projects"
    allornot = input("Do You want to Clear all Projects for "+prefix+"? (Y/N): ")
    if allornot == "Y":
        cursor.execute('''DELETE FROM '''+client_proj_table)
        cursor.execute('''DELETE FROM subcontractors WHERE for_client = ?''',(prefix,))
        cursor.execute('''DELETE FROM manual_work WHERE for_client = ?''',(prefix,))
        print("All Projects Cleared for "+prefix)
        print('')
    elif allornot == "N":
        cursor.execute('''SELECT * FROM '''+client_proj_table)
        print("ID\tProject Name\t\tStart Date\tEnd Date\tTotal Time")
        for row in cursor:
            this_hour = round(float(row[4]),2)
            print('{0}:\t{1}\t\t{2}\t\t{3}\t\t{4} hrs'.format(row[0],row[1],row[2],row[3],this_hour))
        to_delete = input("Enter IDs of Projects to be Deleted (EX: 1,2,3): ")
        indiv_delete = to_delete.split(',', 1)
        for indiv in indiv_delete:
            cursor.execute('''DELETE FROM '''+client_proj_table+''' WHERE id = ? ''',(indiv,))
        print('Tasks Deleted for Client '+prefix)
        
    db.commit()
    db.close()
    print('')
    
        
    
    
###############################################################################

def deploy_updates():
    print("...deploying updates...")
    
  
    
    #connect to db
    db = sqlite3.connect(pt_db)

    # Get a cursor object
    cursor = db.cursor()
    #cursor.execute('''ALTER TABLE subcontractors ADD COLUMN sub_cost''')
    #cursor.execute('''ALTER TABLE all_clients ADD COLUMN address_2 string''')
    #cursor.execute('''UPDATE all_clients SET address_2 = ? WHERE client_prefix = ? ''',("", ""))
    #cursor.execute('''UPDATE all_clients SET address_1 = ? WHERE client_prefix = ? ''',("", ""))
    #cursor.execute('''UPDATE all_clients SET client_name = ? WHERE client_prefix = ? ''',("", ""))
    #cursor.execute('''UPDATE all_clients SET client_hourly = ? WHERE client_prefix = ? ''',(, ""))
    #cursor.execute('''UPDATE all_clients SET client_hourly = ? WHERE client_prefix = ? ''',(, "P"))
    #cursor.execute('''UPDATE all_clients SET address_2 = ? WHERE client_prefix = ? ''',("", ""))
    #cursor.execute('''CREATE TABLE manual_work(id INTEGER PRIMARY KEY, for_client TEXT, man_date TEXT, man_job TEXT, man_hours FLOAT, man_rate FLOAT, man_cost FLOAT)''')
    #cursor.execute('''CREATE TABLE all_clients(id INTEGER PRIMARY KEY, client_name TEXT, client_prefix TEXT, client_hourly DOUBLE)''')
    #cursor.execute('''UPDATE SWP_projects SET proj_time = ? WHERE id = ? ''',(.2, 11))
    db.commit()
    db.close()



   
    
#main program  
while True:
    run = wait()
    if (run == "quit"):
        break



