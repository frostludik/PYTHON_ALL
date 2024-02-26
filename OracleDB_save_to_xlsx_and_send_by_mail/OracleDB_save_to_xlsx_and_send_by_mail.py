"""
author: Ludek Mraz
email: ludek.mraz@centrum.cz
discord: Luděk M.#5570
"""

# To create executable use "pyinstaller with following arguments: 
# --onefile --console --hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2 FILENAME.py
# Neccessary to import "secretes" module because of pyinstaller not working right with versions
# of Python and oracledb
#
# running process:
# check connection to database, if fails then displays error
# check existence of c:\temp folder, if not existing,creates it
# outputfile saved in c:\temp
# sends email using smtplib with xlsx file as attachement
# deletes the File from c:\temp

##CHANGES
##current system date added to mail subject
##added 2nd prompt, shows calculated loading date and gives option to change to another one
##added info in 2nd prompt about Plan date and option to quit if incorrect


import os
import sys
import datetime
import oracledb
import xlsxwriter
import win32com.client as win32
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import secrets 

separator = "*" * 89
seprarator2 = "*" * 26

#log in
try:
    connection = oracledb.connect(
        user="USER",
        password="password",
        dsn="dc-wms01.dc.company.int/database05")
    print("Successfully connected to Oracle Database")
    
except oracledb.DatabaseError as error:
    print(f"Error connecting to Oracle database: {error}"
    "\n\n!!!Try different network with access to company resources!!!")
    input("Press enter to exit...")
    sys.exit()


#check TEMP location
folder_name = "C:\\temp"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Temporary file location {folder_name} created successfully")
else:
    print(f"Temporary location {folder_name} already exists. Continue...")


#creating xslx
workbook = xlsxwriter.Workbook("C:\\temp\\Planning-file.xlsx")
worksheet = workbook.add_worksheet("Planning-file")


#get date imput for SQL query
prompt1 = True
while prompt1:
    req_date = input('\nSet PLAN date "DD.MM.YYYY": ')
    try:
        datetime.datetime.strptime(req_date, '%d.%m.%Y')
        prompt1 = False
    except ValueError:
        print(f"{seprarator2}\nWrong date or date format!\n{seprarator2}")


#count loading date for mail body. Depends on day name
day, month, year = map(int, req_date.split("."))
date_obj = datetime.date(year, month, day)
day_name = date_obj.strftime("%A")
plus_3_days = ["Monday", "Tuesday"]
if day_name in plus_3_days:
    loading_date = date_obj + datetime.timedelta(days=3)
else:
    loading_date = date_obj + datetime.timedelta(days=5)
    
date_obj2 = datetime.datetime.strptime(str(loading_date), "%Y-%m-%d").date()
suggested_loading_date = date_obj2.strftime("%d.%m.%Y")


#get input for loading date        
print(f"\n{separator}\nYou set {req_date} as PLAN date. If not correct,\
press Q to Exit program and start over!!!\n{separator}")
prompt2 = True
while prompt2:
    changed_loading_date = input(f"\nLOADING date should be {suggested_loading_date}\
\npress Enter to confirm or set different date 'DD.MM.YYYY': ")
    if changed_loading_date.upper() == "Q":
        sys.exit()
    elif changed_loading_date == "":
            prompt2 = False
    else:
        try:
            datetime.datetime.strptime(changed_loading_date, '%d.%m.%Y')
            prompt2 = False
        except ValueError:
            print(f"\n{seprarator2}\nWrong date or date format!\n{seprarator2}")
                 
         
if changed_loading_date == "":
    final_loading_date = suggested_loading_date
else:
    final_loading_date = changed_loading_date
    
#SQL query
query = """
    SELECT TO_CHAR(R08T1.regdate, 'DD.MM.YYYY') as regdate, R08T1.etripid, O04T1.r00key, O08T1.ordno,
    L62T1.partgrp3, L62T1.partno, COUNT(O08T1.ordline) as pcs , SUM(O08T1.realvol/1000) as volume,
    SUM(O08T1.realwght) as weight
    FROM R08T1
    LEFT JOIN O08T1 ON O08T1.shortr08 = R08T1.shortr08
    LEFT JOIN O04T1 ON O04T1.shorto04 = O08T1.shorto04
    LEFT JOIN L62T1 ON L62T1.shortl62 = O08T1.shortl62
    WHERE R08T1.tripstat NOT IN (9, 25)
    AND L62T1.partgrp3 NOT IN ('DF ACC', 'DF CUT' , 'DF EDGE')
    AND L62T1.partno LIKE 'E116%'
    AND TO_CHAR(R08T1.regdate, 'DD.MM.YYYY') =:req_date
    GROUP BY R08T1.regdate, R08T1.etripid, O04T1.r00key, O08T1.ordno, L62T1.partgrp3, L62T1.partno
    ORDER BY R08T1.regdate, R08T1.etripid, O04T1.r00key, O08T1.ordno, L62T1.partgrp3, L62T1.partno
"""
cursor = connection.cursor()
cursor.execute(query,{"req_date" : req_date})


# Write the column headers to the worksheet
column_names = ["Plan date", "ExtTripID","Route", "Order", "ArtGrp", "Article", "Pcs", "Volume m3", "Weight"]
worksheet.write_row(0, 0, column_names)


#Write the data rows to the worksheet
row_num = 1
for row in cursor:
    worksheet.write_row(row_num, 0, row)
    row_num += 1


#format data in xlsx
volume_format = workbook.add_format({"num_format": "#,##0.00"})
worksheet.set_column(0, 8, 12)
worksheet.set_column(7, 7, None, volume_format)

#close all
workbook.close()
connection.close()

#get system date in specified format
now = datetime.datetime.now()
today = now.strftime("%d.%m.%Y")

sender_email = "ludek.mraz@centrum.cz"
recipient_email = "testmail@gmail.com"
cc_email = "testmail2@gmail.com"
smtp_server = "smtp.company.com"
smtp_port = 25

# Create message object
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Cc"] = cc_email
message["Subject"] = f"Planning-file {today}"

# Add body text to email
body = f"Enclosed is planning report: Planning-file - Loading date: {final_loading_date}."
message.attach(MIMEText(body))

# Open and attach the file to email
filename = "C:\\temp\\Planning-file.xlsx"
with open(filename, "rb") as attachment:
    file_part = MIMEApplication(attachment.read(), Name="Planning-file.xlsx")
    file_part["Content-Disposition"] = f'attachment; filename="Planning-file.xlsx"'
    message.attach(file_part)

# Connect to SMTP server and send email
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.sendmail(sender_email, [recipient_email, cc_email], message.as_string())
    print("\nE-mail sent successfully!")

# Remove XLSX from temp folder
os.remove(filename)

# Wait for user close
input("Press enter to exit...")
sys.exit()