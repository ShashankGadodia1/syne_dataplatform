import psycopg2

def connect_to_postgres(dbname, user, password, host='localhost', port='5432'):
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connected to the PostgreSQL database!")

        return conn

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Connection to PostgreSQL closed.")

# Example usage:
# Replace these with your actual database credentials

dbname = 'postgres'
user = 'postgres'
password = 'postgres'
host = '127.0.0.1'
port = '5432'

# Connect to PostgreSQL
connection = connect_to_postgres(dbname, user, password)

# Use the connection for operations...

# Don't forget to close the connection when done
close_connection(connection)