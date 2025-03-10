# VroomXpert

## Description

VroomXpert is a web-based vehicle management system built using Flask. It allows users to store, retrieve, and manage vehicle-related data efficiently. The application utilizes a Microsoft Access database (`Database.accdb`) via `pyodbc` for data handling and supports session-based user interactions. The platform features customer registration, vehicle data entry, repair tracking, payments, and feedback submission.

## Features

- **Customer Entry:** Users can register by providing their name, vehicle number, and phone number.
- **Vehicle Details:** Customers can enter vehicle-related information such as brand, model, type, and year.
- **Repair Management:** Users can request repairs and specify insurance details.
- **Payment Processing:** Service charges, auto wash fees, and spare parts charges are recorded.
- **Payment Summary:** Customers receive a detailed receipt for their payments.
- **Feedback Collection:** Users can rate their experience and submit feedback.

## Requirements

- Python 3.x
- Flask (for web framework)
- pyodbc (for database connectivity)
- Microsoft Access Driver (for database support)
- Web browser (for accessing the interface)

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install required dependencies using:
   ```sh
   pip install -r requirements.txt
   ```
3. Make sure the Microsoft Access Driver is installed (if not, download and install it from Microsoft’s official site).
4. Run the application using:
   ```sh
   python app.py
   ```
5. Open a web browser and go to `http://127.0.0.1:5000/` to access the application.

## Usage

### 1. Customer Entry

- Users enter their name, vehicle number, and phone number.
- Data is stored in sessionStorage for seamless navigation.

### 2. Vehicle Details

- Users provide additional details about their vehicle, including brand, model, type, and year.
- Upon submission, the system validates and stores the information.

### 3. Repair Management

- Customers enter their insurance number and specify required repairs.
- The system fetches customer details automatically for better user experience.

### 4. Payment Processing

- Users enter service charges, auto wash fees, and spare parts costs.
- Data is processed and stored, with a summary generated.

### 5. Payment Summary

- A receipt with transaction details, including customer name, vehicle, date, and total charges, is displayed.
- Users can review their payments before proceeding.

### 6. Feedback Submission

- Customers provide feedback on their experience and rate the service from 1 to 5.
- Submitted feedback is stored for future improvements.

## Future Enhancements

- **User Authentication:** Secure login system for better user management.
- **Enhanced Database:** Transition to a more scalable database like PostgreSQL or MySQL.
- **UI Improvements:** A responsive and visually appealing frontend.
- **Automated Service Suggestions:** AI-driven recommendations for maintenance and repairs.
- **Mobile App Integration:** Expanding functionality to mobile platforms.

