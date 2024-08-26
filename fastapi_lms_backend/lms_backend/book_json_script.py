import pymysql
import json
import os

# Database connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123',
    database='lib_mgmt_sys'
)

# Define the list of tables and corresponding file names
tables = {
    'book': 'dump_data/book.json',
    'user': 'dump_data/user.json',
    'book_request': 'dump_data/book_request.json'
}

# Ensure the output directory exists
os.makedirs('dump_data', exist_ok=True)

try:
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        for table, file_path in tables.items():
            # Fetch data from the current table
            sql = f"SELECT * FROM {table}"
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Convert to JSON and write to the corresponding file
            with open(file_path, 'w') as json_file:
                json.dump(rows, json_file, indent=4)

            print(
                f"Data from table '{table}' has been written to '{file_path}'")

except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()
