document.addEventListener('DOMContentLoaded', function () {
    const exerciseForm = document.getElementById('exerciseForm');
    const messageDiv = document.getElementById('message');
    const caloriesSummary = document.getElementById('caloriesSummary');
    let exerciseChart;

    function showMessage(message, isError = false) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${isError ? 'error' : 'success'}`;
        setTimeout(() => {
            messageDiv.textContent = '';
            messageDiv.className = 'message';
        }, 3000);
    }

    function fetchCaloriesSummary() {
        fetch('/api/calories-summary')
            .then(response => response.json())
            .then(data => {
                caloriesSummary.textContent = `${data.total_calories} kcal burned this week`;
            })
            .catch(error => {
                console.error('Error fetching calorie summary:', error);
                caloriesSummary.textContent = 'Error loading data';
            });
    }

    function updateChart() {
        fetch('/api/exercise-progress')
            .then(response => response.json())
            .then(data => {
                if (exerciseChart) {
                    exerciseChart.destroy();
                }

                const ctx = document.getElementById('exerciseChart').getContext('2d');
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
            .catch(error => console.error('Error updating chart:', error));
    }

    exerciseForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(exerciseForm);

        fetch('/api/log-exercise', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('Exercise logged successfully!');
                    exerciseForm.reset();
                    updateChart();
                    fetchCaloriesSummary();
                } else {
                    showMessage(data.message || 'Error logging exercise', true);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error logging exercise', true);
            });
    });

    // Initial loads
    updateChart();
    fetchCaloriesSummary();
});
