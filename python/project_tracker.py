#!/usr/bin/python3
######################################################################
# File History
# 03/14/2021 - Andrew Yoder : Initial Release
# 09/25/2021 - Andrew Yoder : Relocated add_new_client to new Client Manager Utility
#                           : Removed hidden deploy updates functionality
#                           : Moved wait() functionality to __main__ and removed commented out calls to wait()
#                           : Added .upper() to __main__ actions to make case insensitive
# 10/03/2021 - Andrew Yoder : Deprecated "add_subcontractor" capability. Covered by manual line item functionality
# 11/06/2021 - Andrew Yoder : Specifically call out python3
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
    

    
# main program  
if __name__ == "__main__":

    while True:

        print("")
        print("Track A Current Project: T")
        print("Add A New Project: NP")
        print("View Project Reports: R")
        print("Delete Project(s): D")
        print("Add Manual/Fixed Task: M")
        print("Edit a Current Project: E")
        print("Quit Program: Q")
        action = input("What Would You Like To Do? ").upper()

        if ( action == "T" ):
            track_current_project()
        elif ( action == "NP" ):
            add_new_project()
        elif ( action == "R" ):
            view_reports()
        elif ( action == "Q" ):
            break
        elif ( action == "D" ):
            delete_project_s()
        elif ( action == "M" ):
            add_manual_job()
        elif ( action == "E" ):
            update_project()
        else:
            print('')
            print("Did not recognize that option, please try again")
