#!/usr/bin/python3
######################################################################
# File Name: provider_details.py
#
# Description: View and edit details of the service provider. This is
#              printed on invoices.
#
# File History
# 01/03/2023 - Andrew Yoder : Initial Release
######################################################################

import sqlite3

from platform_config import pt_db


# Function to view provider information
def view_provider_details():
    print("")
    print("*********************************************************************************************************************************")
    print("****************************************************** PROVIDER INFORMATION *****************************************************")
    print("*********************************************************************************************************************************") 
    print("")

    #connect to db and fetch all contents
    db = sqlite3.connect(pt_db)
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM provider_details''')
    provider_details_data = cursor.fetchall()

    # Print all clients and information
    for provider in provider_details_data:
      print( "Provider Name: " + provider[1] )
      print( "Provider Title: " + provider[2] )
      print( "Provider Phone Number: " + provider[3] )
      print( "Provider Email Address: " + provider[4] )
      print( "Provider City: " + provider[5] )
      print( "Provider State: " + provider[6] )
      print( "Provider Zip Code: " + provider[7] )
      print( "Provider PayPal Link: " + provider[8] )
      print( "" )

    db.close()
    print("*********************************************************************************************************************************")
    print("")


# Function to Edit provider details
def edit_provider_details():
    print("")
    print("*********************************************************************************************************************************")
    print("**************************************************** EDIT PROVIDER INFORMATION **************************************************")
    print("*********************************************************************************************************************************") 
    print("")

    db = sqlite3.connect(pt_db)
    cursor = db.cursor()
    
    # Gather all current details for the client selected
    all_providers = cursor.execute('''Select * FROM provider_details''').fetchall()
    for provider in all_providers:

        # Edit Provider Name
        print("")
        print( "Current Provider Name: " + str( provider[1] ) )
        new_prov_name = input( "Press enter to accept the current value or type new value: ")
        if ( new_prov_name != "" ):
            cursor.execute('''UPDATE provider_details SET prov_name = ? WHERE id = ? ''', ( new_prov_name, provider[0] ) )

        # Edit Provider Title
        print("")
        print( "Current Provider Title: " + str( provider[2] ) )
        new_prov_title = input( "Press enter to accept the current value or type new value: ")
        if ( new_prov_title != "" ):
            cursor.execute('''UPDATE provider_details SET prov_title = ? WHERE id = ? ''', ( new_prov_title, provider[0] ) )

        # Edit Provider Phone
        print("")
        print( "Current Provider Phone: " + str( provider[3] ) )
        new_prov_phone = input( "Press enter to accept the current value or type new value: ")
        if ( new_prov_phone != "" ):
            cursor.execute('''UPDATE provider_details SET prov_phone = ? WHERE id = ? ''', ( new_prov_phone, provider[0] ) )

        # Edit Provider Email
        print("")
        print( "Current Provider Email: " + str( provider[4] ) )
        new_prov_email = input( "Press enter to accept the current value or type new value: ")
        if ( new_prov_email != "" ):
            cursor.execute('''UPDATE provider_details SET prov_email = ? WHERE id = ? ''', ( new_prov_email, provider[0] ) )

        # Edit Provider City
        print("")
        print( "Current Provider City: " + str( provider[5] ) )
        new_prov_city = input( "Press enter to accept the current value or type new value: ")
        if ( new_prov_city != "" ):
            cursor.execute('''UPDATE provider_details SET prov_city = ? WHERE id = ? ''', ( new_prov_city, provider[0] ) )

        # Edit Provider State
        print("")
        print( "Current Provider State: " + str( provider[6] ) )
        new_prov_state = input( "Press enter to accept the current value or type new value: ")
        if ( new_prov_state != "" ):
            cursor.execute('''UPDATE provider_details SET prov_state = ? WHERE id = ? ''', ( new_prov_state, provider[0] ) )

        # Edit Provider Zip
        print("")
        print( "Current Provider Zip Code: " + str( provider[7] ) )
        new_prov_zip = input( "Press enter to accept the current value or type new value: ")
        if ( new_prov_zip != "" ):
            cursor.execute('''UPDATE provider_details SET prov_zip = ? WHERE id = ? ''', ( new_prov_zip, provider[0] ) )

        # Edit Provider PayPal Link
        print("")
        print( "Current Provider PayPal Link: " + str( provider[8] ) )
        new_prov_paypal_link = input( "Press enter to accept the current value or type new value: ")
        if ( new_prov_paypal_link != "" ):
            cursor.execute('''UPDATE provider_details SET prov_paypal_link = ? WHERE id = ? ''', ( new_prov_paypal_link, provider[0] ) )

    # Commit Changes and close DB
    db.commit()
    db.close()

    print("")
    print("*********************************************************************************************************************************")
    print("")


# main program  
if __name__ == "__main__":

    while True:

        print("")
        print("View Provider Details: V")
        print("Edit Provider Details: E")
        print("Quit Program: Q")
        action = input("What Would You Like To Do? ").upper()

        if ( action == "E" ):
            edit_provider_details()
        elif ( action == "V" ):
            view_provider_details()
        elif ( action == "Q" ):
            break
        else:
            print("")
            print("Did not recognize that option, please try again")
