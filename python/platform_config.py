#!/usr/bin/python3
######################################################################
# File Name: platform_config.py
#
# Description: Configure settings for various platforms
#
# File History:
# 03/14/2021 - Andrew Yoder : Initial Release
# 03/29/2021 - Andrew Yoder : Updated USER to get username from the system
# 09/28/2021 - Andrew Yoder : Removed client spreadsheet definitions. No longer used
# 11/06/2021 - Andrew Yoder : Specifically call out python3
# 12/22/2022 - Andrew Yoder : Added support for MacOS
#                           : Added command per-platform to launch documents programmatially
######################################################################

import platform, os

# Get the Operating System and set paths
this_os = platform.system()

# Get the username from the system
username = os.environ['USER']

# Get the user's $HOME from the system
home_dir = os.environ['HOME']

# Windows
if ( this_os == "Windows" ):
    pt_base_dir = "C:\\Users\\USER\\Documents\\FLSW"
    db_dir = pt_base_dir + "\\database\\"
    img_dir = pt_base_dir + "\\images\\"
    Freelance_home = "C:\\Users\\USER\\Documents\\Freelancing\\"
    open_cmd = "start"
    
# Linux
elif ( this_os == "Linux" ):
    pt_base_dir = "/opt/project-tracker/"
    db_dir = pt_base_dir + "/database/"
    img_dir = pt_base_dir + "/images/"
    Freelance_home = home_dir + "/Freelancing/"
    open_cmd = "/usr/bin/xdg-open"

# MacOS
elif ( this_os == "Darwin" ):
    this_os = "MacOS"
    pt_base_dir = "/opt/project-tracker/"
    db_dir = pt_base_dir + "/database/"
    img_dir = pt_base_dir + "/images/"
    Freelance_home = home_dir + "/Freelancing/"
    open_cmd = "/usr/bin/open"
    
# Other/Unsupported
else:
    print( "Unrecognized Platform: " + str( this_os ) )
    quit()

# The Database
pt_db = db_dir + "project-tracker.sqlite"
