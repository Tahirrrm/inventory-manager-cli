from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default=text("TRUE")
    )
    created_at: Mapped[date] = mapped_column(
        Date, server_default=text("CURRENT_DATE")
    )

    products: Mapped[list["Product"]] = relationship(back_populates="supplier")


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint(
            "purchase_price >= 0",
            name="check_purchase_price_non_negative",
        ),
        CheckConstraint(
            "selling_price >= 0",
            name="check_selling_price_non_negative",
        ),
        CheckConstraint(
            "min_quantity >= 0",
            name="check_min_quantity_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    sku: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    supplier_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("suppliers.id"), nullable=True
    )
    purchase_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    selling_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    min_quantity: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default=text("TRUE")
    )
    created_at: Mapped[date] = mapped_column(
        Date, server_default=text("CURRENT_DATE")
    )

    category: Mapped[Optional["Category"]] = relationship(
        back_populates="products"
    )
    supplier: Mapped[Optional["Supplier"]] = relationship(
        back_populates="products"
    )
    stock_movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="product"
    )


class StockMovement(Base):
    __tablename__ = "stock_movements"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="check_quantity_positive",
        ),
        CheckConstraint(
            "movement_type IN ('IN', 'OUT', 'ADJUST')",
            name="check_movement_type",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )
    movement_type: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[date] = mapped_column(
        Date, server_default=text("CURRENT_DATE")
    )

    product: Mapped["Product"] = relationship(back_populates="stock_movements")
