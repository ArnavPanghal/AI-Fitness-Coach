from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Database connection setup
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",  # Replace with your database name
    "user": "arnav",         # Replace with your PostgreSQL username
    "password": "Arnav@1234" # Replace with your PostgreSQL password
}

def get_db_connection():
    """Establish a database connection."""
    connection = psycopg2.connect(**DB_CONFIG)
    return connection

@app.route('/')
def home():
    """Default route for API."""
    return jsonify({"message": "Welcome to the Fitness App API!"})

@app.route('/users', methods=['GET'])
def get_users():
    """Fetch all users."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.users;")
        users = cur.fetchall()
        cur.close()
        conn.close()

        # Return data as JSON
        users_list = [{"id": row[0], "name": row[1], "email": row[2], "age": row[3], "weight": row[4]} for row in users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """Fetch all workouts."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.workouts;")
        workouts = cur.fetchall()
        cur.close()
        conn.close()

        # Return data as JSON
        workouts_list = [{"id": row[0], "user_id": row[1], "date": row[2], "total_calories": row[3]} for row in workouts]
        return jsonify(workouts_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """Fetch all exercises."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.exercises;")
        exercises = cur.fetchall()
        cur.close()
        conn.close()

        # Return data as JSON
        exercises_list = [{"id": row[0], "workout_id": row[1], "exercise_name": row[2], "sets": row[3], "reps": row[4], "weight": row[5]} for row in exercises]
        return jsonify(exercises_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/muscle-map', methods=['GET'])
def get_muscle_map():
    """Fetch all muscle map entries."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.muscle_map;")
        muscle_map = cur.fetchall()
        cur.close()
        conn.close()

        # Return data as JSON
        muscle_map_list = [{"id": row[0], "workout_id": row[1], "muscle_name": row[2], "intensity": row[3]} for row in muscle_map]
        return jsonify(muscle_map_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
