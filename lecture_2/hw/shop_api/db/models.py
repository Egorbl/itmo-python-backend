from typing import List

# from pydantic.v1 import UUID4
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
     pass

class Item(Base):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    deleted: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"item {self.id} name {self.name} price {self.price}\n"

class Cart(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column()
    quantity: Mapped[int] = mapped_column()

    def __repr__(self):
        return f"cart {self.id}"


class CartToItem(Base):
    __tablename__ = 'cart_to_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column()
    item_id: Mapped[int] = mapped_column()

    def __repr__(self):
        return f"cart_to_items {self.cart_id} {self.item_id}"