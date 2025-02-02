#Import modules
import math
from typing import List
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

#Initialize application
app = FastAPI()

#Used for in-memory storage
processed_receipts = {}

#Model for items in a receipt
class Item(BaseModel):
    shortDescription: str = Field(..., pattern="^[\\w\\s\\-]+$")
    price: str = Field(..., pattern="^\\d+\\.\\d{2}$")

class Receipt(BaseModel):
    retailer: str = Field(..., pattern="^[\\w\\s\\-&]+$")
    purchaseDate: str = Field(..., pattern="^\\d{4}-\\d{2}-\\d{2}$")
    purchaseTime: str = Field(..., pattern="^\\d{2}:\\d{2}$")
    total: str = Field(..., pattern="^\\d+\\.\\d{2}$")
    items: List[Item]

#Function to calculate award points of a given receipt
def award_points(receipt: Receipt) -> int:
    #Initialized points to 0
    current_points = 0

    #Rule 1
    current_points += sum(1 for char in receipt.retailer if char.isalnum())
    
    #Rule 2
    current_points += 50 if float(receipt.total).is_integer() else 0

    #Rule 3
    current_points += 25 if round(float(receipt.total) % 0.25, 10) == 0 else 0

    #Rule 4
    current_points += 5 * (len(receipt.items) // 2)

    #Rule 5
    for item in receipt.items:
        desc_length = len(item.shortDescription.strip())
        if desc_length % 3 == 0:
            current_points += math.ceil(float(item.price) * 0.2)

    #Rule 6
    day = datetime.strptime(receipt.purchaseDate, "%Y-%m-%d").day
    if day % 2 != 0:
        current_points += 6
    
    #Rule 7
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if (purchase_time.hour == 14 and purchase_time.minute > 0) or (purchase_time.hour == 15):
        current_points += 10
    
    return current_points

#Ensures FastAPI's ValidationError is returned with Status Code 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"description": "The receipt is invalid."},
    )

#Endpoint for processing receipts
@app.post("/receipts/process", summary="Submits a receipt for processing.", responses={400: {"description": "The receipt is invalid."}})
def process_receipts(receipt: Receipt):
    points = award_points(receipt)
    id = str(uuid4()) #Generates unique ID for receipt
    processed_receipts[id] = points #Stores points for the receipt using the ID
    return {"id": id}

#Endpoint for retrieving points of a given receipt ID
@app.get("/receipts/{id}/points", summary="Returns the points awarded for the receipt.", responses={404: {"description": "No receipt found for that ID."}})
def get_points(id: str):
    if id not in processed_receipts: #Checks if receipt's ID does not exist
        return JSONResponse(
            status_code=404,
            content={"description": "No receipt found for that ID."}
        )
    return {"points": int(processed_receipts[id])}

