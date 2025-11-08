import os
import pymysql.cursors

# --- Configuration (Based on your Docker setup) ---
# It's best practice to read sensitive data from environment variables.
# You will need to set these variables in your Codespace environment or locally.

DB_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")  # '127.0.0.1' when running Docker locally
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "my_strong_password") # IMPORTANT: Match this to your Docker run command!
DB_NAME = os.getenv("MYSQL_DATABASE", "my_app_db") # Use the DB name you created in Step 4

TABLE_NAME = "items"

def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor # Returns results as dictionaries
        )
        print("✅ Database connection successful.")
        return connection
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"   Please ensure the MySQL container is running on host {DB_HOST}.")
        return None

def setup_and_insert_test_records():
    """Creates the table and inserts test data."""
    connection = get_db_connection()
    if connection is None:
        return

    try:
        with connection.cursor() as cursor:
            # 1. Create Table (if it doesn't exist)
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description VARCHAR(255),
                quantity INT DEFAULT 0
            )
            """
            cursor.execute(create_table_sql)
            print(f"✅ Table '{TABLE_NAME}' ensured.")
            
            # 2. Insert Test Records
            insert_sql = f"""
            INSERT INTO {TABLE_NAME} (name, description, quantity) VALUES 
            (%s, %s, %s)
            """
            
            test_data = [
                ("Laptop", "High-performance laptop.", 5),
                ("Mouse", "Ergonomic wireless mouse.", 20),
                ("Keyboard", "Mechanical keyboard with RGB.", 15)
            ]

            # Clear existing data for a clean test run (optional)
            # cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}") 

            for record in test_data:
                cursor.execute(insert_sql, record)
            
            connection.commit()
            print(f"✅ Successfully inserted {len(test_data)} test records into '{TABLE_NAME}'.")

            # 3. Read (Test the data was added)
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            records = cursor.fetchall()
            print("\nTest Records in Database:")
            for record in records:
                print(f"  ID: {record['id']}, Name: {record['name']}, Qty: {record['quantity']}")

    except Exception as e:
        print(f"❌ An error occurred during setup: {e}")
        connection.rollback()
    finally:
        connection.close()
        print("\nDatabase connection closed.")

if __name__ == '__main__':
    setup_and_insert_test_records()
