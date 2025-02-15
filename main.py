import math
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import uuid
from pprint import pprint

app = FastAPI()

# In-memory data storage
receipts = {}


class Item(BaseModel):
    """
    Represents an item in a receipt.
    """

    # Matches the pattern specified
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$")
    # Ensure price is a float with two decimal places
    price: str = Field(..., pattern=r"^\d+\.\d{2}$")


class Receipt(BaseModel):
    # Matches the pattern specified
    retailer: str = Field(..., pattern=r"^[\w\s\-&]+$")
    # Ensure total is a float with two decimal places
    total: str = Field(..., pattern=r"^\d+\.\d{2}$")
    items: List[Item]
    purchaseDate: str
    purchaseTime: str


@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    """
    Process the receipt and generate a unique ID.
    """
    receipt_id = str(uuid.uuid4())
    # Convert Pydantic model to dict
    points = calculate_points(receipt.model_dump())
    receipts[receipt_id] = {"receipt": receipt.model_dump(), "points": points}
    pprint(receipt.model_dump())
    return {"id": receipt_id}


@app.get("/receipts/{id}/points")
def get_points(id: str):
    """
    Retrieve the points for the given receipt ID.
    """
    if id not in receipts:
        raise HTTPException(status_code=404, detail="Receipt ID not found")
    return {"points": receipts[id]["points"]}


def calculate_points(receipt: dict) -> int:
    """
    Point calculation logic based on rules.
    """
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name.
    points += sum(c.isalnum() for c in receipt.get("retailer", ""))

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    total = float(receipt.get("total", 0))
    if total.is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt.
    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    """
    Rule 5: If the trimmed length of the item description is a multiple of 3,
    multiply the price by 0.2 and round up to the nearest integer.
    The result is the number of points earned.
    """
    for item in items:
        description = item["shortDescription"].strip()
        price = float(item["price"])
        if len(description) % 3 == 0:
            points += math.ceil(price * 0.2)

    # Rule 6: 6 points if the purchase date's day is odd
    purchase_date = datetime.strptime(receipt.get("purchaseDate"), "%Y-%m-%d")
    if purchase_date.day % 2 == 1:
        points += 6

    # Rule 7: 10 points if purchase time is between 2:00pm and 4:00pm
    purchase_time = datetime.strptime(receipt.get("purchaseTime"), "%H:%M").time()
    if (
        purchase_time >= datetime.strptime("14:00", "%H:%M").time()
        and purchase_time < datetime.strptime("16:00", "%H:%M").time()
    ):
        points += 10

    return points
