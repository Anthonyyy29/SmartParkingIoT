// Configuration
const API_BASE_URL = 'http://localhost:8000'; // Change this for production
const REFRESH_INTERVAL = 5000; // 5 seconds

let autoRefreshInterval = null;
let autoRefreshEnabled = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Dashboard initialized');
    
    // Event listeners
    document.getElementById('refreshBtn').addEventListener('click', refreshData);
    document.getElementById('autoRefreshToggle').addEventListener('click', toggleAutoRefresh);
    
    // Initial data load
    refreshData();
});

// Fetch and display parking status
async function refreshData() {
    console.log('🔄 Fetching parking status...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/parking-status`);
        const data = await response.json();
        
        if (data.success) {
            displayParkingStatus(data);
            updateLastUpdateTime();
            console.log('✅ Data updated successfully');
        } else {
            showError('Failed to fetch data');
        }
    } catch (error) {
        console.error('❌ Error:', error);
        showError(`Connection error: ${error.message}`);
    }
}

// Display parking status data
function displayParkingStatus(data) {
    // Update active vehicles count
    const activeCount = data.active_vehicles;
    document.getElementById('activeVehiclesCount').textContent = activeCount;
    
    // Calculate total revenue
    let totalRevenue = 0;
    data.vehicles.forEach(vehicle => {
        totalRevenue += vehicle.fee;
    });
    document.getElementById('totalRevenueToday').textContent = 
        `Rp ${totalRevenue.toLocaleString('id-ID')}`;
    
    // Update table
    const tableBody = document.getElementById('vehiclesTableBody');
    
    if (activeCount === 0) {
        tableBody.innerHTML = '<tr><td colspan="5" class="empty-message">No vehicles currently parked</td></tr>';
    } else {
        tableBody.innerHTML = '';
        data.vehicles.forEach((vehicle, index) => {
            const row = document.createElement('tr');
            const fee = parseFloat(vehicle.fee).toLocaleString('id-ID');
            const entryTime = new Date(vehicle.entry_time).toLocaleString('id-ID');
            
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><strong>${vehicle.uid}</strong></td>
                <td>${entryTime}</td>
                <td>${vehicle.duration_minutes}</td>
                <td><strong>Rp ${fee}</strong></td>
            `;
            tableBody.appendChild(row);
        });
    }
}

// Toggle auto refresh
function toggleAutoRefresh() {
    autoRefreshEnabled = !autoRefreshEnabled;
    const button = document.getElementById('autoRefreshToggle');
    
    if (autoRefreshEnabled) {
        button.classList.add('active');
        button.textContent = 'Auto Refresh: ON';
        autoRefreshInterval = setInterval(refreshData, REFRESH_INTERVAL);
        console.log('✅ Auto refresh enabled');
    } else {
        button.classList.remove('active');
        button.textContent = 'Auto Refresh: OFF';
        clearInterval(autoRefreshInterval);
        console.log('❌ Auto refresh disabled');
    }
}

// Update last update time
function updateLastUpdateTime() {
    const now = new Date().toLocaleTimeString('id-ID');
    document.getElementById('lastUpdateTime').textContent = now;
    document.getElementById('footerTime').textContent = now;
}

// Show error message
function showError(message) {
    const tableBody = document.getElementById('vehiclesTableBody');
    tableBody.innerHTML = `
        <tr>
            <td colspan="5" class="empty-message" style="color: #d32f2f;">
                ⚠️ ${message}
            </td>
        </tr>
    `;
}

// Format currency (Indonesian Rupiah)
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(amount);
}

console.log('📊 Admin Dashboard Script Loaded');
