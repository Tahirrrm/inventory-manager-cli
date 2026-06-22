from database import Base, engine
from models import Category, Supplier, Product, StockMovement

Base.metadata.drop_all(engine)
print("Таблицы удалены")
