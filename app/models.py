from typing import List
from pydantic import BaseModel, Field

#Model for items in a receipt
class Item(BaseModel):
    shortDescription: str = Field(..., pattern="^[\\w\\s\\-]+$")
    price: str = Field(..., pattern="^\\d+\\.\\d{2}$")

#Model for Receipts
class Receipt(BaseModel):
    retailer: str = Field(..., pattern="^[\\w\\s\\-&]+$")
    purchaseDate: str = Field(..., pattern="^\\d{4}-\\d{2}-\\d{2}$")
    purchaseTime: str = Field(..., pattern="^\\d{2}:\\d{2}$")
    total: str = Field(..., pattern="^\\d+\\.\\d{2}$")
    items: List[Item]