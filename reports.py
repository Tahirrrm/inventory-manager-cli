from sqlalchemy import case, func, select

from database import SessionLocal
from models import Category, Product, StockMovement, Supplier


def get_products_with_category_and_supplier():
    """Товары с названиями категорий и поставщиков"""
    with SessionLocal() as session:
        stmt = (
            select(
                Product.id,
                Product.name,
                Product.sku,
                Category.name.label("category_name"),
                Supplier.name.label("supplier_name"),
                Product.purchase_price,
                Product.selling_price,
                Product.is_active,
            )
            .outerjoin(Category, Product.category_id == Category.id)
            .outerjoin(Supplier, Product.supplier_id == Supplier.id)
            .order_by(Product.id)
        )
        return session.execute(stmt).all()


def get_movements_with_product():
    """История операций с названием товара"""
    with SessionLocal() as session:
        stmt = (
            select(
                StockMovement.created_at,
                Product.name.label("product_name"),
                Product.sku,
                StockMovement.movement_type,
                StockMovement.quantity,
                StockMovement.comment,
            )
            .join(Product, StockMovement.product_id == Product.id)
            .order_by(
                StockMovement.created_at.desc(), StockMovement.id.desc()
            )
        )
        return session.execute(stmt).all()


def get_products_count_by_category():
    """Количество товаров в каждой категории"""
    with SessionLocal() as session:
        stmt = (
            select(
                Category.name,
                func.count(Product.id).label("product_count"),
            )
            .outerjoin(Product, Product.category_id == Category.id)
            .group_by(Category.name)
            .order_by(Category.name)
        )
        return session.execute(stmt).all()


def get_products_count_by_supplier():
    """Количество товаров у каждого поставщика"""
    with SessionLocal() as session:
        stmt = (
            select(
                Supplier.name,
                func.count(Product.id).label("product_count"),
            )
            .outerjoin(Product, Product.supplier_id == Supplier.id)
            .group_by(Supplier.name)
            .order_by(Supplier.name)
        )
        return session.execute(stmt).all()


def _stock_subquery(session):
    """Вспомогательная функция: подзапрос остатка для каждого товара"""
    in_adjust = case(
        (StockMovement.movement_type.in_(["IN", "ADJUST"]), StockMovement.quantity),
        else_=0,
    )
    out = case(
        (StockMovement.movement_type == "OUT", StockMovement.quantity),
        else_=0,
    )

    subq = (
        select(
            Product.id,
            Product.name,
            Product.purchase_price,
            Product.selling_price,
            Product.min_quantity,
            (
                func.coalesce(func.sum(in_adjust), 0)
                - func.coalesce(func.sum(out), 0)
            ).label("current_stock"),
        )
        .outerjoin(StockMovement, Product.id == StockMovement.product_id)
        .group_by(
            Product.id,
            Product.name,
            Product.purchase_price,
            Product.selling_price,
            Product.min_quantity,
        )
    ).subquery()

    return subq


def get_current_stock_by_product():
    """Текущий остаток по каждому товару"""
    with SessionLocal() as session:
        subq = _stock_subquery(session)
        stmt = select(
            subq.c.id,
            subq.c.name,
            subq.c.current_stock,
        ).order_by(subq.c.id)
        return session.execute(stmt).all()


def get_low_stock_products():
    """Товары, которые заканчиваются"""
    with SessionLocal() as session:
        subq = _stock_subquery(session)
        stmt = (
            select(subq)
            .where(subq.c.current_stock <= subq.c.min_quantity)
            .order_by(subq.c.id)
        )
        return session.execute(stmt).all()


def get_total_purchase_value():
    """Общая закупочная стоимость склада"""
    with SessionLocal() as session:
        subq = _stock_subquery(session)
        stmt = select(
            func.coalesce(
                func.sum(subq.c.current_stock * subq.c.purchase_price), 0
            ).label("total_value")
        )
        return session.execute(stmt).scalar()


def get_total_selling_value():
    """Потенциальная выручка склада"""
    with SessionLocal() as session:
        subq = _stock_subquery(session)
        stmt = select(
            func.coalesce(
                func.sum(subq.c.current_stock * subq.c.selling_price), 0
            ).label("total_value")
        )
        return session.execute(stmt).scalar()


def get_potential_profit():
    """Потенциальная прибыль склада"""
    with SessionLocal() as session:
        subq = _stock_subquery(session)
        stmt = select(
            func.coalesce(
                func.sum(
                    subq.c.current_stock
                    * (subq.c.selling_price - subq.c.purchase_price)
                ),
                0,
            ).label("total_profit")
        )
        return session.execute(stmt).scalar()
