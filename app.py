from flask import Flask, render_template_string, request, jsonify, session
from datetime import datetime
import secrets
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Menu items (15 items)
MENU = {
    1: {"name": "Espresso", "price": 80, "category": "Coffee"},
    2: {"name": "Cappuccino", "price": 120, "category": "Coffee"},
    3: {"name": "Latte", "price": 130, "category": "Coffee"},
    4: {"name": "Americano", "price": 100, "category": "Coffee"},
    5: {"name": "Mocha", "price": 150, "category": "Coffee"},
    6: {"name": "Cold Coffee", "price": 140, "category": "Cold Drinks"},
    7: {"name": "Iced Tea", "price": 90, "category": "Cold Drinks"},
    8: {"name": "Fresh Juice", "price": 110, "category": "Cold Drinks"},
    9: {"name": "Sandwich", "price": 120, "category": "Food"},
    10: {"name": "Burger", "price": 180, "category": "Food"},
    11: {"name": "Pizza", "price": 220, "category": "Food"},
    12: {"name": "Pasta", "price": 200, "category": "Food"},
    13: {"name": "Cake Slice", "price": 100, "category": "Dessert"},
    14: {"name": "Brownie", "price": 90, "category": "Dessert"},
    15: {"name": "Cookie", "price": 50, "category": "Dessert"}
}

# In-memory storage (replace with database in production)
orders = {}
order_counter = 1

# HTML Templates
CUSTOMER_ORDER_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Place Your Order</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .category {
            padding: 20px;
            border-bottom: 1px solid #eee;
        }
        .category h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 18px;
        }
        .menu-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 10px;
            transition: all 0.3s;
        }
        .menu-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        .item-info { flex: 1; }
        .item-name {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        .item-price {
            color: #667eea;
            font-weight: bold;
        }
        .quantity-control {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .qty-btn {
            width: 35px;
            height: 35px;
            border: none;
            background: #667eea;
            color: white;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.3s;
        }
        .qty-btn:hover {
            background: #5568d3;
            transform: scale(1.1);
        }
        .qty-display {
            min-width: 30px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
        }
        .cart-summary {
            position: sticky;
            bottom: 0;
            background: white;
            padding: 20px;
            border-top: 2px solid #667eea;
            box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
        }
        .total {
            display: flex;
            justify-content: space-between;
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        .customer-info {
            margin-bottom: 15px;
        }
        .customer-info input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .customer-info input:focus {
            outline: none;
            border-color: #667eea;
        }
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        .submit-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>☕ Cafe Menu</h1>
            <p>Select your items and place order</p>
        </div>
        
        <div id="menu"></div>
        
        <div class="cart-summary">
            <div class="total">
                <span>Total:</span>
                <span id="total">₹0</span>
            </div>
            <div class="customer-info">
                <input type="text" id="customerName" placeholder="Your Name" required>
                <input type="tel" id="customerPhone" placeholder="Phone Number" required>
                <input type="text" id="tableNumber" placeholder="Table Number (optional)">
            </div>
            <button class="submit-btn" onclick="submitOrder()">Place Order</button>
            <div class="success-message" id="successMsg"></div>
        </div>
    </div>

    <script>
        const menu = {{ menu | tojson }};
        const cart = {};

        function renderMenu() {
            const categories = {};
            Object.entries(menu).forEach(([id, item]) => {
                if (!categories[item.category]) {
                    categories[item.category] = [];
                }
                categories[item.category].push({id, ...item});
            });

            const menuDiv = document.getElementById('menu');
            menuDiv.innerHTML = '';

            Object.entries(categories).forEach(([category, items]) => {
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'category';
                categoryDiv.innerHTML = `<h3>${category}</h3>`;

                items.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'menu-item';
                    itemDiv.innerHTML = `
                        <div class="item-info">
                            <div class="item-name">${item.name}</div>
                            <div class="item-price">₹${item.price}</div>
                        </div>
                        <div class="quantity-control">
                            <button class="qty-btn" onclick="updateQuantity('${item.id}', -1)">−</button>
                            <div class="qty-display" id="qty-${item.id}">0</div>
                            <button class="qty-btn" onclick="updateQuantity('${item.id}', 1)">+</button>
                        </div>
                    `;
                    categoryDiv.appendChild(itemDiv);
                });

                menuDiv.appendChild(categoryDiv);
            });
        }

        function updateQuantity(itemId, change) {
            if (!cart[itemId]) cart[itemId] = 0;
            cart[itemId] = Math.max(0, cart[itemId] + change);
            
            document.getElementById(`qty-${itemId}`).textContent = cart[itemId];
            updateTotal();
        }

        function updateTotal() {
            let total = 0;
            Object.entries(cart).forEach(([id, qty]) => {
                if (qty > 0) {
                    total += menu[id].price * qty;
                }
            });
            document.getElementById('total').textContent = `₹${total}`;
        }

        async function submitOrder() {
            const name = document.getElementById('customerName').value;
            const phone = document.getElementById('customerPhone').value;
            const table = document.getElementById('tableNumber').value;

            if (!name || !phone) {
                alert('Please enter your name and phone number');
                return;
            }

            const items = Object.entries(cart)
                .filter(([id, qty]) => qty > 0)
                .map(([id, qty]) => ({
                    id: parseInt(id),
                    name: menu[id].name,
                    price: menu[id].price,
                    quantity: qty
                }));

            if (items.length === 0) {
                alert('Please select at least one item');
                return;
            }

            const orderData = {
                customer_name: name,
                customer_phone: phone,
                table_number: table || 'N/A',
                items: items
            };

            try {
                const response = await fetch('/api/order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(orderData)
                });

                const result = await response.json();
                
                if (result.success) {
                    const msg = document.getElementById('successMsg');
                    msg.textContent = `Order #${result.order_id} placed successfully! Total: ₹${result.total}`;
                    msg.style.display = 'block';
                    
                    // Reset form
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                }
            } catch (error) {
                alert('Error placing order. Please try again.');
            }
        }

        renderMenu();
    </script>
