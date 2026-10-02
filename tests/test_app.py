import pytest
from app import app, employees


@pytest.fixture
def client():
    app.config["TESTING"] = True

    original_employees = [employee.copy() for employee in employees]

    with app.test_client() as client:
        yield client

    employees.clear()
    employees.extend(original_employees)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_get_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_employee(client):
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_employee_not_found(client):
    response = client.get("/employees/999")
    assert response.status_code == 404


def test_create_employee(client):
    response = client.post(
        "/employees",
        json={
            "name": "Neha",
            "department": "QA",
            "role": "Test Engineer"
        }
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Neha"
    assert data["department"] == "QA"
    assert data["role"] == "Test Engineer"


def test_create_employee_invalid_data(client):
    response = client.post(
        "/employees",
        json={
            "name": "Neha"
        }
    )

    assert response.status_code == 400


def test_update_employee(client):
    response = client.put(
        "/employees/1",
        json={
            "role": "Senior Data Engineer"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["role"] == "Senior Data Engineer"


def test_delete_employee(client):
    response = client.delete("/employees/3")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Employee deleted successfully"
