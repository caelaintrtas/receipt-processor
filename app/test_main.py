#Import modules
from fastapi.testclient import TestClient
from app.main import app

#Initialize testing client
client = TestClient(app)

#Tests successful input of process_receipts()
def test_process_receipts():
    response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },{
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
            }
        ],
        "total": "35.35"
    })
    #Validate status code
    assert response.status_code == 200

    #Validate presence of 'id' and type
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], str)

#Tests invalid input of process_receipts()
def test_process_receipts_invalid_receipt():
    #Missing field
    response = client.post("/receipts/process", json={
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },{
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
            }
        ],
        "total": "35.35"
    })

    #Validates status code
    assert response.status_code == 400

    #Validates return object
    assert response.json() == {"description": "The receipt is invalid."}

#Tests successful input of get_points()
def test_get_points():
    response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },{
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
            }
        ],
        "total": "35.35"
    })
    id = response.json()["id"]
    points_response = client.get(f"/receipts/{id}/points")

    #Validates status code
    assert points_response.status_code == 200

    #Validates presence of 'points', type, and correct value
    data = points_response.json()
    assert "points" in data
    assert isinstance(data["points"], int)
    points = 28
    assert data["points"] == points

#Tests invalid input of get_points()
def test_get_points_invalid_id():
    response = client.get("/receipts/invalid-id/points")

    #Validates status code
    assert response.status_code == 404

    #Validates return object
    assert response.json() == {"description": "No receipt found for that ID."}

