#!/usr/bin/env python
######################################################################
# File History
# 09/25/2021 - Andrew Yoder: Initial Release
######################################################################

import sqlite3

from platform_config import pt_db


# Function to select a client out of the list of current clients
def select_a_client():

    #connect to db and fetch all current clients
    db = sqlite3.connect(pt_db)
    cursor = db.cursor()
    cursor.execute('''SELECT client_name FROM all_clients''')
    all_client_names = sorted( cursor.fetchall() )

    # Print out all clients
    print("Listing all current clients below:")
    for client_name in all_client_names:
        print( " - " + client_name[0] )

    # Prompt for client selection and return to caller
    selected_client = input("Select a client listed above: ").strip()
    return selected_client


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
    
    print('New Client ' + new_client_name + ' Has Been Successfully Added')
    print("*********************************************************************************************************************************")
    print('')


# Function to Remove a current client from the system
def remove_client():
    print("")
    print("*********************************************************************************************************************************")
    print("********************************************************** REMOVE CLIENT ********************************************************")
    print("*********************************************************************************************************************************") 
    print("")

    # Get name of client to remove
    client_to_delete = select_a_client()

    db = sqlite3.connect(pt_db)
    cursor = db.cursor()

    # Get confirmation before deleting
    client_delete_info = cursor.execute('''SELECT client_prefix FROM all_clients WHERE client_name = ?''', (client_to_delete,)).fetchall()
    for row in client_delete_info:
        client_to_delete_prefix = row[0]

    confirm_delete = input("About to remove client '" + client_to_delete + "' from system. Enter 'YES' to confirm: ")
    if ( confirm_delete.upper() == "YES" ):
        # Delete client from all_clients table
        cursor.execute('''DELETE FROM all_clients WHERE client_name = ?''', (client_to_delete,))
        # Delete the client's project table
        client_project_table = client_to_delete_prefix + "_projects"
        cursor.execute('''DROP TABLE ''' + client_project_table )
    else:
        print("Client removal not confirmed. Skipping removal")

    db.commit()
    db.close()

    print("*********************************************************************************************************************************")
    print("")



# Function to view all clients and information
def view_all_clients():
    print("")
    print("*********************************************************************************************************************************")
    print("******************************************************* VIEWING ALL CLIENTS *****************************************************")
    print("*********************************************************************************************************************************") 
    print("")

    #connect to db and fetch all contents
    db = sqlite3.connect(pt_db)
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM all_clients''')
    all_client_data = cursor.fetchall()

    # Print all clients and information
    for iteration, row in enumerate(all_client_data):
        client_id          = str(iteration + 1).zfill(2)
        client_name        = str(row[1])
        client_abbrev      = str(row[2])
        client_hourly_rate = format(row[3], '.2f')
        client_addr_one    = str(row[4])
        client_addr_two    = str(row[5])

        print( client_id + ". Client Name: " + client_name + ", (" + client_abbrev + ")" )
        print( "    Client Hourly Rate: $" + client_hourly_rate )
        print( "    Client Billing Address:" )
        print( "      " + client_addr_one )
        print( "      " + client_addr_two )
        print( "" )
        print( "-------------------------------" )
        print( "" )

    db.close()
    print("*********************************************************************************************************************************")
    print("")


# Function to Edit a current client
def edit_client():
    print("")
    print("*********************************************************************************************************************************")
    print("***************************************************** EDIT CLIENT INFORMATION ***************************************************")
    print("*********************************************************************************************************************************") 
    print("")

    # Make selection of client to edit
    client_to_edit = select_a_client()

    db = sqlite3.connect(pt_db)
    cursor = db.cursor()
    
    # Gather all current details for the client selected
    current_client_name = cursor.execute('''Select * FROM all_clients WHERE client_name = ?''',(client_to_edit,) ).fetchall()
    for row in current_client_name:

        # Edit Client Name
        print("")
        print( "Current client name: " + str(row[1]) )
        new_client_name = input( "Press enter to accept the current value or type new value: ")
        if ( new_client_name != "" ):
            cursor.execute('''UPDATE all_clients SET client_name = ? WHERE client_name = ? ''',(new_client_name, client_to_edit))

        # Edit Client Abbreviation
        print("")
        print( "Current client abbreviation: " + str(row[2]) )
        new_client_abbrev = input( "Press enter to accept the current value or type new value: ")
        if ( new_client_abbrev != "" ):
            cursor.execute('''UPDATE all_clients SET client_prefix = ? WHERE client_name = ? ''',(new_client_abbrev, client_to_edit))

        # Edit Client Hourly Rate
        print("")
        print( "Current client hourly rate: " + str(row[3]) )
        new_client_hourly = input( "Press enter to accept the current value or type new value: ")
        if ( new_client_hourly != "" ):
            cursor.execute('''UPDATE all_clients SET client_hourly = ? WHERE client_name = ? ''',(new_client_hourly, client_to_edit))

        # Edit Client Address Line 1
        print("")
        print( "Current client address line 1: " + str(row[4]) )
        new_client_addr_one = input( "Press enter to accept the current value or type new value: ")
        if ( new_client_addr_one != "" ):
            cursor.execute('''UPDATE all_clients SET address_1 = ? WHERE client_name = ? ''',(new_client_addr_one, client_to_edit))

        # Edit Client Address Line 2
        print("")
        print( "Current client address line 2: " + str(row[5]) )
        new_client_addr_two = input( "Press enter to accept the current value or type new value: ")
        if ( new_client_addr_two != "" ):
            cursor.execute('''UPDATE all_clients SET address_2 = ? WHERE client_name = ? ''',(new_client_addr_two, client_to_edit))

    # Commit Changes and close DB
    db.commit()
    db.close()

    print("")
    print("*************************************************************************************************************************************")
    print("")





# main program  
if __name__ == "__main__":

    while True:

        print("")
        print("Add A New Client: A")
        print("Edit a Current Client: E")
        print("Remove a Client: R")
        print("View All Clients: V")
        print("Quit Program: Q")
        action = input("What Would You Like To Do? ").upper()

        if ( action == "A" ):
            add_new_client()
        elif ( action == "E" ):
            edit_client()
        elif ( action == "R" ):
            remove_client()
        elif ( action == "V" ):
            view_all_clients()
        elif ( action == "Q" ):
            break
        else:
            print("")
            print("Did not recognize that option, please try again")
