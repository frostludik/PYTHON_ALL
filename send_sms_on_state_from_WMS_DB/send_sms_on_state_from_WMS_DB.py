"""
author: Ludek Mraz
email: ludek.mraz@centrum.cz
discord: Luděk M.#5570
"""

# This code runs SQL query against WMS's Oracle database
# If query is evaluated as True, it sends SMS
    # check status via SQL every 2 mins, if True, sends SMS
    # check when last SMS been sent
    # re-sends SMS not earlier than 15 mins after previous one
    # possible to break the loop with Ctrl+C
    # check runs only within specific time frame (6:00 - 22:00)

# you can create exe file with pyinstaller to run it on Windows without Python installed in console 
#       -> pyinstaller --onefile --console --hidden copy_astro_sms.py
# or run it in console with Python installed
#       -> install python 3.8 or higher
#       -> install required packages: pip install oracledb, pip install requests
#       -> run the script: python copy_astro_sms.py

#### 2024-02-28 changed: merged send_sms and admin_send_sms into one function execute_sms
#### 2024-05-23 changed: database credentials moved to config file


import oracledb
import requests
import time
import datetime
import json
import sys
import configparser

sms_message = "Some packages are missing TRACKNO"
admin_sms_message = "trackno SMS - failed connecting to database"
recipients = ["+420123456789"] 
admin_recipient = "+420123456789"
api_url = "https://api.services.company.com/iam/proxy/sms/manual/paths/invoke"
headers = {"Ocp-Apim-Subscription-Key": "YOUR_API_KEY"}


send_sms = False

query = """
    Select O40T2.upddate, O40T2.ecarrno, O40T92.trackno 
    FROM O40T2
    LEFT JOIN O40T92 ON O40T2.ecarrno = O40T92.ecarrno
    WHERE stato40 IN ('70','80','85')
    AND O40T92.trackno IS NULL
    AND O40T2.upddate < (sysdate - interval '2' minute)
    AND ocarrtyp NOT IN ('DPTOP','DPMPE','EUR')
    """
    

def print_with_timestamp(msg):
    '''
    gives timestamp to every print statement
    '''
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"[{timestamp}] {msg}")   
    
    
        
def db_connect(retry_interval=30, max_attempts=5):
    '''
    connects to Oracle database
    If fails, retries connection in 30 sec intervals for 5 times
    if still fails, sends admin SMS and exits the program
    '''
    config = configparser.ConfigParser()
    config.read(r"C:\send_sms_config\config.ini")
    user = config["oracle_database"]["user"]
    password = config["oracle_database"]["password"]
    hostname = config["oracle_database"]["hostname"]
    attempt_count = 0
    while attempt_count < max_attempts:
        try:
            global oracle_connect
            oracle_connect = oracledb.connect(user + "/" + password + "@" + hostname)
            print_with_timestamp("Successfully connected to Oracle Database")
            return
            
        except oracledb.DatabaseError as error:
            attempt_count += 1
            print_with_timestamp(f"Attempt {attempt_count} failed. Error connecting to Oracle database: {error}")
            if attempt_count < max_attempts:
                print_with_timestamp(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                execute_sms(admin_recipient, is_admin=True)
                print_with_timestamp("\n\n!!!Try different network with access to company resources!!!")
                input("Press enter to exit...")
                sys.exit()
   
              
            
def run_sql(query):
    '''
    runs SQL query saved in variable, returns bool depeding
    if get any result or not
    '''
    cursor = oracle_connect.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    return bool(row)



def update_send_sms():
    '''
    updates send_sms variable based on run_sql function result
    '''
    global send_sms
    send_sms = run_sql(query)
    
  
       
def run_check_loop():
    '''
    runs the main program process
    -connection to database
    -check result
    -check whether to send SMS or not
    '''
    db_connect()
    update_send_sms()
    oracle_connect.close()
    print_with_timestamp("Database closed")
    print_with_timestamp(f"Send SMS: {send_sms}")
    print_with_timestamp("Waiting 120s for next check...\n")


   
def execute_sms(recipients, is_admin=False):
    '''
    sends SMS
    if is_admin is True, sends admin SMS    
    if is_admin is False, sends SMS to recipients
    '''
    correlation_id = ""
    component = "AstroELDC"
    if is_admin:
        event_type = "Failed connect to database"
        message = "trackno SMS - failed connecting to database"
        recipients = [admin_recipient] 
    else:
        event_type = "Missing TRACKNO"
        message = "Some packages are missing TRACKNO"

    for recipient in recipients:
        payload = {
            "to": recipient,
            "message": message,
            "correlationId": correlation_id,
            "component": component,
            "eventType": event_type
        }
        
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 202:
            response_data = response.json()
            service_message_id = response_data.get("serviceMessageId", "N/A")
            workflow_run_id = response_data.get("workflowRunId", "N/A")
            print_with_timestamp(f"SMS queued for {recipient}. Message ID: {service_message_id}, Workflow ID: {workflow_run_id}")
        elif response.status_code == 500:
            response_data = response.json()
            service_description = response_data.get("serviceDescription", "N/A")
            service_status = response_data.get("serviceStatus", "N/A")
            workflow_run_id = response_data.get("workflowRunId", "N/A")
            print_with_timestamp(f"Error sending SMS to {recipient}. Description: {service_description}, Status: {service_status}, Workflow ID: {workflow_run_id}")
        else:
            print_with_timestamp(f"Failed to send SMS to {recipient}. Status code: {response.status_code} - {response.text}")



def run_loop():
    '''
    -runs the loop with main program
    -check status via SQL every 2 mins
        -if True, sends SMS
    -check when last SMS been sent
        -re-sends SMS not earlier than 15 mins after previous one
    -possible to break the loop with Ctrl+C
    '''
    last_triggered_time = 0
    
    while True:
        try:
            start_time = datetime.time(5, 59, 0)
            end_time = datetime.time(22, 0, 0)
            now = datetime.datetime.now().time()
            if start_time <= now <= end_time:
                run_check_loop()
                if send_sms:
                    current_time = time.time()
                    if current_time - last_triggered_time > 900:  #send SMS not earlier than 15 mins after previous one
                        execute_sms(recipients)
                        print_with_timestamp(f"time since last sms: {current_time - last_triggered_time} , waiting 120s for next check...\n")
                        last_triggered_time = current_time
                    else:
                        print_with_timestamp("!!!SMS NOT SENT. Too short time for re-sending!!!")
                        print_with_timestamp(f"time since last sms: {current_time - last_triggered_time} Must be more than 900 sec\n")
            else:
                print_with_timestamp(f"DB check paused until {start_time}\n")
            time.sleep(120)  #check status via SQL every 2 mins
        except KeyboardInterrupt:
            break
        
        
if __name__ == "__main__":       
    run_loop()
    
    
