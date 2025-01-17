from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory data (mimics your database structure)
users = [
    {"id": 1, "name": "John Doe", "email": "johndoe@example.com", "age": 28, "weight": 75},
    {"id": 2, "name": "Jane Smith", "email": "janesmith@example.com", "age": 25, "weight": 68}
]

workouts = [
    {"id": 1, "user_id": 1, "date": "2025-01-17", "total_calories": 300},
    {"id": 2, "user_id": 2, "date": "2025-01-16", "total_calories": 450}
]

exercises = [
    {"id": 1, "workout_id": 1, "exercise_name": "Push-ups", "sets": 3, "reps": 15, "weight": 0},
    {"id": 2, "workout_id": 2, "exercise_name": "Bicep Curls", "sets": 3, "reps": 12, "weight": 15}
]

muscle_map = [
    {"id": 1, "workout_id": 1, "muscle_name": "Chest", "intensity": 80},
    {"id": 2, "workout_id": 2, "muscle_name": "Biceps", "intensity": 70}
]

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    return jsonify(workouts)

@app.route('/exercises', methods=['GET'])
def get_exercises():
    return jsonify(exercises)

@app.route('/muscle_map', methods=['GET'])
def get_muscle_map():
    return jsonify(muscle_map)

@app.route('/add_user', methods=['POST'])
def add_user():
    new_user = request.json
    users.append(new_user)
    return jsonify({"message": "User added successfully!", "user": new_user})

@app.route('/add_workout', methods=['POST'])
def add_workout():
    new_workout = request.json
    workouts.append(new_workout)
    return jsonify({"message": "Workout added successfully!", "workout": new_workout})

@app.route('/add_exercise', methods=['POST'])
def add_exercise():
    new_exercise = request.json
    exercises.append(new_exercise)
    return jsonify({"message": "Exercise added successfully!", "exercise": new_exercise})

@app.route('/add_muscle_map', methods=['POST'])
def add_muscle_map():
    new_muscle = request.json
    muscle_map.append(new_muscle)
    return jsonify({"message": "Muscle map added successfully!", "muscle": new_muscle})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
