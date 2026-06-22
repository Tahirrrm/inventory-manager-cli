from database import Base, engine
from models import Category, Supplier, Product, StockMovement

Base.metadata.create_all(engine)
print("Таблицы созданы")
