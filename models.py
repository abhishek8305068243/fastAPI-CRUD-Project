
from pydantic import BaseModel          

# Ye base Pydantic Model hai jo Product ka structure define krta hai
# Iska use hum request body validate krne ke liye use krte hai
class Product(BaseModel):
    id: int     
    name: str
    description: str
    price: float
    quantity: int
    category: str
    
    
# Ye response model hai jo API response me data return krne ke kaam aata hai
# Ye products se inherit krta hai (sare fields aa jate hai) 
class ProductResponse(Product):
    id: int                         # id explicitly define ki (clearity ke liye)
                                    # id is the conventional pimary key name used across databases & ORMs. It keep API simple & consistent.
    class Config:
        # Ye setting FastAPI ko batati hai ki
        # SQLAlchemy ORM object ko directly Pydantic model me convert kar sakte hain
        # Matlab: database object → JSON response
        from_attributes = True   # SQLAlchemy object → JSON