document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('log-workout-form');
    const ctx = document.getElementById('workoutChart').getContext('2d');
    let workoutChart;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch('/log_workout', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Workout logged successfully!');
                form.reset();
                updateChart();
            }
        })
        .catch(error => console.error('Error:', error));
    });

    function updateChart() {
        fetch('/get_workout_data')
        .then(response => response.json())
        .then(data => {
            const dates = data.map(item => item.date);
            const weights = data.map(item => item.weight);
            const reps = data.map(item => item.reps);

            if (workoutChart) {
                workoutChart.destroy();
            }

            workoutChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Weight (lbs)',
                        data: weights,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }, {
                        label: 'Reps',
                        data: reps,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
    }

    updateChart();
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize exercise progress chart
    const ctx = document.getElementById('exerciseChart').getContext('2d');
    let exerciseChart;

    // Fetch and render exercise progress data
    fetch('/api/exercise-progress')
        .then(response => response.json())
        .then(data => {
            exerciseChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: data.datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: '30-Day Exercise Progress'
                        },
                        legend: {
                            position: 'bottom'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Count (reps/seconds)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading exercise progress:', error));
});