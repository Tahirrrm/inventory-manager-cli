from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from database import SessionLocal
from models import Category, Product, StockMovement, Supplier


def create_category(name: str):
    with SessionLocal() as session:
        try:
            category = Category(name=name)
            session.add(category)
            session.commit()
            session.refresh(category)
            return category
        except IntegrityError:
            session.rollback()
            print(f"Ошибка: категория с названием '{name}' уже существует.")
            return None


def get_all_categories():
    with SessionLocal() as session:
        stmt = select(Category).order_by(Category.id)
        return session.execute(stmt).scalars().all()


def get_category_by_id(category_id: int):
    with SessionLocal() as session:
        return session.get(Category, category_id)


def update_category_name(category_id: int, new_name: str):
    with SessionLocal() as session:
        try:
            category = session.get(Category, category_id)
            if category is None:
                print(f"Ошибка: категория с id {category_id} не найдена.")
                return None
            category.name = new_name
            session.commit()
            session.refresh(category)
            return category
        except IntegrityError:
            session.rollback()
            print(f"Ошибка: категория с названием '{new_name}' уже существует.")
            return None


def delete_category(category_id: int):
    with SessionLocal() as session:
        try:
            category = session.get(Category, category_id)
            if category is None:
                print(f"Ошибка: категория с id {category_id} не найдена.")
                return False

            product_count = session.execute(
                select(func.count(Product.id)).where(
                    Product.category_id == category_id
                )
            ).scalar()
            if product_count > 0:
                print("Нельзя удалить категорию, потому что в ней есть товары.")
                return False

            session.delete(category)
            session.commit()
            print(f"Категория '{category.name}' удалена.")
            return True
        except IntegrityError:
            session.rollback()
            print("Ошибка при удалении категории.")
            return False


def create_supplier(
    name: str,
    phone: str | None = None,
    email: str | None = None,
):
    with SessionLocal() as session:
        try:
            supplier = Supplier(name=name, phone=phone, email=email)
            session.add(supplier)
            session.commit()
            session.refresh(supplier)
            return supplier
        except IntegrityError:
            session.rollback()
            print("Ошибка: поставщик с таким именем или email уже существует.")
            return None


def get_all_suppliers():
    with SessionLocal() as session:
        stmt = select(Supplier).order_by(Supplier.id)
        return session.execute(stmt).scalars().all()


def get_supplier_by_id(supplier_id: int):
    with SessionLocal() as session:
        return session.get(Supplier, supplier_id)


def update_supplier_contacts(
    supplier_id: int,
    phone: str | None = None,
    email: str | None = None,
):
    with SessionLocal() as session:
        try:
            supplier = session.get(Supplier, supplier_id)
            if supplier is None:
                print(f"Ошибка: поставщик с id {supplier_id} не найден.")
                return None
            if phone is not None:
                supplier.phone = phone
            if email is not None:
                supplier.email = email
            session.commit()
            session.refresh(supplier)
            return supplier
        except IntegrityError:
            session.rollback()
            print("Ошибка: поставщик с таким email уже существует.")
            return None


def deactivate_supplier(supplier_id: int):
    with SessionLocal() as session:
        supplier = session.get(Supplier, supplier_id)
        if supplier is None:
            print(f"Ошибка: поставщик с id {supplier_id} не найден.")
            return None
        supplier.is_active = False
        session.commit()
        session.refresh(supplier)
        print(f"Поставщик '{supplier.name}' деактивирован.")
        return supplier


def delete_supplier(supplier_id: int):
    with SessionLocal() as session:
        try:
            supplier = session.get(Supplier, supplier_id)
            if supplier is None:
                print(f"Ошибка: поставщик с id {supplier_id} не найден.")
                return False

            product_count = session.execute(
                select(func.count(Product.id)).where(
                    Product.supplier_id == supplier_id
                )
            ).scalar()
            if product_count > 0:
                print(
                    "Нельзя удалить поставщика, "
                    "потому что к нему привязаны товары."
                )
                return False

            session.delete(supplier)
            session.commit()
            print(f"Поставщик '{supplier.name}' удалён.")
            return True
        except IntegrityError:
            session.rollback()
            print("Ошибка при удалении поставщика.")
            return False


def create_product(
    name: str,
    sku: str,
    category_id: int | None = None,
    supplier_id: int | None = None,
    purchase_price: Decimal | None = None,
    selling_price: Decimal | None = None,
    min_quantity: int | None = None,
):
    with SessionLocal() as session:
        try:
            if purchase_price is not None and purchase_price < 0:
                print("Ошибка: закупочная цена не может быть отрицательной.")
                return None
            if selling_price is not None and selling_price < 0:
                print("Ошибка: продажная цена не может быть отрицательной.")
                return None
            if min_quantity is not None and min_quantity < 0:
                print("Ошибка: минимальный остаток не может быть отрицательным.")
                return None

            if category_id is not None:
                category = session.get(Category, category_id)
                if category is None:
                    print(f"Ошибка: категория с id {category_id} не существует.")
                    return None

            if supplier_id is not None:
                supplier = session.get(Supplier, supplier_id)
                if supplier is None:
                    print(
                        f"Ошибка: поставщик с id {supplier_id} не существует."
                    )
                    return None

            product = Product(
                name=name,
                sku=sku,
                category_id=category_id,
                supplier_id=supplier_id,
                purchase_price=purchase_price,
                selling_price=selling_price,
                min_quantity=min_quantity,
            )
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
        except IntegrityError:
            session.rollback()
            print(f"Ошибка: товар с SKU '{sku}' уже существует.")
            return None


