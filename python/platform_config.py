#!/usr/bin/python
######################################################################
# File History
# 03/14/2021 - Andrew Yoder: Initial Release
# 03/29/2021 - Andrew Yoder: Updated USER to get username from the system
######################################################################

import platform, os

# Get the Operating System and set paths
this_os = platform.system()

# Get the username from the system
username = os.environ['USER']

# Windows
if ( this_os == "Windows" ):
    pt_base_dir = "C:\\Users\\USER\\Documents\\FLSW"
    db_dir = pt_base_dir + "\\database\\"
    img_dir = pt_base_dir + "\\images\\"
    spreadsheet_dir = pt_base_dir + "\\spreadsheets\\"
    Freelance_home = "C:\\Users\\USER\\Documents\\Freelancing\\"
    
# Linux
elif ( this_os == "Linux" ):
    pt_base_dir = "/opt/project-tracker/"
    db_dir = pt_base_dir + "/database/"
    img_dir = pt_base_dir + "/images/"
    spreadsheet_dir = pt_base_dir + "/spreadsheets/"
    Freelance_home = "/home/" + username + "/Freelancing/"
    
# Other/Unsupported
else:
    print("Unrecognized Platform")
    quit()

# The Database
pt_db = db_dir + "project-tracker.sqlite"

# The Client Workbook
client_workbook = spreadsheet_dir + "clients.xlsx"
