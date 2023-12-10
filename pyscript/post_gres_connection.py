import psycopg2

# Replace these with your actual database credentials
dbname = 'postgres'
user = 'postgres'
password = 'postgres'
host = '127.0.0.1'
port = '5432'  # Default PostgreSQL port

try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # Example: Execute a SQL query
    cursor.execute("SELECT version();")

    # Fetch the result
    db_version = cursor.fetchone()
    print(f"PostgreSQL database version: {db_version}")

    # Don't forget to close the cursor and connection
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")