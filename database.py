import psycopg2

# Establish connection to PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="fitness_tracker",  # Replace with your database name
            user="postgres",           # Replace with your PostgreSQL username
            password="your_password",  # Replace with your PostgreSQL password
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Insert exercise data
def store_data(exercise_name, reps):
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = '''
        INSERT INTO exercises (exercise, reps) VALUES (%s, %s);
        '''
        cursor.execute(query, (exercise_name, reps))
        conn.commit()
        print(f"Data saved: {exercise_name}, {reps} reps")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()

# Retrieve all exercise data
def retrieve_data():
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = '''
        SELECT * FROM exercises;
        '''
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error retrieving data: {e}")
    finally:
        conn.close()
