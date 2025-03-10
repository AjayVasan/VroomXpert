from flask import Flask, request, jsonify, render_template, send_from_directory
import pyodbc
import random
import os

app = Flask(__name__, template_folder="templates")

# Database path & connection string
DB_PATH = r"C:\xampp1\htdocs\VroomXpert\database\Database.accdb"
CONN_STR = rf"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH}"

def get_db_connection():
    """Establish connection to MS Access database."""
    return pyodbc.connect(CONN_STR)

# ---------------------- Serve HTML Pages ----------------------
@app.route('/')
def home():
    return render_template("index.html")  # Serve customer form

@app.route('/vehicle')
def vehicle():
    return render_template("vehicle.html")  # Serve vehicle form

@app.route('/factory')
def factory_page():
    return render_template("factory.html")  # Final confirmation page

# ---------------------- Save Customer ----------------------
@app.route('/save_customer', methods=['POST'])
def save_customer():
    try:
        name = request.form.get("name")
        vehicle_number = request.form.get("vehicleNum")
        phone = request.form.get("phone")

        if not name or not vehicle_number or not phone:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        customer_id = random.randint(1000, 9999)

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO Customers (customer_id, name, phone_number, vehicle_number) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (customer_id, name, phone, vehicle_number))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"status": "success", "customerID": customer_id, "name": name, "vehicleNum": vehicle_number, "phone": phone})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------------- Save Vehicle ----------------------
@app.route('/save_vehicle', methods=['POST'])
def save_vehicle():
    try:
        customer_id = request.form.get("CustomerID")  # ✅ Auto-filled from sessionStorage
        vehicle_number = request.form.get("vehicleNum")  # ✅ Auto-filled from sessionStorage
        type_ = request.form.get("type")
        brand = request.form.get("brand")
        model = request.form.get("model")
        year = request.form.get("year")

        if not customer_id or not vehicle_number or not type_ or not brand or not model or not year:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Vehicles (customer_id, vehicle_number, type, brand, model, year) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (customer_id, vehicle_number, type_, brand, model, year))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "customerID": customer_id, "vehicle_number": vehicle_number,
                        "type": type_, "brand": brand, "model": model, "year": year})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/get_customer_name')
def get_customer_name():
    try:
        customer_id = request.args.get("CustomerID")
        print(f"🔍 Received CustomerID: {customer_id}")  # Debugging

        if not customer_id:
            return jsonify({"status": "error", "message": "Customer ID missing"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Make sure the table name is "Customers"
        query = "SELECT name FROM Customers WHERE customer_id = ?"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        
        print(f"🔍 Query Result: {result}")  # Debugging

        cursor.close()
        conn.close()

        if result:
            return jsonify({"status": "success", "name": result[0]})
        else:
            return jsonify({"status": "error", "message": f'Customer ID {customer_id} not found'}), 404

    except Exception as e:
        print(f"❌ Error: {e}")  # Debugging
        return jsonify({"status": "error", "message": str(e)}), 500


# ---------------------- Serve Static Files ----------------------
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory("static", filename)  # Serve CSS, JS, images

if __name__ == "__main__":
    app.run(debug=True)
