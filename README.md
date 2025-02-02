# Receipt Processor Web Service
This is a Python-based FastAPI web service that processes receipts and awards points.

## Setup Instructions

### Clone the repository
```
git clone https://github.com/caelaintrtas/receipt-processor.git
cd receipt-processor
```

### Run with Docker
```
docker build -t receipt-processor .
docker run -p 8000:8000 receipt-processor
```
The API will be accessible at http://127.0.0.1:8000 for making requests.

## API Endpoints
### 1. Process Receipts
Endpoint: POST /receipts/process

Description: Submits a receipt for processing and returns a unique receipt ID.

Request Body Example:
```
{
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
}
```
Response Example:
```
{ "id": "7fb1377b-b223-49d9-a31a-5a02701dd310" }
```

### 2. Get Points
Endpoint: GET /receipts/{id}/points

Description: Retrieves the number of points awarded for the receipt.

Response Example:
```
{ "points": 28 }
```

## Running Tests
To run tests inside the Docker container:
```
docker exec -it <container_id> pytest
```
