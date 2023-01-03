#!/usr/bin/python3
######################################################################
# File Name: config_vars.py
#
# Description: Program configuration variables
#
# File History
# 03/14/2021 - Andrew Yoder : Initial Release
# 11/06/2021 - Andrew Yoder : Specifically call out python3
# 01/03/2023 - Andrew Yoder : Updated to pull provider details from database
#                             instead of being hardcoded in this file
######################################################################

import sqlite3

from platform_config import pt_db

 #connect to db and fetch all contents
db = sqlite3.connect(pt_db)
cursor = db.cursor()
cursor.execute('''SELECT * FROM provider_details''')
provider_details_data = cursor.fetchall()

    # Print all clients and information
for provider in provider_details_data:
    provider_name = provider[1]
    provider_title = provider[2]
    provider_phone = provider[3]
    provider_email = provider[4] 
    provider_location = provider[5] + ", " + provider[6] + ", " + provider[7]
    paypal_link = provider[8]