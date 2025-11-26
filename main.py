from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import random
from mangum import Mangum

from database import SessionLocal, engine, Base
from models import Product

# Creează tabelele dacă nu există
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Casa Ta Inteligentă API")

# CORS – permite orice origine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexiune DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Adaugă produs
@app.post("/add_product")
def add_product(product: dict, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.get("name"),
        category=product.get("category"),
        price=product.get("price"),
        description=product.get("description")
    )
    db.add(new_product)
    db.commit()
    return {"status": "added", "product": product}

# Listare produse
@app.get("/all_products")
def all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# Recomandare / căutare după text
@app.post("/recommend")
def recommend(query: dict, db: Session = Depends(get_db)):
    search_text = query.get("query", "").lower()
    products_list = db.query(Product).all()
    filtered = [
        p.name for p in products_list
        if search_text in (p.name or "").lower() or search_text in (p.description or "").lower()
    ]
    if not filtered:
        return {"recommendations": ["Niciun produs disponibil"]}
    return {"recommendations": random.sample(filtered, min(2, len(filtered)))}

# Mangum handler pentru Vercel serverless
handler = Mangum(app)
