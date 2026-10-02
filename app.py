import os
from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [
    {
        "id": 1,
        "name": "Yash",
        "department": "Data Engineering",
        "role": "Data Engineer"
    },
    {
        "id": 2,
        "name": "Rahul",
        "department": "IT",
        "role": "Software Engineer"
    },
    {
        "id": 3,
        "name": "Amit",
        "department": "DevOps",
        "role": "DevOps Engineer"
    }
]


@app.route("/")
def home():
    return jsonify({
        "message": "Employee Management API v1.1",
        "version": "1.1",
        "environment": os.getenv("APP_ENV", "development"),
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees), 200


@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return jsonify(employee), 200

    return jsonify({
        "error": "Employee not found"
    }), 404


@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json()

    if not data or "name" not in data or "department" not in data or "role" not in data:
        return jsonify({
            "error": "name, department and role are required"
        }), 400

    new_employee = {
        "id": len(employees) + 1,
        "name": data["name"],
        "department": data["department"],
        "role": data["role"]
    }

    employees.append(new_employee)

    return jsonify(new_employee), 201


@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json()

    for employee in employees:
        if employee["id"] == employee_id:

            if "name" in data:
                employee["name"] = data["name"]

            if "department" in data:
                employee["department"] = data["department"]

            if "role" in data:
                employee["role"] = data["role"]

            return jsonify(employee), 200

    return jsonify({
        "error": "Employee not found"
    }), 404


@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            employees.remove(employee)

            return jsonify({
                "message": "Employee deleted successfully"
            }), 200

    return jsonify({
        "error": "Employee not found"
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
