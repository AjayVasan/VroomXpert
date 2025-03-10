from flask import Flask, request, jsonify, render_template, send_from_directory, session
import pyodbc
import random
import os
from datetime import datetime

app = Flask(__name__, template_folder="templates")
app.secret_key = "your_secret_key"  # Required for session storage

# Database path & connection string
DB_PATH = r"database\Database.accdb"
CONN_STR = rf"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH}"

def get_db_connection():
    """Establish connection to MS Access database."""
    return pyodbc.connect(CONN_STR)

# ---------------------- Serve HTML Pages ----------------------
@app.route('/')
def home():
    return render_template("index.html")  

@app.route('/vehicle')
def vehicle():
    return render_template("vehicle.html")  

@app.route('/payment')
def payment():
    return render_template("payment.html")  

@app.route('/factory')
def factory_page():
    return render_template("factory.html")  

@app.route('/payment_summary')
def payment_summary():
    return render_template("payment_summary.html")

@app.route('/feedback')
def feedback():
    return render_template("feedback.html")

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
    


def get_customer_name1():
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

# ---------------------- Save Vehicle ----------------------
@app.route('/save_vehicle', methods=['POST'])
def save_vehicle():
    try:
        customer_id = request.form.get("CustomerID")  
        vehicle_number = request.form.get("vehicleNum")
        type_ = request.form.get("type")
        brand = request.form.get("brand")
        model = request.form.get("model")
        year = request.form.get("year")

        if not customer_id or not vehicle_number or not type_ or not brand or not model or not year:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if vehicle_number already exists
        check_query = "SELECT COUNT(*) FROM Vehicles WHERE vehicle_number = ?"
        cursor.execute(check_query, (vehicle_number,))
        count = cursor.fetchone()[0]

        if count > 0:
            return jsonify({"status": "error", "message": "Vehicle number already exists."}), 409  

        query = "INSERT INTO Vehicles (vehicle_number, customer_id, type, brand, model, year) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (vehicle_number, customer_id, type_, brand, model, year))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "customerID": customer_id, "vehicle_number": vehicle_number,
                        "type": type_, "brand": brand, "model": model, "year": year})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------------- Get Customer Name ----------------------
