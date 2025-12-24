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
origins = [
    "http://localhost:3000",
    # Add another frontend origins as needed (e.g., production domain)
]

app.add_middleware(
    CORSMiddleware,         # React se API calls allow krta hai 
    allow_origins=origins,
    allow_credentials=True, #Allow cookies and authorization headers
    allow_methods=["*"],    #Allow all standard HTTP methods (GET, PUT, POST, DELETE etc)
    allow_headers=["*"],    #Allow all headers
)

# Define the startup event function using the decorator
@app.on_event("startup")
def startup_event():
    print("👉 startup_event CALLED")

    # Initialize the database connection (if necessary, though 'engine' might handle this)
    init_db()

    # Create all defined tables of (SQLAlchemy models) in the database
    database_models.Base.metadata.create_all(bind=engine)


# Route Endpoint (Test route)
@app.get("/")
def greet():
    return "Welcome to Telusko Trac"


# Default Products
products = [
    Product(id=1, name="phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=5, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=6, name="Table", description="A wooden table", price=199.99, quantity=50),
    
]

# Database Session Dependency
def get_db():
    db = SessionLocal()    # Har API request ke liye DB session deta hai
    try:
        yield db
    finally:
        db.close()
    


# Database Initialization Function
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


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    
    db_products = db.query(database_models.Product).all()
    return db_products
    # db = SessionLocal()
    # db.query()
    # return products 


@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:  
        return db_product  
    #return "product not found"


@app.post("/products", response_model=ProductResponse)
def add_product(product: Product, db: Session = Depends(get_db)):
    new_product = database_models.Product(**product.model_dump())
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)   # 👈 gets generated ID

    return new_product



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