def get_all_products():
    with SessionLocal() as session:
        stmt = select(Product).order_by(Product.id)
        return session.execute(stmt).scalars().all()


def get_product_by_id(product_id: int):
    with SessionLocal() as session:
        return session.get(Product, product_id)


def get_products_by_category(category_id: int):
    with SessionLocal() as session:
        stmt = (
            select(Product)
            .where(Product.category_id == category_id)
            .order_by(Product.id)
        )
        return session.execute(stmt).scalars().all()


def get_products_by_supplier(supplier_id: int):
    with SessionLocal() as session:
        stmt = (
            select(Product)
            .where(Product.supplier_id == supplier_id)
            .order_by(Product.id)
        )
        return session.execute(stmt).scalars().all()


def update_product_prices(
    product_id: int,
    purchase_price: Decimal | None = None,
    selling_price: Decimal | None = None,
):
    with SessionLocal() as session:
        product = session.get(Product, product_id)
        if product is None:
            print(f"Ошибка: товар с id {product_id} не найден.")
            return None

        if purchase_price is not None:
            if purchase_price < 0:
                print("Ошибка: закупочная цена не может быть отрицательной.")
                return None
            product.purchase_price = purchase_price

        if selling_price is not None:
            if selling_price < 0:
                print("Ошибка: продажная цена не может быть отрицательной.")
                return None
            product.selling_price = selling_price

        session.commit()
        session.refresh(product)
        return product


def update_product_min_quantity(product_id: int, min_quantity: int):
    with SessionLocal() as session:
        product = session.get(Product, product_id)
        if product is None:
            print(f"Ошибка: товар с id {product_id} не найден.")
            return None

        if min_quantity < 0:
            print("Ошибка: минимальный остаток не может быть отрицательным.")
            return None

        product.min_quantity = min_quantity
        session.commit()
        session.refresh(product)
        return product


def deactivate_product(product_id: int):
    with SessionLocal() as session:
        product = session.get(Product, product_id)
        if product is None:
            print(f"Ошибка: товар с id {product_id} не найден.")
            return None
        product.is_active = False
        session.commit()
        session.refresh(product)
        print(f"Товар '{product.name}' деактивирован.")
        return product


def delete_product(product_id: int):
    with SessionLocal() as session:
        try:
            product = session.get(Product, product_id)
            if product is None:
                print(f"Ошибка: товар с id {product_id} не найден.")
                return False

            movement_count = session.execute(
                select(func.count(StockMovement.id)).where(
                    StockMovement.product_id == product_id
                )
            ).scalar()
            if movement_count > 0:
                print(
                    "Нельзя удалить товар, "
                    "потому что по нему уже есть складские операции."
                )
                return False

            session.delete(product)
            session.commit()
            print(f"Товар '{product.name}' удалён.")
            return True
        except IntegrityError:
            session.rollback()
            print("Ошибка при удалении товара.")
            return False


def create_stock_movement(
    product_id: int,
    movement_type: str,
    quantity: int,
    comment: str | None = None,
):
    with SessionLocal() as session:
        try:
            if movement_type not in ("IN", "OUT", "ADJUST"):
                print("Ошибка: тип операции должен быть IN, OUT или ADJUST.")
                return None

            if quantity <= 0:
                print("Ошибка: количество должно быть больше 0.")
                return None

            product = session.get(Product, product_id)
            if product is None:
                print(f"Ошибка: товар с id {product_id} не существует.")
                return None

            movement = StockMovement(
                product_id=product_id,
                movement_type=movement_type,
                quantity=quantity,
                comment=comment,
            )
            session.add(movement)
            session.commit()
            session.refresh(movement)
            return movement
        except IntegrityError:
            session.rollback()
            print("Ошибка при создании складской операции.")
            return None


def get_all_stock_movements():
    with SessionLocal() as session:
        stmt = select(StockMovement).order_by(
            StockMovement.created_at.desc(), StockMovement.id.desc()
        )
        return session.execute(stmt).scalars().all()


def get_movements_by_product(product_id: int):
    with SessionLocal() as session:
        stmt = (
            select(StockMovement)
            .where(StockMovement.product_id == product_id)
            .order_by(StockMovement.created_at.desc(), StockMovement.id.desc())
        )
        return session.execute(stmt).scalars().all()


def delete_stock_movement(movement_id: int):
    with SessionLocal() as session:
        try:
            movement = session.get(StockMovement, movement_id)
            if movement is None:
                print(f"Ошибка: операция с id {movement_id} не найдена.")
                return False
            session.delete(movement)
            session.commit()
            print("Операция удалена.")
            return True
        except IntegrityError:
            session.rollback()
            print("Ошибка при удалении операции.")
            return False
