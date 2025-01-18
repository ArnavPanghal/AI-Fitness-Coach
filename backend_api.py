from flask import Flask, jsonify, request , render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import psycopg2
from graph import get_calories_summary,calculate_calories_burned,get_exercise_progress



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a real secret key
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database connection setup
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",  # Replace with your database name
    "user": "arnav",         # Replace with your PostgreSQL username
    "password": "Arnav@1234" # Replace with your PostgreSQL password
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Dummy user database (replace with real database in production)
# users = {'user@example.com': {'password': 'password'}}
users = {
    'user@example.com': {'password': 'password'},
    'john.doe@example.com': {'password': 'johnpassword'},
    'jane.doe@example.com': {'password': 'janepassword'},
    'alice@example.com': {'password': 'alicepassword'},
    'bob@example.com': {'password': 'bobpassword'}
}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def get_db_connection():
    """Establish a database connection."""
    connection = psycopg2.connect(**DB_CONFIG)
    return connection

@app.route('/')
def home():
    """Default route for API."""
    return render_template('home.html')

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
    
@app.route('/pushups', methods=['GET'])
def pushups():
    return render_template('pushups.html')

@app.route('/community', methods=['GET'])
def community():
    return render_template('community.html')

@app.route('/videos', methods=['GET'])
def videos():
    return render_template('videos.html')

@app.route('/workout', methods=['GET'])
def workout():
    return render_template('workout.html')
    
# Login and Auth

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    weekly_summary = (get_calories_summary)
    return render_template('dashboard.html', weekly_summary=weekly_summary)

@app.route('/api/calories-summary', methods=['GET'])
def calories_summary():
    summary = get_calories_summary()
    return jsonify({'total_calories': summary})

@app.route('/api/log-exercise', methods=['POST'])
def log_exercise():
    # Handle exercise logging logic here
    return jsonify({'success': True, 'message': 'Exercise logged successfully!'})


@app.route('/api/exercise-progress', methods=['GET'])
def exercise_progress():
    progress = get_exercise_progress()
    return jsonify(progress)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
