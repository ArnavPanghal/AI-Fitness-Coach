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
    SELECT user_id, exercise_type, reps_count, timestamp
    FROM exercise_records
    WHERE timestamp >= NOW() - INTERVAL '7 days'; -- Fetch last week's data
    """
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        print("Error fetching data:", e)
        return None


# Generate summary report
def generate_summary_report(data):
    summary = data.groupby('exercise_type')['reps_count'].sum().reset_index()
    print("Summary Report (Total Reps per Exercise Type):")
    print(summary)
    return summary


# Heatmap Visualization Function
def plot_heatmap(data):
    data_pivot = data.pivot_table(index='user_id', columns='exercise_type', values='reps_count', aggfunc='sum')

    plt.figure(figsize=(10, 6))
    sns.heatmap(data_pivot, annot=True, cmap='coolwarm', fmt='d', cbar_kws={'label': 'Total Reps'})
    plt.title('Heatmap of Exercise Reps by User and Exercise Type')
    plt.xlabel('Exercise Type')
    plt.ylabel('User ID')
    plt.tight_layout()
    plt.show()


# Plotting functions
def plot_reps_trend(data):
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    daily_data = data.groupby(['exercise_type', data['timestamp'].dt.date])['reps_count'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='timestamp', y='reps_count', hue='exercise_type', data=daily_data)
    plt.title('Reps Trend Over the Last Week')
    plt.xlabel('Date')
    plt.ylabel('Reps Count')
    plt.xticks(rotation=45)
    plt.legend(title='Exercise Type')
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
            print("No data available for the last week.")
            return

        # Step 3: Generate summary report
        summary_report = generate_summary_report(exercise_data)

        # Step 4: Visualize data
        plot_reps_trend(exercise_data)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
