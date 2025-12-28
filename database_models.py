# from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Product(Base):
    
#     __tablename__ = "product"
    
#     id: Column(Integer, primary_key=True, index=True)
#     name: Column(String)
#     description: Column(String)
#     price: Column(Float)
#     quantity: Column(Integer)


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
    pass

# Define your data models here
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(255))