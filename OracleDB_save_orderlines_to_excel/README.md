# OracleDB_save_orderlines_to_excel.py

## Overview

This script runs an SQL query against an Oracle database of WMS, extracts data, and saves them in an `.XLSX` file. It includes several features such as checking the connection to the destination network folder, retrying on failure, logging progress, and timestamped print statements.

## Features

- **SQL Query Execution**: Runs a predefined SQL query against an Oracle database.
- **Data Extraction**: Extracts data from the database and saves it in an `.XLSX` file.
- **Network Folder Check**: Checks the connection to the destination network folder and stops the program after 5 retries if the connection fails.
- **File Existence Check**: Checks if the file already exists before saving.
- **Logging**: Saves progress to a logfile in `C:\temp`.
- **Timestamped Print Statements**: Uses a custom function to add timestamps to print statements.

## Requirements

- Python 3.x
- `oracledb` library for Oracle database connectivity
- `openpyxl` library for working with Excel files

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required Python packages:
    ```sh
    pip install oracledb openpyxl
    ```

## Configuration

- **SQL Query**: The SQL query to be executed is defined in the `query` variable.
- **File Path**: The destination file path is defined in the `file_path` variable.
- **Log File Path**: The log file path is defined in the `log_file_path` variable.

## Usage

Run the script using Python:
```sh
python OracleDB_save_orderlines_to_excel.py
```

## Functions

`print_with_timestamp(msg, file=sys.stdout)`

- **Description**: Adds a timestamp to each print statement.
- **Parameters**:
  - `msg`: The message to print.
  - `file`: The file to which the message should be printed (default is `sys.stdout`).

## Error Handling

- **Network Folder Connection**: Retries up to 5 times with a delay of 15 seconds between retries if the connection to the network folder fails.
- **File Existence**: Checks if the file already exists before attempting to save the data.