// Toggle sidebar
document.getElementById("menu-toggle").addEventListener("click", function() {
    document.getElementById("sidebar-wrapper").classList.toggle("d-none");
});

// Chart.js example data
const salesCtx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(salesCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Sales ($)',
            data: [1200, 1900, 3000, 5000, 2300, 3400],
            backgroundColor: 'rgba(102,126,234,0.2)',
            borderColor: 'rgba(102,126,234,1)',
            borderWidth: 3,
            tension: 0.4,
            fill: true
        }]
    },
    options: { responsive: true }
});

const inventoryCtx = document.getElementById('inventoryChart').getContext('2d');
const inventoryChart = new Chart(inventoryCtx, {
    type: 'bar',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Inventory Count',
            data: [200, 180, 170, 150, 140, 130],
            backgroundColor: 'rgba(67,233,123,0.7)',
            borderRadius: 5
        }]
    },
    options: { responsive: true }
});



