import math
from datetime import datetime
from app.models import Receipt

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