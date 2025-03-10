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
# @app.route('/save_vehicle', methods=['POST'])
# def save_vehicle():
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
@app.route('/save_vehicle', methods=['POST'])
def save_vehicle():
    try:
        customer_id = request.form.get("CustomerID")  
        vehicle_number = request.form.get("vehicleNum")
        type_ = request.form.get("type")
        brand = request.form.get("brand")
        model = request.form.get("model")
        year = request.form.get("year")

        print(f"Received Data:")
        print(f"CustomerID: {customer_id}", flush=True)
        print(f"VehicleNum: {vehicle_number}", flush=True)
        print(f"Type: {type_}", flush=True)
        print(f"Brand: {brand}", flush=True)
        print(f"Model: {model}", flush=True)
        print(f"Year: {year}", flush=True)

        if not customer_id or not vehicle_number or not type_ or not brand or not model or not year:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Check if vehicle_number already exists in the database
        check_query = "SELECT COUNT(*) FROM Vehicles WHERE vehicle_number = ?"
        cursor.execute(check_query, (vehicle_number,))
        count = cursor.fetchone()[0]

        if count > 0:
            return jsonify({"status": "error", "message": "Vehicle number already exists. Please use a different one."}), 409  # HTTP 409 Conflict

        # ✅ Insert only if vehicle_number is unique
        query = "INSERT INTO Vehicles (vehicle_number, customer_id, type, brand, model, year) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (vehicle_number, customer_id, type_, brand, model, year))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "customerID": customer_id, "vehicle_number": vehicle_number,
                        "type": type_, "brand": brand, "model": model, "year": year})

    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
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


def get_customer_name():
    try:
        customer_id = request.args.get('CustomerID')
        
        if not customer_id:
            return jsonify({"status": "error", "message": "CustomerID is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT name FROM Customers WHERE customer_id = ?"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return jsonify({"status": "success", "name": result['name']})
        else:
            return jsonify({"status": "error", "message": "Customer not found"}), 404
            
    except Exception as e:
        print(f"❌ Error in get_customer_name: {e}", flush=True)
        return jsonify({"status": "error", "message": str(e)}), 500
    




# Add this route to handle form submission from factory page
@app.route('/submit_factory', methods=['POST'])
def submit_factory():
    try:
        # ✅ Get form data
        customer_id = request.form.get("customer_id")
        vehicle_number = request.form.get("vehicle_number")
        problem = request.form.get("problem")
        additional_details = request.form.get("additional_details")
        insurance_number = request.form.get("insurance_number")
        request_date = request.form.get("request_date")
        status = request.form.get("status")

        print(f"📥 Received Data:\nCustomer ID: {customer_id}\nVehicle Number: {vehicle_number}\nProblem: {problem}\nDetails: {additional_details}\nInsurance: {insurance_number}\nDate: {request_date}\nStatus: {status}")

        # ✅ Check for missing required fields
        if not customer_id or not vehicle_number or not problem or not insurance_number or not request_date:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Insert into Access Database
        query = """INSERT INTO Factory (customer_id, vehicle_number, problem, additional_details, insurance_number, request_date, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, (customer_id, vehicle_number, problem, additional_details, insurance_number, request_date, status))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "Data inserted successfully"})

    except Exception as e:
        print(f"❌ Error in submit_factory: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ---------------------- Serve Static Files ----------------------
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory("static", filename)  # Serve CSS, JS, images

if __name__ == "__main__":
    app.run(debug=True)
