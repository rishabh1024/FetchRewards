from fastapi.testclient import TestClient
import sys
import os
import math


# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, calculate_points, receipts

# Import FastAPI test clientKK
client = TestClient(app)

# Helper function to create a valid receipt
def create_valid_receipt():
    return {
        "retailer": "Test Retailer",
        "total": "100.00",
        "purchaseDate": "2023-10-01",
        "purchaseTime": "15:00",
        "items": [
            {"shortDescription": "Item 1", "price": "10.00"},
            {"shortDescription": "Item 2", "price": "20.00"}
        ]
    }

# Base functionality tests
def test_process_receipt_valid():
    receipt = create_valid_receipt()
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    assert "id" in response.json()

# Rule-specific tests
def test_rule1_alphanumeric_chars():
    receipt = create_valid_receipt()
    receipt["retailer"] = "M&M Corner Market"
    points = calculate_points(receipt)
    assert points >= sum(c.isalnum() for c in receipt["retailer"])

def test_rule2_round_dollar():
    receipt = create_valid_receipt()
    receipt["total"] = "10.00"
    points = calculate_points(receipt)
    assert points >= 50  # Base points + 50 for round dollar

def test_rule3_multiple_of_quarter():
    receipt = create_valid_receipt()
    receipt["total"] = "10.25"
    points = calculate_points(receipt)
    assert points >= 25

def test_rule4_pair_items():
    receipt = create_valid_receipt()
    receipt["items"] = [{"shortDescription": "item", "price": "5.00"}]*5
    points = calculate_points(receipt)
    assert points >= (5 // 2) * 5

def test_rule5_description_multiple_of_3():
    receipt = create_valid_receipt()
    receipt["items"][0]["shortDescription"] = "abc"
    points = calculate_points(receipt)
    expected = math.ceil(10.00 * 0.2)
    assert points >= expected

def test_rule6_total_over_10():
    receipt = create_valid_receipt()
    receipt["total"] = "15.00"
    points = calculate_points(receipt)
    assert points >= 5

def test_rule7_odd_day():
    receipt = create_valid_receipt()
    receipt["purchaseDate"] = "2023-10-03"  # Odd day
    points = calculate_points(receipt)
    assert points >= 6

def test_rule8_time_window():
    receipt = create_valid_receipt()
    receipt["purchaseTime"] = "14:30"
    points = calculate_points(receipt)
    assert points >= 10

# Edge case tests
def test_invalid_retailer():
    receipt = create_valid_receipt()
    receipt["retailer"] = "Invalid@Retailer"
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 422

def test_get_points_invalid_id():
    response = client.get("/receipts/invalid-id/points")
    assert response.status_code == 404