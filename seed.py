from database import SessionLocal, engine
from models import Base, Product

Base.metadata.create_all(bind=engine)

db = SessionLocal()

products = [
    Product(name="Lampa Smart A", category="Iluminat"),
    Product(name="Lampa Smart B", category="Iluminat"),
    Product(name="Termostat C", category="Climatizare"),
    Product(name="Priza Inteligentă D", category="Electrocasnice"),
]

for p in products:
    db.add(p)
db.commit()
db.close()
