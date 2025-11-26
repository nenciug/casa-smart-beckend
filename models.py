from sqlalchemy import Column, Integer, String, Numeric, Text
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    category = Column(String(100))
    price = Column(Numeric)
    description = Column(Text)
