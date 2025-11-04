let tableBody = document.querySelector('#salesTable tbody');

function updateRowTotal(row) {
    const select = row.querySelector('.product-select');
    const qty = row.querySelector('.quantity');
    const unitPriceInput = row.querySelector('.unit-price');
    const totalPriceInput = row.querySelector('.total-price');

    const price = parseFloat(select.selectedOptions[0]?.dataset.price || 0);
    const quantity = parseInt(qty.value || 1);

    unitPriceInput.value = price.toFixed(2);
    totalPriceInput.value = (price * quantity).toFixed(2);

    updateGrandTotal();
}

function updateGrandTotal() {
    let total = 0;
    document.querySelectorAll('.total-price').forEach(input => {
        total += parseFloat(input.value || 0);
    });
    document.getElementById('grandTotal').innerText = `$${total.toFixed(2)}`;
}

document.getElementById('addRow').addEventListener('click', function() {
    const newRow = tableBody.insertRow();

    const productOptions = Array.from(document.querySelector('.product-select').options)
        .map(opt => `<option value="${opt.value}" data-price="${opt.dataset.price}">${opt.text}</option>`).join('');

    newRow.innerHTML = `
        <td>
            <select class="form-select product-select" name="product[]" required>
                ${productOptions}
            </select>
        </td>
        <td><input type="number" name="quantity[]" min="1" value="1" class="form-control quantity" required></td>
        <td><input type="text" class="form-control unit-price" readonly></td>
        <td><input type="text" class="form-control total-price" readonly></td>
    `;

    const select = newRow.querySelector('.product-select');
    const qty = newRow.querySelector('.quantity');

    select.addEventListener('change', () => updateRowTotal(newRow));
    qty.addEventListener('input', () => updateRowTotal(newRow));
});

// Initialize first row
document.querySelectorAll('#salesTable tbody tr').forEach(row => {
    const select = row.querySelector('.product-select');
    const qty = row.querySelector('.quantity');

    select.addEventListener('change', () => updateRowTotal(row));
    qty.addEventListener('input', () => updateRowTotal(row));

    updateRowTotal(row);
});
