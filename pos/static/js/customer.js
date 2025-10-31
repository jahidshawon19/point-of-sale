document.getElementById('customerSearch').addEventListener('keyup', function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#customerTable tbody tr');

    rows.forEach(row => {
        const phone = row.cells[3].textContent.toLowerCase();
        const email = row.cells[2].textContent.toLowerCase();
        if (phone.includes(filter) || email.includes(filter)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});


// pagination


function setupPagination(tableId, paginationId, rowsPerPage = 5) {
    const table = document.getElementById(tableId);
    const tbody = table.querySelector('tbody');
    const pagination = document.getElementById(paginationId);
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const totalPages = Math.ceil(rows.length / rowsPerPage);

    let currentPage = 1;

    function displayPage(page) {
        tbody.innerHTML = '';
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        rows.slice(start, end).forEach(row => tbody.appendChild(row));

        updatePagination();
    }

    function updatePagination() {
        pagination.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.innerText = i;
            btn.classList.toggle('active', i === currentPage);
            btn.addEventListener('click', () => {
                currentPage = i;
                displayPage(currentPage);
            });
            pagination.appendChild(btn);
        }
    }

    displayPage(currentPage);
}

// Initialize pagination for all tables
document.addEventListener('DOMContentLoaded', function() {
    setupPagination('categoryTable', 'categoryPagination', 5);
    setupPagination('productTable', 'productPagination', 5);
    setupPagination('customerTable', 'customerPagination', 5);
});
