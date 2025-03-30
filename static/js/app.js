document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('calculatorForm');
    const alert = document.getElementById('alert');
    const results = document.getElementById('results');
    const sheetDetails = document.getElementById('sheetDetails');
    const costBreakdown = document.getElementById('costBreakdown');

    // Show alert message
    function showAlert(message, type = 'error') {
        alert.textContent = message;
        alert.className = `mb-6 p-4 rounded-lg ${type === 'error' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`;
        alert.classList.remove('hidden');
        setTimeout(() => {
            alert.classList.add('hidden');
        }, 5000);
    }

    // Format number as currency
    function formatCurrency(number) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(number);
    }

    // Format number with 2 decimal places
    function formatNumber(number) {
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(number);
    }

    // Create a result row
    function createResultRow(label, value, isHighlight = false) {
        const div = document.createElement('div');
        div.className = `flex justify-between items-center p-2 ${isHighlight ? 'bg-blue-50 rounded' : ''}`;
        div.innerHTML = `
            <span class="text-gray-700">${label}</span>
            <span class="${isHighlight ? 'font-semibold text-blue-700' : 'text-gray-900'}">${value}</span>
        `;
        return div;
    }

    // Display calculation results
    function displayResults(data) {
        // Clear previous results
        sheetDetails.innerHTML = '';
        costBreakdown.innerHTML = '';

        // Sheet Details
        sheetDetails.appendChild(createResultRow('Best Sheet Size', `${data.best_sheet[0]}" × ${data.best_sheet[1]}"`, true));
        sheetDetails.appendChild(createResultRow('Pieces per Sheet', data.pieces));
        sheetDetails.appendChild(createResultRow('Waste Area', `${formatNumber(data.waste)} sq. inches`));
        sheetDetails.appendChild(createResultRow('Sheets Needed', data['Sheets Needed']));
        sheetDetails.appendChild(createResultRow('Paper Weight (GSM)', formatNumber(data['Gms'])));

        // Cost Breakdown
        costBreakdown.appendChild(createResultRow('Amount per Sheet', formatCurrency(data['Amount per Sheet'])));
        costBreakdown.appendChild(createResultRow('Total Paper Cost', formatCurrency(data['Total Paper Cost'])));
        costBreakdown.appendChild(createResultRow('Pasting Cost', formatCurrency(data['Pasting Cost'])));
        costBreakdown.appendChild(createResultRow('Cost after Pasting', formatCurrency(data['Total Cost after Pasting'])));
        costBreakdown.appendChild(createResultRow('Plate Cost', formatCurrency(data['Plate Cost'])));
        costBreakdown.appendChild(createResultRow('Total Production Cost', formatCurrency(data['Total Production Cost']), true));
        costBreakdown.appendChild(createResultRow('Cost per Piece', formatCurrency(data['Cost per Piece']), true));

        // Show results section
        results.classList.remove('hidden');
        results.scrollIntoView({ behavior: 'smooth' });
    }

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Calculation failed');
            }

            showAlert('Calculation completed successfully!', 'success');
            displayResults(result);
        } catch (error) {
            showAlert(error.message);
            results.classList.add('hidden');
        }
    });
});