from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# MongoDB Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/cateringDB"
os.getenv("mongodb+srv://androjebina:x0MDWPlseFNbdxOx@cluster0.mt7kb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo = PyMongo(app)

# Item Prices & Tax Rates
ITEM_PRICES = {"idly": 10, "chapati": 15, "poori": 20}
GST_RATE = 5  # 5%
SST_RATE = 8  # 8%

@app.route('/calculate', methods=['POST'])
def calculate_bill():
    data = request.json  # Get order details

    subtotal = sum(data.get(item, 0) * ITEM_PRICES.get(item, 0) for item in ITEM_PRICES)
    gst_amount = (subtotal * GST_RATE) / 100
    sst_amount = (subtotal * SST_RATE) / 100
    grand_total = subtotal + gst_amount + sst_amount

    # Store order in MongoDB
    order = {
        "items": data,
        "subtotal": subtotal,
        "GST": gst_amount,
        "SST": sst_amount,
        "grand_total": grand_total,
        "order_time": datetime.now()
    }
    mongo.db.orders.insert_one(order)

    return jsonify({
        "message": "✅ Thank you for your order!",
        "subtotal": subtotal,
        "GST": gst_amount,
        "SST": sst_amount,
        "Grand Total": grand_total
    })

if __name__ == '__main__':
    app.run(debug=True)
