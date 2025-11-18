# flask-cafe-ordering-system
A complete web-based Cafe POS system with QR code ordering, real-time kitchen dashboard, and payment tracking built with Flask
# ☕ Cafe POS & Ordering System

A complete, lightweight Point of Sale (POS) system for cafes and restaurants built with Flask. Customers can scan QR codes to place orders directly from their phones, while staff manage orders and payments through a real-time kitchen dashboard.

## ✨ Features

### 👥 Customer Features
- 📱 Mobile-responsive ordering interface
- 🍕 15-item menu organized by categories (Coffee, Cold Drinks, Food, Desserts)
- ➕ Easy quantity selection with intuitive controls
- 💳 Real-time order total calculation
- 📝 Customer information capture (name, phone, table number)
- ✅ Instant order confirmation

### 🍳 Kitchen/Admin Features
- 📊 Real-time dashboard with live order updates
- 📈 Statistics tracking (total orders, revenue, pending orders, unpaid amounts)
- 🔄 Order status management (Pending → Preparing → Completed)
- 💰 Payment tracking (paid/unpaid)
- 🔃 Auto-refresh every 10 seconds
- 👤 Complete customer details on each order
- 📱 Responsive design for tablets and phones

### 📲 QR Code System
- Generate printable QR codes for table ordering
- Easy scanning with any smartphone camera
- Direct link to ordering page

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cafe-pos-system.git
cd cafe-pos-system
```

2. **Install dependencies**
```bash
pip install flask qrcode[pil]
```

3. **Run the application**
```bash
python app.py
```

4. **Access the system**
- Home: `http://localhost:5000/`
- Customer Order Page: `http://localhost:5000/order`
- Kitchen Dashboard: `http://localhost:5000/kitchen`
- QR Code Generator: `http://localhost:5000/qr`

## 📱 Usage

1. **For Customers:**
   - Scan the QR code or visit the order page
   - Browse menu and select items
   - Enter name, phone, and table number
   - Place order

2. **For Kitchen Staff:**
   - Open kitchen dashboard
   - View incoming orders in real-time
   - Update order status as you prepare items
   - Mark orders as paid when payment is received

3. **Generate QR Codes:**
   - Visit `/qr` page
   - Print QR code
   - Place on tables for easy customer access

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **QR Code Generation:** python-qrcode, Pillow
- **Storage:** In-memory (can be upgraded to database)

## 📂 Project Structure
```
cafe-pos-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Customization

### Update Menu Items
Edit the `MENU` dictionary in `app.py`:
```python
MENU = {
    1: {"name": "Your Item", "price": 100, "category": "Category"},
    # Add more items...
}
```

### Change Port
Modify the last line in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change port here
```

## 🚀 Deployment

### For Production Use:
1. Replace in-memory storage with a database (SQLite/PostgreSQL/MongoDB)
2. Add authentication for kitchen dashboard
3. Enable HTTPS
4. Deploy to cloud platforms:
   - Heroku
   - PythonAnywhere
   - AWS EC2
   - DigitalOcean
   - Render

### Example: Deploy to Heroku
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
heroku create your-cafe-pos
git push heroku main
```

## 🔮 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication & authorization
- [ ] Order history & analytics
- [ ] Email/SMS notifications
- [ ] Receipt printing
- [ ] Multi-language support
- [ ] Inventory management
- [ ] Daily sales reports
- [ ] Table management system
- [ ] Tip calculation
- [ ] Discount & coupon system

## 📸 Screenshots

*(Add screenshots of your customer order page, kitchen dashboard, and QR code page here)*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Your Name - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/yourusername/cafe-pos-system](https://github.com/yourusername/cafe-pos-system)

## 🙏 Acknowledgments

- Flask documentation
- QR Code generation with python-qrcode
- Inspiration from modern restaurant ordering systems

---

⭐ If you found this project helpful, please give it a star!
```

---

## 🏷️ **GitHub Topics/Tags to Add:**
```
flask, pos-system, restaurant, cafe, qr-code, ordering-system, 
python, food-ordering, kitchen-dashboard, payment-tracking, 
web-app, food-service, restaurant-management
