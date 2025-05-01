# CLI FinTrack

CLI FinTrack is a console-based personal expense tracker application built with Python and MySQL. The application allows users to manage their expenses efficiently by adding, viewing, and deleting expenses, generating reports, and more.

## Features
- **User Registration & Login**: Allows users to register and login with their credentials.
- **Add Expense**: Users can add expenses, specifying the amount, category, date, and optional notes.
- **View Expenses**: View a list of all expenses, with the option to filter by date or category.
- **Delete Expense**: Users can delete an expense by its ID.
- **Generate Report**: View a summary of total expenses.
- **Weekly Summary**: View weekly breakdowns of expenses.

## Technologies Used
- **Python**: Main programming language.
- **MySQL**: Database used for storing user and expense data.
- **MySQL Connector**: Python library used to interact with MySQL databases.

## Installation

### Prerequisites

Before running the project, make sure you have the following installed:
- Python 3.x
- MySQL Server
- MySQL Connector for Python

### Steps to Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/CLI-FinTrack.git
   cd CLI-FinTrack


2. **Install MySQL Connector**:
   ```bash
   pip install mysql-connector-python

3. pip install mysql-connector-python

Set up the MySQL Database:

    Open the MySQL terminal and create a new database:

CREATE DATABASE IF NOT EXISTS fintrack;
USE fintrack;

Create the expenses table (if not already created):

    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        amount FLOAT NOT NULL,
        category VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        note TEXT
    );

Update Database Credentials: Open CLI FinTrack.py and update the database connection details (host, user, password) as per your MySQL setup.

Run the application: After setting up the database, you can run the Python script:

python CLI_FinTrack.py   
