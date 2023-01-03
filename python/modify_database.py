######################################################################
# File Name: alter_db.py
#
# Description: Python functions to alter database  when needed at
#              installation time
#
# File History
# 10/02/2021 - Andrew Yoder : Initial Release
######################################################################

import sqlite3

from platform_config import pt_base_dir, db_dir, pt_db


#def create_all_clients_table():

def create_provider_details_table():   

  #connect to db
  db = sqlite3.connect(pt_db)
  # Get a cursor object
  cursor = db.cursor()
    
  # Create the table for provider details if it does not exist
  cursor.execute( '''CREATE TABLE IF NOT EXISTS provider_details ( 
                       id INTEGER PRIMARY KEY, 
                       prov_name TEXT,
                       prov_title TEXT,
                       prov_phone TEXT,
                       prov_email TEXT,
                       prov_city TEXT,
                       prov_state TEXT,
                       prov_zip TEXT,
                       prov_paypal_link TEXT 
                     ) ''' )
  db.commit()

  # Insert default row if the table is empty
  providers = cursor.execute('''SELECT * FROM provider_details''').fetchall()

  if ( len( providers ) == 0 ):

    cursor.execute( '''INSERT INTO provider_details (
                         prov_name,
                         prov_title,
                         prov_phone,
                         prov_email,
                         prov_city,
                         prov_state,
                         prov_zip,
                         prov_paypal_link ) 
                       VALUES(?,?,?,?,?,?,?,?)''', (
                         "John Doe",
                         "Provider Title",
                         "123) 456-7890",
                         "johndoe@email.com",
                         "Provider City",
                         "Provider State",
                         "12345",
                         "https://paypal.com/" )
                  )

    db.commit()

  db.close()





if ( __name__ == "__main__" ):

  #create_all_clients_table():

  # Create provider details table
  create_provider_details_table()
