from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import os
import tempfile

app = Flask(__name__)

# Sample in-memory data for expenses
expenses = []

@app.route('/')
def index():
    return render_template('index.html', expenses=expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    expenses.append(data)
    return jsonify({"message": "Expense added successfully!"}), 201

@app.route('/export', methods=['GET'])
def export_expenses():
    if not expenses:  # Check if there are any expenses
        return jsonify({"error": "No expenses to export."}), 400

    df = pd.DataFrame(expenses)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        excel_file_path = tmp.name
        df.to_excel(excel_file_path, index=False)

    return send_file(excel_file_path, as_attachment=True)

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
