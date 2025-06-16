from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load existing customers from file if it exists
customers_file = 'customers.json'
if os.path.exists(customers_file):
    with open(customers_file, 'r') as f:
        customers = json.load(f)
else:
    customers = []

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    customer = {'name': name, 'email': email}
    customers.append(customer)

    # Save to file
    with open(customers_file, 'w') as f:
        json.dump(customers, f, indent=2)

    return jsonify({'message': 'Customer added', 'customer': customer}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    name_filter = request.args.get('name')

    if name_filter:
        filtered = [c for c in customers if name_filter.lower() in c['name'].lower()]
        return jsonify(filtered)

    return jsonify(customers)


if __name__ == '__main__':
    print("✅ app.py is running")
    app.run(debug=True)
