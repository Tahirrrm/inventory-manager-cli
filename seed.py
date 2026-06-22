from decimal import Decimal

from sqlalchemy import select

from database import SessionLocal
from models import Category, Product, StockMovement, Supplier


def seed():
    with SessionLocal() as session:
        existing = session.execute(select(Category).limit(1)).scalar()
        if existing:
            print("Данные уже существуют. Seed пропущен.")
            return

     
        electronics = Category(name="Electronics")
        furniture = Category(name="Furniture")
        office_supplies = Category(name="Office Supplies")
        tools = Category(name="Tools")

        session.add_all([electronics, furniture, office_supplies, tools])
        session.flush()

      
        techtrade = Supplier(
            name="TechTrade",
            phone="+7-123-456-78-90",
            email="info@techtrade.ru",
        )
        officemarket = Supplier(
            name="OfficeMarket",
            phone="+7-123-456-78-91",
            email="info@officemarket.ru",
        )
        woodfactory = Supplier(
            name="WoodFactory",
            phone="+7-123-456-78-92",
            email="info@woodfactory.ru",
        )
        globaltools = Supplier(
            name="GlobalTools",
            phone="+7-123-456-78-93",
            email="info@globaltools.ru",
        )

        session.add_all([techtrade, officemarket, woodfactory, globaltools])
        session.flush()

    
        laptop = Product(
            name="Laptop Lenovo ThinkPad",
            sku="LAP001",
            category_id=electronics.id,
            supplier_id=techtrade.id,
            purchase_price=Decimal("70000.00"),
            selling_price=Decimal("95000.00"),
            min_quantity=5,
        )
        mouse = Product(
            name="Wireless Mouse",
            sku="MOU001",
            category_id=electronics.id,
            supplier_id=techtrade.id,
            purchase_price=Decimal("500.00"),
            selling_price=Decimal("1200.00"),
            min_quantity=10,
        )
        chair = Product(
            name="Office Chair",
            sku="CHA001",
            category_id=furniture.id,
            supplier_id=woodfactory.id,
            purchase_price=Decimal("8000.00"),
            selling_price=Decimal("15000.00"),
            min_quantity=5,
        )
        paper = Product(
            name="A4 Paper Pack",
            sku="PAP001",
            category_id=office_supplies.id,
            supplier_id=officemarket.id,
            purchase_price=Decimal("200.00"),
            selling_price=Decimal("400.00"),
            min_quantity=50,
        )
        screwdriver = Product(
            name="Screwdriver Set",
            sku="SCR001",
            category_id=tools.id,
            supplier_id=globaltools.id,
            purchase_price=Decimal("300.00"),
            selling_price=Decimal("800.00"),
            min_quantity=10,
        )
        monitor = Product(
            name="Monitor 27 inch",
            sku="MON001",
            category_id=electronics.id,
            supplier_id=techtrade.id,
            purchase_price=Decimal("25000.00"),
            selling_price=Decimal("35000.00"),
            min_quantity=5,
        )

        session.add_all([laptop, mouse, chair, paper, screwdriver, monitor])
        session.flush()

        movements = [
            StockMovement(
                product_id=laptop.id,
                movement_type="IN",
                quantity=10,
                comment="Поступление ноутбуков",
            ),
            StockMovement(
                product_id=mouse.id,
                movement_type="IN",
                quantity=30,
                comment="Поступление мышек",
            ),
            StockMovement(
                product_id=chair.id,
                movement_type="IN",
                quantity=15,
                comment="Поступление кресел",
            ),
            StockMovement(
                product_id=paper.id,
                movement_type="IN",
                quantity=200,
                comment="Поступление бумаги",
            ),
            StockMovement(
                product_id=screwdriver.id,
                movement_type="IN",
                quantity=25,
                comment="Поступление отвёрток",
            ),
            StockMovement(
                product_id=laptop.id,
                movement_type="OUT",
                quantity=2,
                comment="Списание ноутбуков",
            ),
            StockMovement(
                product_id=mouse.id,
                movement_type="OUT",
                quantity=5,
                comment="Списание мышек",
            ),
            StockMovement(
                product_id=paper.id,
                movement_type="OUT",
                quantity=80,
                comment="Списание бумаги",
            ),
            StockMovement(
                product_id=chair.id,
                movement_type="ADJUST",
                quantity=1,
                comment="Корректировка кресла",
            ),
        ]

        session.add_all(movements)
        session.commit()
        print("Seed-данные успешно добавлены!")


if __name__ == "__main__":
    seed()
