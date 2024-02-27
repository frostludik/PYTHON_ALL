"""
author: Ludek Mraz
email: ludek.mraz@centrum.cz
discord: Luděk M.#5570
"""

# This code runs SQL query against WMS Oracle database
# If query is evaluated as True, it sends SMS
    # check status via SQL every 2 mins, if True, sends SMS.
    # check when last SMS been sent
    # re-sends SMS not earlier than 15 mins after previous one
    # possible to break the loop with Ctrl+C

import oracledb
import requests
import time
import datetime
import json
import sys

sms_message = "Some packages are missing TRACKNO"
admin_sms_message = "trackno SMS - failed connecting to database"
recipients = ["+420000000000", "+420000000000"]  #list of recipients
admin_recipient = ["+420000000000"]
api_url = "https://api.services.company.com/sms/manual/paths/invoke"
headers = {"Ocp-Apim-Subscription-Key": "API product subscription key"}


send_sms = False

query = """
    Select O40T2.upddate, O40T2.ecarrno, O40T92.trackno
    FROM O40T2
    LEFT JOIN O40T92 ON O40T2.ecarrno = O40T92.ecarrno
    WHERE stato40 IN ('70','80','85')
    AND O40T92.trackno IS NULL
    AND O40T2.upddate < (sysdate - interval '2' minute)
    AND ocarrtyp NOT IN ('DPTOP','DPMPE')
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
    attempt_count = 0
    while attempt_count < max_attempts:
        try:
            global oracle_connect
            oracle_connect = oracledb.connect('USER/password@hostname:dc-wms01.dc.company.int/database05')
            print_with_timestamp("Successfully connected to Oracle Database")
            return
            
        except oracledb.DatabaseError as error:
            attempt_count += 1
            print_with_timestamp(f"Attempt {attempt_count} failed. Error connecting to Oracle database: {error}")
            if attempt_count < max_attempts:
                print_with_timestamp(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                execute_admin_sms()
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


   
def execute_sms():
    '''
    sends SMS to recipients
    '''
    correlation_id = ""
    component = "DC-WMS"
    event_type = "Missing trackingNumber"

    for recipient in recipients:
        payload = {
            "to": recipient,
            "message": sms_message,
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


def execute_admin_sms():
    '''
    sends SMS to admin recipient only
    send in case of failed connection to database
    simplified response handling
    '''
    correlation_id = ""
    component = "DC-WMS error"
    event_type = "Failed connect to database"
    
    payload = {
        "to": admin_recipient,
        "message": admin_sms_message,
        "correlationId": correlation_id,
        "component": component,
        "eventType": event_type
    }
    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 202:
        response_data = response.json()
        service_message_id = response_data.get("serviceMessageId", "N/A")
        workflow_run_id = response_data.get("workflowRunId", "N/A")
        print_with_timestamp(f"SMS queued for {admin_recipient}. Message ID: {service_message_id}, Workflow ID: {workflow_run_id}")
    elif response.status_code == 500:
        response_data = response.json()
        service_description = response_data.get("serviceDescription", "N/A")
        service_status = response_data.get("serviceStatus", "N/A")
        workflow_run_id = response_data.get("workflowRunId", "N/A")
        print_with_timestamp(f"Error sending SMS to {admin_recipient}. Description: {service_description}, Status: {service_status}, Workflow ID: {workflow_run_id}")
    else:
        print_with_timestamp(f"Failed to send SMS to {admin_recipient}. Status code: {response.status_code} - {response.text}")
        

def run_loop():
    '''
    -runs the loop with main program
    -check status via SQL every 2 mins
        -if True, sends SMS
    -check when last SMS been sent
        -re-sends SMS not earlier than 15 mins after previous one
    -possible to break the loop with Ctrl+C
    '''
    start_time = datetime.time(8, 0, 0)
    end_time = datetime.time(22, 0, 0)
    now = datetime.datetime.now().time()
    last_triggered_time = 0
    
    while True:
        try:
            if start_time <= now <= end_time:
                run_check_loop()
                if send_sms == True:
                    current_time = time.time()
                    if current_time - last_triggered_time > 900:
                        execute_sms()
                        print_with_timestamp(f"time since last sms: {current_time - last_triggered_time} , waiting 120s for next check...")
                        last_triggered_time = current_time
                    else:
                        print_with_timestamp("!!!SMS NOT SENT. Too short time for re-sending!!!")
                        print_with_timestamp(f"time since last sms: {current_time - last_triggered_time} Must be more than 900 sec")
            time.sleep(120)
        except KeyboardInterrupt:
            break
        
if __name__ == "__main__":       
    run_loop()
    
    