</body>
</html>
"""

KITCHEN_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>Kitchen Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { font-size: 28px; }
        .refresh-btn {
            background: white;
            color: #667eea;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .orders-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        .order-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .order-header {
            padding: 15px;
            background: #667eea;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .order-id {
            font-size: 20px;
            font-weight: bold;
        }
        .order-status {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .status-pending { background: #ffc107; color: #000; }
        .status-preparing { background: #17a2b8; color: white; }
        .status-completed { background: #28a745; color: white; }
        .order-body {
            padding: 15px;
        }
        .customer-info {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }
        .items-list {
            margin-bottom: 15px;
        }
        .item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .order-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 15px;
            border-top: 2px solid #667eea;
        }
        .total {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        .action-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        .prepare-btn {
            background: #17a2b8;
            color: white;
        }
        .complete-btn {
            background: #28a745;
            color: white;
        }
        .payment-section {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }
        .payment-btn {
            width: 100%;
            margin-top: 5px;
        }
        .paid { background: #28a745; color: white; }
        .unpaid { background: #dc3545; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🍳 Kitchen Dashboard</h1>
        <button class="refresh-btn" onclick="loadOrders()">↻ Refresh</button>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-value" id="totalOrders">0</div>
            <div class="stat-label">Total Orders</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="pendingOrders">0</div>
            <div class="stat-label">Pending</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="totalRevenue">₹0</div>
            <div class="stat-label">Total Revenue</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="unpaidAmount">₹0</div>
            <div class="stat-label">Unpaid</div>
        </div>
    </div>

    <div class="orders-grid" id="ordersGrid"></div>

    <script>
        async function loadOrders() {
            try {
                const response = await fetch('/api/orders');
                const data = await response.json();
                
                updateStats(data.orders);
                renderOrders(data.orders);
            } catch (error) {
                console.error('Error loading orders:', error);
            }
        }

        function updateStats(orders) {
            let total = 0, pending = 0, revenue = 0, unpaid = 0;
            
            orders.forEach(order => {
                total++;
                if (order.status === 'pending') pending++;
                revenue += order.total;
                if (!order.paid) unpaid += order.total;
            });

            document.getElementById('totalOrders').textContent = total;
            document.getElementById('pendingOrders').textContent = pending;
            document.getElementById('totalRevenue').textContent = `₹${revenue}`;
            document.getElementById('unpaidAmount').textContent = `₹${unpaid}`;
        }

        function renderOrders(orders) {
            const grid = document.getElementById('ordersGrid');
            grid.innerHTML = '';

            orders.sort((a, b) => b.order_id - a.order_id).forEach(order => {
                const card = document.createElement('div');
                card.className = 'order-card';
                
                const itemsHtml = order.items.map(item => `
                    <div class="item">
                        <span>${item.quantity}x ${item.name}</span>
                        <span>₹${item.price * item.quantity}</span>
                    </div>
                `).join('');

                const statusClass = `status-${order.status}`;
                const actionBtn = order.status === 'pending' ? 
                    `<button class="action-btn prepare-btn" onclick="updateStatus(${order.order_id}, 'preparing')">Start Preparing</button>` :
                    order.status === 'preparing' ?
                    `<button class="action-btn complete-btn" onclick="updateStatus(${order.order_id}, 'completed')">Mark Complete</button>` :
                    '<span style="color: #28a745; font-weight: bold;">✓ Completed</span>';

                const paymentBtn = order.paid ?
                    `<button class="action-btn payment-btn paid" disabled>✓ Paid</button>` :
                    `<button class="action-btn payment-btn unpaid" onclick="markPaid(${order.order_id})">Mark as Paid</button>`;

                card.innerHTML = `
                    <div class="order-header">
                        <div class="order-id">Order #${order.order_id}</div>
                        <div class="order-status ${statusClass}">${order.status.toUpperCase()}</div>
                    </div>
                    <div class="order-body">
                        <div class="customer-info">
                            <div class="info-row">
                                <strong>Customer:</strong>
                                <span>${order.customer_name}</span>
                            </div>
                            <div class="info-row">
                                <strong>Phone:</strong>
                                <span>${order.customer_phone}</span>
                            </div>
                            <div class="info-row">
                                <strong>Table:</strong>
                                <span>${order.table_number}</span>
                            </div>
                            <div class="info-row">
                                <strong>Time:</strong>
                                <span>${new Date(order.timestamp).toLocaleTimeString()}</span>
                            </div>
                        </div>
                        <div class="items-list">${itemsHtml}</div>
                        <div class="order-footer">
                            <div class="total">₹${order.total}</div>
                            ${actionBtn}
                        </div>
                        <div class="payment-section">
                            ${paymentBtn}
                        </div>
                    </div>
                `;
                
                grid.appendChild(card);
            });
        }

        async function updateStatus(orderId, status) {
            try {
                const response = await fetch(`/api/order/${orderId}/status`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({status})
                });
                
                if (response.ok) {
                    loadOrders();
                }
            } catch (error) {
                console.error('Error updating status:', error);
            }
        }

        async function markPaid(orderId) {
            try {
                const response = await fetch(`/api/order/${orderId}/payment`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({paid: true})
                });
                
                if (response.ok) {
                    loadOrders();
                }
            } catch (error) {
                console.error('Error marking as paid:', error);
            }
        }

        // Auto-refresh every 10 seconds
        setInterval(loadOrders, 10000);
        loadOrders();
    </script>
</body>
</html>
"""

