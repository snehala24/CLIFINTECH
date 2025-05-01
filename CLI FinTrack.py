import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Expense:
    def __init__(self, expense_id, amount, category, date, note=""):
        self.expense_id = expense_id
        self.amount = amount
        self.category = category
        self.date = date
        self.note = note

    def __repr__(self):
        return f"Expense(₹{self.amount}, {self.category}, {self.date}, {self.note})"

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note
        }

    @staticmethod
    def from_dict(data):
        return Expense(data["expense_id"], data["amount"], data["category"], data["date"], data["note"])

class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            return mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database
            )
        except Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def execute_query(self, query, params=()):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def fetch_records(self, query, params=()):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def initialize_database(self):
        try:
            # Check if the database exists; if not, create it
            self.execute_query(f"CREATE DATABASE IF NOT EXISTS {self.database}")

            # Create Users table
            self.execute_query("""
            CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                points INT DEFAULT 0
            );
            """)

            # Create Expenses table
            self.execute_query("""
            CREATE TABLE IF NOT EXISTS Expenses (
                expense_id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(10, 2) NOT NULL,
                category VARCHAR(255) NOT NULL,
                date DATE NOT NULL,
                note TEXT,
                user_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users (id)
            );
            """)

            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")

    # Insert a record into the database (for User registration)
    def insert_record(self, query, params=()):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid  # Return the ID of the inserted record
        except Error as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

class UserManager:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def register(self, username, email, password):
        try:
            existing_user = self.db_handler.fetch_records(
                "SELECT id FROM Users WHERE username = %s OR email = %s", (username, email)
            )
            if existing_user:
                print("Username or email already in use.")
                return None

            user_id = self.db_handler.insert_record(
                "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password),
            )
            print(f"User '{username}' registered successfully with ID {user_id}.")
            return user_id
        except Exception as e:
            print(f"Error during registration: {e}")
            return None

    def login(self, username, password):
        try:
            records = self.db_handler.fetch_records(
                "SELECT id FROM Users WHERE username = %s AND password = %s", (username, password)
            )
            if records:
                user_id = records[0][0]
                print(f"User '{username}' logged in successfully.")
                return user_id
            else:
                print("Invalid username or password.")
                return None
        except Exception as e:
            print(f"Error during login: {e}")
            return None

class ExpenseManager:
    def __init__(self, db_handler, user_id):
        self.db_handler = db_handler
        self.user_id = user_id

    def add_expense(self, amount, category, date, note=""):
        try:
            self.db_handler.execute_query(
                "INSERT INTO Expenses (amount, category, date, note, user_id) VALUES (%s, %s, %s, %s, %s)",
                (amount, category, date, note, self.user_id),
            )
            print(f"Expense of ₹{amount} in '{category}' category added successfully.")
        except Exception as e:
            print(f"Error adding expense: {e}")

    def view_expenses(self, filter_by=None, filter_value=None):
        try:
            if filter_by and filter_value:
                query = f"SELECT * FROM Expenses WHERE user_id = %s AND {filter_by} = %s"
                expenses = self.db_handler.fetch_records(query, (self.user_id, filter_value))
            else:
                query = "SELECT * FROM Expenses WHERE user_id = %s"
                expenses = self.db_handler.fetch_records(query, (self.user_id,))

            if expenses:
                print("Your Expenses:")
                for expense in expenses:
                    print(f"ID: {expense[0]}, Amount: ₹{expense[1]}, Category: {expense[2]}, Date: {expense[3]}, Note: {expense[4]}")
            else:
                print("No expenses found.")
        except Exception as e:
            print(f"Error viewing expenses: {e}")

    def delete_expense(self, expense_id):
        try:
            self.db_handler.execute_query(
                "DELETE FROM Expenses WHERE expense_id = %s AND user_id = %s", (expense_id, self.user_id)
            )
            print(f"Expense ID {expense_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting expense: {e}")

class ReportGenerator:
    def __init__(self, db_handler, user_id):
        self.db_handler = db_handler
        self.user_id = user_id

    def generate_report(self):
        try:
            total_expenses = self.db_handler.fetch_records(
                "SELECT SUM(amount) FROM Expenses WHERE user_id = %s", (self.user_id,)
            )[0][0]

            if total_expenses:
                print(f"Total Expenses: ₹{total_expenses}")
            else:
                print("No expenses recorded.")

        except Exception as e:
            print(f"Error generating report: {e}")

    def generate_weekly_summary(self):
        try:
            query = """
                SELECT SUM(amount), WEEK(date) FROM Expenses 
                WHERE user_id = %s GROUP BY WEEK(date) ORDER BY WEEK(date)
            """
            weekly_summary = self.db_handler.fetch_records(query, (self.user_id,))
            print("Weekly Expenses Summary:")
            for week, total in weekly_summary:
                print(f"Week {week}: ₹{total}")
        except Exception as e:
            print(f"Error generating weekly summary: {e}")

if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = 'Sn@240804'
    database = 'fintrack'

    db_handler = DatabaseHandler(host, user, password, database)
    db_handler.initialize_database()

    user_manager = UserManager(db_handler)
    print("1. Register\n2. Login")
    choice = int(input("Select an option: "))

    user_id = None
    if choice == 1:
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        user_id = user_manager.register(username, email, password)
    elif choice == 2:
        username = input("Enter username: ")
        password = input("Enter password: ")
        user_id = user_manager.login(username, password)

    if user_id:
        expense_manager = ExpenseManager(db_handler, user_id)
        report_generator = ReportGenerator(db_handler, user_id)

        while True:
            print("\n1. Add Expense\n2. View Expenses\n3. Delete Expense\n4. Generate Report\n5. Weekly Summary\n6. Exit")
            option = int(input("Choose an option: "))

            if option == 1:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ")
                date = input("Enter date (YYYY-MM-DD): ")
                note = input("Enter note (optional): ")
                expense_manager.add_expense(amount, category, date, note)
            elif option == 2:
                filter_by = input("Filter by (date/category): ").lower()
                if filter_by not in ["date", "category"]:
                    print("Invalid filter. Viewing all expenses.")
                    expense_manager.view_expenses()
                else:
                    filter_value = input(f"Enter {filter_by}: ")
                    expense_manager.view_expenses(filter_by, filter_value)
            elif option == 3:
                expense_id = int(input("Enter expense ID to delete: "))
                expense_manager.delete_expense(expense_id)
            elif option == 4:
                report_generator.generate_report()
            elif option == 5:
                report_generator.generate_weekly_summary()
            elif option == 6:
                break
            else:
                print("Invalid option. Please try again.")
