import psycopg2

import psycopg2
# Connect to your PostgreSQL server
conn = psycopg2.connect(
    dbname="fitness_coach", 
    user="arnav", 
    password="Arnav@1234", 
    host="localhost", 
    port="5432"                   # default PostgreSQL port
)

# Create a cursor object
cursor = conn.cursor()

# Execute a simple query
cursor.execute("SELECT version();")

# Fetch the result
result = cursor.fetchone()
print("Connected to:", result)

# Close the cursor and connection
cursor.close()
conn.close()