QR_CODE_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Code - Cafe Ordering</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 { color: #333; margin-bottom: 20px; }
        p { color: #666; margin-bottom: 30px; }
        img { 
            border: 5px solid #667eea; 
            border-radius: 10px;
            max-width: 100%;
        }
        .url {
            margin-top: 20px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 8px;
            word-break: break-all;
            color: #667eea;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>☕ Scan to Order</h1>
        <p>Customers can scan this QR code to place orders</p>
        <img src="data:image/png;base64,{{ qr_code }}" alt="QR Code">
        <div class="url">{{ order_url }}</div>
        <p style="margin-top: 20px; font-size: 14px;">Print this QR code and place it on tables</p>
    </div>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Cafe POS System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
            }
            .container {
                background: white;
                padding: 50px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 { color: #333; margin-bottom: 40px; }
            .btn {
                display: inline-block;
                padding: 15px 40px;
                margin: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                transition: transform 0.3s;
            }
            .btn:hover {
                transform: translateY(-3px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>☕ Cafe POS System</h1>
            <a href="/order" class="btn">Customer Order Page</a><br>
            <a href="/kitchen" class="btn">Kitchen Dashboard</a><br>
            <a href="/qr" class="btn">Generate QR Code</a>
        </div>
    </body>
    </html>
    """

@app.route('/order')
def order_page():
    return render_template_string(CUSTOMER_ORDER_PAGE, menu=MENU)

@app.route('/kitchen')
def kitchen_page():
    return render_template_string(KITCHEN_DASHBOARD)

@app.route('/qr')
def qr_page():
    # Generate QR code
    order_url = request.url_root + 'order'
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(order_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_code_base64 = base64.b64encode(buf.getvalue()).decode()
    
    return render_template_string(QR_CODE_PAGE, qr_code=qr_code_base64, order_url=order_url)

# API Routes
@app.route('/api/order', methods=['POST'])
def create_order():
    global order_counter
    
    data = request.json
    order_id = order_counter
    order_counter += 1
    
    total = sum(item['price'] * item['quantity'] for item in data['items'])
    
    order = {
        'order_id': order_id,
        'customer_name': data['customer_name'],
        'customer_phone': data['customer_phone'],
        'table_number': data['table_number'],
        'items': data['items'],
        'total': total,
        'status': 'pending',
        'paid': False,
        'timestamp': datetime.now().isoformat()
    }
    
    orders[order_id] = order
    
    return jsonify({
        'success': True,
        'order_id': order_id,
        'total': total
    })

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify({
        'orders': list(orders.values())
    })

@app.route('/api/order/<int:order_id>/status', methods=['POST'])
def update_order_status(order_id):
    if order_id in orders:
        data = request.json
        orders[order_id]['status'] = data['status']
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/order/<int:order_id>/payment', methods=['POST'])
def update_payment_status(order_id):
    if order_id in orders:
        data = request.json
        orders[order_id]['paid'] = data['paid']
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 CAFE POS SYSTEM STARTED")
    print("="*60)
    print("\n📱 Access URLs:")
    print("   • Home Page:     http://localhost:5000/")
    print("   • Customer Order: http://localhost:5000/order")
    print("   • Kitchen View:   http://localhost:5000/kitchen")
    print("   • QR Code:       http://localhost:5000/qr")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
