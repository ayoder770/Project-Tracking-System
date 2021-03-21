#!/usr/bin/python
######################################################################
# File History
# 03/14/2021 - Andrew Yoder: Initial Release
######################################################################

import platform

# Get the Operating System and set paths
this_os = platform.system()

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
    Freelance_home = "/home/USER/Freelancing/"
    
# Other/Unsupported
else:
    print("Unrecognized Platform")
    quit()

# The Database
pt_db = db_dir + "project-tracker.sqlite"

# The Client Workbook
client_workbook = spreadsheet_dir + "clients.xlsx"
