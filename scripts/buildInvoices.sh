#!/bin/bash
######################################################################
# File History
# 03/14/2021 - Andrew Yoder: Initial Release
# 03/29/2021 - Andrew Yoder: Fixed year variable of the totals spreadsheet
######################################################################

# File Paths
FL_home="/opt/project-tracker/"

# Run the build pdf python script and output results to a file
python3 $FL_home/pdf.py > $FL_home/payPeriodStats.txt


# Open Zenity with the results
cat $FL_home/payPeriodStats.txt | zenity --text-info --title="Pay Period Stats" --width=500 --height=350 &


# Open the summary spreadsheet
year=`date +'%Y'`

/usr/bin/libreoffice $HOME/Freelancing/Finances/${year}_totals.ods