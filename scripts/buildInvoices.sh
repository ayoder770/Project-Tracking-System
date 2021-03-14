#!/bin/bash
######################################################################
# File History
# 03/14/2021 - Andrew Yoder: Initial Release
######################################################################

# File Paths
FL_home="/opt/FLSW"

# Run the build pdf python script and output results to a file
python3 $FL_home/pdf.py > $FL_home/payPeriodStats.txt


# Open Zenity with the results
cat $FL_home/payPeriodStats.txt | zenity --text-info --title="Pay Period Stats" --width=500 --height=350 &


# Open the summary spreadsheet
/usr/bin/libreoffice $HOME/Freelancing/Finances/2020_totals.ods
