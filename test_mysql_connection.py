import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sn@240804'  # replace with your actual password
    )

    if connection.is_connected():
        print("✅ Connected to MySQL successfully!")

except Error as e:
    print("❌ Error while connecting to MySQL:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("🔌 Connection closed.")
