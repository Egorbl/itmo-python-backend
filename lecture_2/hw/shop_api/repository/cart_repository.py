from itertools import count

from fastapi import HTTPException
from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session

from lecture_2.hw.shop_api.db.models import Cart, CartToItem, Item

def serialize_cart(cart: Cart, items):
    serialized_cart = {"id": cart.id, "price": cart.price, "items": []}

    for item, quantity in items.items():
        serialized_cart["items"].append({
            "id": item.id, "name": item.name, "quantity": quantity, "available": not item.deleted
        })

    return serialized_cart


def get_carts(session: Session,
             offset: int = 0, limit: int = 10, min_price: int = None, max_price: int = None,
             min_quantity: int = None, max_quantity: int = None):
    if offset < 0 or limit <= 0:
        raise HTTPException(status_code=422, detail="Offset and limit must be positive")

    query = select(Cart).offset(offset).limit(limit)

    if min_price is not None:
        if min_price < 0:
            raise HTTPException(status_code=422, detail="Min price must be positive")
        query = query.where(Cart.price >= min_price)
    if max_price is not None:
        if max_price < 0:
            raise HTTPException(status_code=422, detail="Max price must be positive")
        query = query.where(Cart.price <= max_price)
    if min_quantity is not None:
        if min_quantity < 0:
            raise HTTPException(status_code=422, detail="Min quantity must be positive")
        query = query.where(Cart.quantity >= min_quantity)
    if max_quantity is not None:
        if max_quantity < 0:
            raise HTTPException(status_code=422, detail="Max quantity must be positive")
        query = query.where(Cart.quantity <= max_quantity)

    carts = session.execute(query).scalars().all()
    carts_with_items = [get_cart_with_items(session, cart.id) for cart in carts]

    return carts_with_items

def get_cart_with_items(session: Session, cart_id):
    query = select(Cart).where(Cart.id == cart_id)
    cart = session.execute(query).scalar()

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    items = get_items_for_cart(session, cart)
    return serialize_cart(cart, items)
    

def get_items_for_cart(session: Session, cart: Cart):
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    query = select(CartToItem).where(CartToItem.cart_id == cart.id)
    items_to_cart = session.execute(query).scalars().all()
    items_id = [item_to_cart.item_id for item_to_cart in items_to_cart]
    query = select(Item).where(Item.id.in_(items_id))
    items = session.execute(query)
    items = items.scalars().all()

    items_quantity = dict()

    for item_id in items_id:
        for item in items:
            if item.id != item_id:
                continue
            items_quantity[item] = items_quantity.get(item, 0) + 1

    return items_quantity

def get_item_by_id(session: Session, item_id):
    query = select(Item).where(Item.id == item_id)
    item = session.execute(query).scalar()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def get_cart_by_id(session: Session, cart_id):
    query = select(Cart).where(Cart.id == cart_id)
    cart = session.execute(query).scalar_one_or_none()

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart

def search_items(session, offset: int = 0, limit: int = 10, min_price: int = None, max_price: int = None,
             show_deleted: bool = False):
    if offset < 0 or limit <= 0:
        raise HTTPException(status_code=422, detail="Offset and limit must be positive")

    query = select(Item).offset(offset).limit(limit)
    if min_price is not None:
        if min_price < 0:
            raise HTTPException(status_code=422, detail="Min price must be positive")
        query = query.where(Item.price >= min_price)

    if max_price is not None:
        if max_price < 0:
            raise HTTPException(status_code=422, detail="Max price must be positive")
        query = query.where(Item.price <= max_price)

    if not show_deleted:
        query = query.where(Item.deleted == False)
    items = session.execute(query).scalars().all()
    return items