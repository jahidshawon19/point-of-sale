let tableBody = document.querySelector('#salesTable tbody');
const discountInput = document.getElementById('discount');
const vatInput = document.getElementById('vat');
const subtotalEl = document.getElementById('subtotal');
const discountEl = document.getElementById('discountValue');
const vatEl = document.getElementById('vatValue');
const grandTotalEl = document.getElementById('grandTotal');

// Update a row total
function updateRowTotal(row) {
    const select = row.querySelector('.product-select');
    const qty = row.querySelector('.quantity');
    const unitPriceInput = row.querySelector('.unit-price');
    const totalPriceInput = row.querySelector('.total-price');

    const price = parseFloat(select.selectedOptions[0]?.dataset.price || 0);
    const quantity = parseInt(qty.value || 1);

    // Stock validation
    if (quantity > stock) {
        alert(`⚠️ Not enough stock available! Only ${stock} left.`);
        qty.value = stock;  // reset to max allowed
    }

    unitPriceInput.value = price.toFixed(2);
    totalPriceInput.value = (price * quantity).toFixed(2);

    updateTotals();
}

// Update totals: subtotal, discount, VAT, grand total
function updateTotals() {
    let subtotal = 0;
    document.querySelectorAll('.total-price').forEach(input => {
        subtotal += parseFloat(input.value || 0);
    });

    const discountPercent = parseFloat(discountInput.value) || 0;
    const vatPercent = parseFloat(vatInput.value) || 0;

    const discountAmount = subtotal * (discountPercent / 100);
    const vatAmount = (subtotal - discountAmount) * (vatPercent / 100);
    const grandTotal = subtotal - discountAmount + vatAmount;

    // Update UI
    subtotalEl.innerText = `$${subtotal.toFixed(2)}`;
    discountEl.innerText = `$${discountAmount.toFixed(2)}`;
    vatEl.innerText = `$${vatAmount.toFixed(2)}`;
    grandTotalEl.innerText = `$${grandTotal.toFixed(2)}`;
}

// Add new row
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
    updateTotals();
});

// Event listeners for discount and VAT input changes
discountInput.addEventListener('input', updateTotals);
vatInput.addEventListener('input', updateTotals);

// Initialize first row
document.querySelectorAll('#salesTable tbody tr').forEach(row => {
    const select = row.querySelector('.product-select');
    const qty = row.querySelector('.quantity');

    select.addEventListener('change', () => updateRowTotal(row));
    qty.addEventListener('input', () => updateRowTotal(row));

    updateRowTotal(row);
});
