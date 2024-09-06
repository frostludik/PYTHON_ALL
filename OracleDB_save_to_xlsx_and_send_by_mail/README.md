# OracleDB_save_to_xlsx_and_send_by_mail.py

## Overview

This script connects to an Oracle database, extracts data, saves it to an `.XLSX` file, and sends the file via email. It includes several features such as checking the connection to the database, ensuring the existence of a temporary folder, and deleting the file after sending the email.

## Features

- **Database Connection**: Connects to an Oracle database using the `oracledb` library.
- **Data Extraction**: Extracts data from the database and saves it in an `.XLSX` file.
- **Temporary Folder Check**: Ensures the existence of the `C:\temp` folder and creates it if it does not exist.
- **Email Sending**: Sends an email with the `.XLSX` file as an attachment using the `smtplib` library.
- **File Deletion**: Deletes the file from `C:\temp` after sending the email.
- **Logging**: Logs the connection status and any errors encountered.
- **Prompts**: Includes prompts for user input to confirm dates and other details.

## Requirements

- Python 3.x
- `oracledb` library for Oracle database connectivity
- `xlsxwriter` library for creating Excel files
- `pywin32` library for Windows COM client
- `smtplib` library for sending emails

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required Python packages:
    ```sh
    pip install oracledb xlsxwriter pywin32
    ```

## Configuration

- **Database Connection**: Configure your database connection parameters in the script.
- **Email Settings**: Configure the email server, sender, and recipient details in the script.
- **File Paths**: The temporary folder and file paths are defined in the script.

## Usage

Run the script using Python:
```sh
python OracleDB_save_to_xlsx_and_send_by_mail.py
```

## Creating an Executable

To create an executable using `pyinstaller`, use the following command:
```sh
pyinstaller --onefile --console --hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2 OracleDB_save_to_xlsx_and_send_by_mail.py
```

## Error Handling

- **Database Connection**: Displays an error message if the connection to the database fails.
- **Temporary Folder**: Creates the `C:\temp` folder if it does not exist.
- **File Deletion**: Deletes the file from `C:\temp` after sending the email.