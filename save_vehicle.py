from flask import Flask, render_template, request, jsonify
import pyodbc
import random

app = Flask(__name__, template_folder="templates")

# Ensure your homepage route is correctly defined
@app.route("/")
def home():
    return render_template("index.html")  # Serves the customer form

@app.route("/vehicle")
def vehicle_page():
    return render_template("vehicle.html")  # Serves the vehicle form

@app.route("/factory")
def factory_page():
    return render_template("factory.html")  # Serves the factory page

# Database connection
DB_PATH = r"C:\xampp1\htdocs\VroomXpert\database\Database.accdb"
CONN_STR = rf"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH}"

def get_db_connection():
    return pyodbc.connect(CONN_STR)

# Endpoint for saving customer details
@app.route("/save_customer", methods=["POST"])
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

@app.route("/save_vehicle", methods=["POST"])
def save_vehicle():
    try:
        customer_id = request.form.get("CustomerID")
        model = request.form.get("model")
        series = request.form.get("series")
        type_ = request.form.get("type")

        if not customer_id or not model or not series or not type_:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Vehicles (customer_id, model, series, type) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (customer_id, model, series, type_))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "customerID": customer_id, "model": model, "series": series, "type": type_})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
