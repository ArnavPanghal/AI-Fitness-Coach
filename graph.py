from flask import jsonify
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_workout_data():
    """Generate sample workout data for demonstration"""
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]
    exercises = [
        'pushups', 'planks', 'lateral_raises', 'squats', 'lunges', 'crunches',
        'burpees', 'mountain_climbers', 'jumping_jacks', 'dips'
    ]
    data = {'dates': dates}
    for exercise in exercises:
        data[exercise] = [random.randint(10, 50) for _ in range(30)]
    return data

def get_exercise_progress():
    """Get exercise progress data for charts"""
    data = generate_workout_data()  # Replace with database query in production
    colors = [
        'rgb(75, 192, 192)', 'rgb(255, 99, 132)', 'rgb(153, 102, 255)',
        'rgb(255, 159, 64)', 'rgb(54, 162, 235)', 'rgb(255, 206, 86)',
        'rgb(231, 233, 237)', 'rgb(46, 204, 113)', 'rgb(241, 196, 15)', 'rgb(52, 152, 219)'
    ]
    return {
        'labels': data['dates'],
        'datasets': [
            {
                'label': f"{exercise.replace('_', ' ').title()} (reps)",
                'data': data[exercise],
                'borderColor': colors[i],
                'tension': 0.1
            } for i, exercise in enumerate(data.keys()) if exercise != 'dates'
        ]
    }

def get_weekly_summary():
    """Get weekly summary data for the dashboard"""
    data = generate_workout_data()
    recent_data = {exercise: sum(data[exercise][-7:]) for exercise in data.keys() if exercise != 'dates'}
    return recent_data

def calculate_calories_burned(exercise_type, duration, intensity='medium'):
    """Calculate estimated calories burned for an exercise"""
    # These are rough estimates and should be refined with more accurate data
    calories_per_minute = {
        'pushups': {'low': 7, 'medium': 9, 'high': 11},
        'planks': {'low': 3, 'medium': 4, 'high': 5},
        'lateral_raises': {'low': 4, 'medium': 5, 'high': 6},
        'squats': {'low': 6, 'medium': 8, 'high': 10},
        'lunges': {'low': 5, 'medium': 7, 'high': 9},
        'crunches': {'low': 4, 'medium': 5, 'high': 6},
        'burpees': {'low': 8, 'medium': 10, 'high': 12},
        'mountain_climbers': {'low': 6, 'medium': 8, 'high': 10},
        'jumping_jacks': {'low': 5, 'medium': 7, 'high': 9},
        'dips': {'low': 4, 'medium': 6, 'high': 8}
    }

    if exercise_type not in calories_per_minute or intensity not in calories_per_minute[exercise_type]:
        raise ValueError("Invalid exercise type or intensity level")

    calories = calories_per_minute[exercise_type][intensity] * duration
    return calories

def get_calories_summary():
    """Generate a weekly calorie summary for all exercises"""
    data = generate_workout_data()
    calories_summary = {}
    for exercise, reps in data.items():
        if exercise != 'dates':
            calories_summary[exercise] = sum([
                calculate_calories_burned(exercise, duration=rep//10, intensity='medium')
                for rep in reps[-7:]
            ])
    return calories_summary
