#Import modules
from uuid import uuid4
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.models import Receipt
from app.services import award_points
from app.exceptions import validation_exception_handler

#Initialize application
app = FastAPI()

#Used for in-memory storage
processed_receipts = {}

#Handles automated ValidationError of FastAPI
app.add_exception_handler(RequestValidationError, validation_exception_handler)

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

