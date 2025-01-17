import psycopg2
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Database connection setup
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="arnav",
            password="Arnav@1234",
            host="localhost",
            port= 5432
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None


# Fetch exercise data
def fetch_exercise_data(conn):
    query = """
    SELECT u.id AS user_id, u.name AS user_name, u.email AS user_email, u.age, u.weight,
           w.date AS workout_date, w.total_calories,
           e.exercise_name, e.sets, e.reps, e.weight AS lifted_weight,
           m.muscle_name, m.intensity
    FROM public.users u
    JOIN public.workouts w ON u.id = w.user_id
    JOIN public.exercises e ON w.id = e.workout_id
    JOIN public.muscle_map m ON w.id = m.workout_id
    """
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        print("Error fetching data:", e)
        return None

# Generate summary report
def generate_summary_report(data):
    summary = data.groupby('exercise_name')['reps'].sum().reset_index()
    print("Summary Report (Total Reps per Exercise):")
    print(summary)
    return summary


# Heatmap Visualization Function
def plot_heatmap(data):
    data_pivot = data.pivot_table(index='user_id', columns='exercise_name', values='reps', aggfunc='sum')

    plt.figure(figsize=(10, 6))
    sns.heatmap(data_pivot, annot=True, cmap='coolwarm', fmt='d', cbar_kws={'label': 'Total Reps'})
    plt.title('Heatmap of Exercise Reps by User and Exercise Type')
    plt.xlabel('Exercise Type')
    plt.ylabel('User ID')
    plt.tight_layout()
    plt.show()


# Plotting functions for Reps Trend
def plot_reps_trend(data):
    data['workout_date'] = pd.to_datetime(data['workout_date'])
    daily_data = data.groupby(['exercise_name', data['workout_date'].dt.date])['reps'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='workout_date', y='reps', hue='exercise_name', data=daily_data)
    plt.title('Reps Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Reps')
    plt.xticks(rotation=45)
    plt.legend(title='Exercise Name')
    plt.tight_layout()
    plt.show()


def main():
    # Step 1: Connect to the database
    conn = connect_to_db()
    if not conn:
        return

    try:
        # Step 2: Fetch data
        exercise_data = fetch_exercise_data(conn)
        if exercise_data is None or exercise_data.empty:
            print("No data available.")
            return

        # Step 3: Generate summary report
        summary_report = generate_summary_report(exercise_data)

        # Step 4: Visualize data
        plot_heatmap(exercise_data)
        plot_reps_trend(exercise_data)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
