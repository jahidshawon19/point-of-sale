document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('overviewChart').getContext('2d');

    const overviewChart = new Chart(ctx, {
        type: 'bar', // you can change to 'pie', 'doughnut', etc.
        data: {
            labels: ['Total Sales', 'Total Products', 'Total Customers'],
            datasets: [{
                label: 'POS Metrics',
                data: [
                    parseFloat(document.querySelector('.card-metric.bg-gradient-primary h3').innerText.replace('$','')),
                    parseInt(document.querySelector('.card-metric.bg-gradient-success h3').innerText),
                    parseInt(document.querySelector('.card-metric.bg-gradient-warning h3').innerText)
                ],
                backgroundColor: [
                    'rgba(0, 123, 255, 0.7)',
                    'rgba(40, 167, 69, 0.7)',
                    'rgba(255, 193, 7, 0.7)'
                ],
                borderColor: [
                    'rgba(0, 123, 255, 1)',
                    'rgba(40, 167, 69, 1)',
                    'rgba(255, 193, 7, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
});