@app.route('/get_customer_name')
def get_customer_name():
    try:
        customer_id = request.args.get('customer_id')

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
            return jsonify({"status": "success", "name": result[0]})
        else:
            return jsonify({"status": "error", "message": "Customer not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------------- Submit Factory ----------------------
@app.route('/submit_factory', methods=['POST'])
def submit_factory():
    try:
        customer_id = request.form.get("customerID")
        vehicle_number = request.form.get("vehicleNum")
        problem = request.form.get("repair")
        additional_details = request.form.get("additional_details", "")  # Optional field
        insurance_number = request.form.get("insuranceNum")
        request_date = datetime.now().strftime("%m/%d/%Y")
        status = request.form.get("status", "Pending")  # Default status

        if not customer_id or not vehicle_number or not problem or not insurance_number:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # First, create a unique request ID
        request_id = random.randint(10000, 99999)
        
        query = """INSERT INTO ServiceRequests (request_id, customer_id, vehicle_number, problem, additional_details, 
                   insurance_number, request_date, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, (request_id, customer_id, vehicle_number, problem, additional_details, 
                      insurance_number, request_date, status))
        conn.commit()

        cursor.close()
        conn.close()

        # Store request_id in session for payment processing
        session["request_id"] = request_id
        
        # Return necessary values for the next page
        return jsonify({
            "status": "success", 
            "message": "Service request submitted successfully",
            "request_id": request_id,
            "insuranceNum": insurance_number,
            "repair": problem
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------------- Save Payment ----------------------
# @app.route('/save_payment', methods=['POST'])
# def save_payment():
#     try:
#         customer_id = request.form.get("customerID")
#         name = request.form.get("name")
#         model = request.form.get("model")
#         vehicle_number = request.form.get("vehicleNum")
#         phone = request.form.get("phone")
#         service_charge = float(request.form.get("serviceCharge", 0))
#         auto_wash = float(request.form.get("autoWash", 0))  # Renamed to cleaning_charge
#         spare_charges = float(request.form.get("spareCharges", 0))  # Renamed to spare_parts_cost
        
#         # ✅ Calculate total amount
#         total_amount = service_charge + auto_wash + spare_charges
        
#         # ✅ Get request_id from session if available, otherwise generate one
#         request_id = session.get("request_id", random.randint(10000, 99999))
        
#         # ✅ Current transaction date
#         transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
#         conn = get_db_connection()
#         cursor = conn.cursor()
        
#         # ✅ Insert into Payments table (No `invoice_id`, use correct field names)
#         cursor.execute("""
#             INSERT INTO Payments (request_id, service_charge, spare_parts_cost, cleaning_charge, total_amount, 
#                                   payment_status, transaction_date)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (request_id, service_charge, spare_charges, auto_wash, total_amount, "Completed", transaction_date))
        
#         # ✅ Update the service request status if request_id exists
#         if request_id:
#             cursor.execute("UPDATE ServiceRequests SET status = ? WHERE request_id = ?", 
#                           ("Payment Completed", request_id))
        
#         conn.commit()
#         cursor.close()
#         conn.close()
        
#         # ✅ Store values in session for the summary page
#         session["total"] = total_amount
#         session["request_id"] = request_id
#         session["serviceCharge"] = service_charge
#         session["autoWash"] = auto_wash
#         session["spareCharges"] = spare_charges
        
#         return jsonify({
#             "status": "success",
#             "total": total_amount,
#             "requestID": request_id,
#             "serviceCharge": service_charge,
#             "autoWash": auto_wash,
#             "spareCharges": spare_charges
#         })

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/save_payment', methods=['POST'])
def save_payment():
    try:
        customer_id = request.form.get("customerID")
        name = request.form.get("name")
        model = request.form.get("model")
        vehicle_number = request.form.get("vehicleNum")
        phone = request.form.get("phone")
        service_charge = float(request.form.get("serviceCharge", 0))
        auto_wash = float(request.form.get("autoWash", 0))  # Renamed to cleaning_charge
        spare_charges = float(request.form.get("spareCharges", 0))  # Renamed to spare_parts_cost
        
        # Calculate total amount
        total_amount = service_charge + auto_wash + spare_charges
        
        # Get request_id from session if available, otherwise generate one
        request_id = session.get("request_id", random.randint(10000, 99999))
        
        # Current transaction date
        transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert into Payments table
        cursor.execute("""
            INSERT INTO Payments (request_id, service_charge, spare_parts_cost, cleaning_charge, total_amount, 
                                  payment_status, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (request_id, service_charge, spare_charges, auto_wash, total_amount, "Completed", transaction_date))
        
        # Update the service request status if request_id exists
        if request_id:
            cursor.execute("UPDATE ServiceRequests SET status = ? WHERE request_id = ?", 
                          ("Payment Completed", request_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Store values in session for the summary page
        session["total"] = total_amount
        session["request_id"] = request_id
        session["serviceCharge"] = service_charge
        session["autoWash"] = auto_wash
        session["spareCharges"] = spare_charges
        session["customerName"] = name
        session["model"] = model
        session["vehicleNum"] = vehicle_number
        session["CustomerID"] = customer_id  # Consistent case for CustomerID
        
        # Also store in sessionStorage via returned JSON for client-side use
        return jsonify({
            "status": "success",
            "total": total_amount,
            "requestID": request_id,
            "serviceCharge": service_charge,
            "autoWash": auto_wash,
            "spareCharges": spare_charges,
            "customerName": name,
            "model": model,
            "vehicleNum": vehicle_number,
            "CustomerID": customer_id
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------------- Submit Feedback ----------------------
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        customer_id = request.form.get("customer_id")
        rating = request.form.get("rating")
        comments = request.form.get("comments")

        if not customer_id or not rating or not comments:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Convert rating to integer
        rating = int(rating)
        feedback_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Feedback (customer_id, rating, comments, feedback_date)
            VALUES (?, ?, ?, ?)
        """, (customer_id, rating, comments, feedback_date))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "Feedback submitted successfully"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------------- Serve Static Files ----------------------
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory("static", filename)  

if __name__ == "__main__":
    app.run(debug=True) 