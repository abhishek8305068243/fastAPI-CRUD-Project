from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product, ProductResponse
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session



# Create the fastapi app instance
# ye backend application object hai, sare routes isi se judte hai
app = FastAPI()


# Here we add the origins separately (& also we can add more than 1 origins)
# Ye wo frontend URLs hai jinko backend allow krega
origins = [
    "http://localhost:3000",    # React Frontend
    # Add another frontend origins as needed (e.g., production domain)
]

app.add_middleware(
    CORSMiddleware,         # Frontend se API calls allow krta hai 
    allow_origins=origins,  # sirf specified origins allowed (like above)
    allow_credentials=True, #Allow cookies and authorization headers
    allow_methods=["*"],    #Allow all standard HTTP methods (GET, PUT, POST, DELETE etc)
    allow_headers=["*"],    #Allow all headers
)

# Application startup event function using the decorator

# App start hote hi ye function call hota hai
@app.on_event("startup")
def startup_event():
    print("👉 startup_event CALLED")

    # Database initialize karna
    init_db()

    # Create all defined tables of (SQLAlchemy models) in the database
    database_models.Base.metadata.create_all(bind=engine)


# Route Endpoint (Test route)
# Simple test route to check API running or not
@app.get("/")
def greet():
    return "Hey Abhishek! API is running"


# Default In-memory Products
# (sirf initial DB seeding ke liye)
products = [
    Product(id=1, name="phone", description="A smartphone", price=699.99, quantity=50, category = "Electronic device"),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30, category = "Electronic device"),
    Product(id=5, name="Pen", description="A blue ink pen", price=1.99, quantity=100, category = "Study material"),
    Product(id=6, name="Table", description="A wooden table", price=199.99, quantity=50, category = "Wooden Material"),
    
]

# Database Session Dependency

# Ye function har API request ke liye
# ek naya database session deta hai
def get_db():
    db = SessionLocal()    # Har API request ke liye DB session deta hai
    try:
        yield db           # API ko session provide karta hai
    finally:
        db.close()         # Request complete hone ke baad session close
    


# Database Initialization Logic

# App startup par DB me data hai ya nahi ye check karta hai
def init_db():
    print("init_db CALLED")
    db = SessionLocal()
    try:
        print("🔥 BEFORE COUNT")
        count = db.query(database_models.Product).count()
        print("COUNT =", count)
        if count == 0:
            for product in products:
                db.add(database_models.Product(**product.model_dump()))
            db.commit()
        
    except Exception as e:
        print(e)
    finally:
        db.close()


# ==============================
# API Endpoints
# ==============================

# 🔹 Get all products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    # Database se saare products fetch karta hai
    db_products = db.query(database_models.Product).all()
    return db_products
    # db = SessionLocal()
    # db.query()
    # return products 


# 🔹 Get product by ID
@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    # ID ke basis par single product fetch
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:  
        return db_product  
    #return "product not found"


# 🔹 Add new product
@app.post("/products", response_model=ProductResponse)
def add_product(product: Product, db: Session = Depends(get_db)):
    # Pydantic model ko SQLAlchemy model me convert kar rahe hain
    new_product = database_models.Product(**product.model_dump())
    
    db.add(new_product)
    db.commit()
    
    # Database se updated object reload karta hai (ID generate hoti hai)
    db.refresh(new_product)   # 👈 gets generated ID

    return new_product


# 🔹 Update existing product
@app.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_models.Product)
        .filter(database_models.Product.id == id)
        .first()
    )

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)   # 👈 updated data reload

    return db_product




@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product have been deleted"
    else:   
        return "Product not found"