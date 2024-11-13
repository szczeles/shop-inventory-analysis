# generated using https://github.com/agronholm/sqlacodegen
# sqlacodegen postgresql://postgres:products@localhost/postgres | sed -e's/Products/Product/g' -e's/ProductAlternates/ProductAlternate/g' > products_api/models.py

import datetime
import decimal
from typing import List, Optional

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        PrimaryKeyConstraint("product_id", name="products_pkey"),
        UniqueConstraint("upc", name="products_upc_key"),
    )

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    upc: Mapped[Optional[str]] = mapped_column(String(14))
    name: Mapped[Optional[str]] = mapped_column(Text)
    item_number: Mapped[Optional[int]] = mapped_column(Integer)
    price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    supplier: Mapped[Optional[str]] = mapped_column(Text)
    inventory_level: Mapped[Optional[int]] = mapped_column(Integer)
    inventory_updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    product_alternates: Mapped[List["ProductAlternate"]] = relationship(
        "ProductAlternate", back_populates="product"
    )


class ProductAlternate(Base):
    __tablename__ = "product_alternates"
    __table_args__ = (
        ForeignKeyConstraint(
            ["product_id"], ["products.product_id"], name="fk_product"
        ),
        PrimaryKeyConstraint("product_alternate_id", name="product_alternates_pkey"),
    )

    product_alternate_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[Optional[int]] = mapped_column(Integer)
    upc: Mapped[Optional[str]] = mapped_column(String(14))
    alternate_type: Mapped[Optional[str]] = mapped_column(
        Enum("variant", "case", name="alternate_type")
    )
    case_pack: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    product: Mapped["Product"] = relationship(
        "Product", back_populates="product_alternates"
    )
