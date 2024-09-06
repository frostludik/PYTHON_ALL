# send_sms_on_state_from_WMS_DB.py

## Overview

This script monitors a database for specific states and sends SMS notifications based on the state changes. It runs in a loop, checking the database every 2 minutes and sending SMS messages if certain conditions are met.

## Features

- **Database Monitoring**: Checks the database for specific states at regular intervals.
- **SMS Notification**: Sends SMS messages to predefined recipients when certain conditions are met.
- **Rate Limiting**: Ensures that SMS messages are not sent more frequently than every 15 minutes.
- **Operational Hours**: Only runs checks and sends SMS messages between 6:00 AM and 10:00 PM.
- **Graceful Shutdown**: Can be stopped gracefully using `Ctrl+C`.

## Requirements

- Python 3.x
- `requests` library for making HTTP requests
- Database client library (oracledb)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required Python packages:
    ```sh
    pip install requests
    ```

3. Ensure you have the necessary database client library installed (oracledb).

## Configuration

- **Database Connection**: Configure your database connection parameters in the script.
- **Recipients**: Define the list of recipients for the SMS notifications.
- **SMS API**: Configure the SMS API endpoint and authentication details.

## Usage

Run the script using Python:
```sh
python send_sms_on_state_from_WMS_DB.py
```

## Functions

`run_loop()`

- **Description:** Main loop that checks the database and sends SMS notifications.
- **Operational Hours:** Runs between 6:00 AM and 10:00 PM.
- **Rate Limiting:** Ensures SMS messages are not sent more frequently than every 15 minutes.
- **Graceful Shutdown:** Can be interrupted using Ctrl+C.

`execute_sms(recipients)`

- **Description:** Sends SMS messages to the specified recipients.
- **Parameters:** `recipients` - List of recipient phone numbers.

`print_with_timestamp(message)`

- **Description:** Prints a message with a timestamp.
- **Parameters:** `message` - The message to print.

## Error Handling

- **500 Status Code:** Logs detailed error information including service description and status.
- **Other Status Codes:** Logs the status code and response text.