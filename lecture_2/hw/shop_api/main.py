import random
from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.openapi.models import Response
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from lecture_2.hw.shop_api.db.session import get_session
from lecture_2.hw.shop_api.dto.item import CreateItemRequest, Item, Cart, PatchItemRequest

from lecture_2.hw.shop_api.db.models import Item as dbItem
from lecture_2.hw.shop_api.db.models import CartToItem as dbCartToItem
from lecture_2.hw.shop_api.db.models import Cart as dbCart
from lecture_2.hw.shop_api.repository.cart_repository import get_carts, get_item_by_id, get_cart_by_id, get_cart_with_items, search_items

app = FastAPI(title="shop_api")

@app.get("/cart")
def get_cart(session: Annotated[Session, Depends(get_session)],
             offset: int = 0, limit: int = 10, min_price: int = None, max_price: int = None,
             min_quantity: int = None, max_quantity: int = None):
    carts = get_carts(session, offset, limit, min_price, max_price, min_quantity, max_quantity)

    return carts

@app.get("/cart/{cart_id}")
def get_one_cart(session: Annotated[Session, Depends(get_session)], cart_id: int):
    cart = get_cart_with_items(session, cart_id)
    return cart

@app.post("/item", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(request: CreateItemRequest, session: Annotated[Session, Depends(get_session)]):
    item = Item(id=random.randint(1, 10000000), name=request.name, price=request.price, deleted=False)
    session.add(dbItem(id=item.id, name=item.name, price=item.price, deleted=False))
    session.commit()

    return JSONResponse(content=item.model_dump(mode="json"),
                        status_code=status.HTTP_201_CREATED, headers={"location": f"item/{item.id}"})

@app.get("/item")
def get_items(session: Annotated[Session, Depends(get_session)],
             offset: int = 0, limit: int = 10, min_price: int = None, max_price: int = None,
             show_deleted: bool = False):
    return search_items(session, offset, limit, min_price, max_price, show_deleted)

@app.get("/item/{item_id}", response_model=Item)
def get_item(session: Annotated[Session, Depends(get_session)], item_id: int):
    item = get_item_by_id(session, item_id)

    if item.deleted:
        raise HTTPException(404, "Item deleted")

    return Item(id=item.id, name=item.name, price=item.price, deleted=item.deleted)

@app.post("/cart", status_code=status.HTTP_201_CREATED)
def create_cart(session: Annotated[Session, Depends(get_session)]):
    cart_id = random.randint(1, 10000000)
    cart = Cart(id=cart_id)
    session.add(dbCart(id=cart.id, price=0.0, quantity=0))
    session.commit()
    return JSONResponse(content={"id": cart.id}, status_code=status.HTTP_201_CREATED,
                        headers={"location": f"cart/{cart.id}"})

@app.post("/cart/{cart_id}/add/{item_id}", status_code=status.HTTP_201_CREATED)
def add_item_to_cart(session: Annotated[Session, Depends(get_session)], cart_id: int, item_id: int):
    item = get_item_by_id(session, item_id)
    cart = get_cart_by_id(session, cart_id)

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    session.add(dbCartToItem(id=random.randint(1, 1000000), cart_id=cart.id, item_id=item.id))
    cart.price += item.price
    cart.quantity += 1
    session.commit()

    return "All good"

@app.delete("/item/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(session: Annotated[Session, Depends(get_session)], item_id: int):
    item = get_item_by_id(session, item_id)
    item.deleted = True
    session.commit()

    return Item(id=item.id, name=item.name, price=item.price, deleted=item.deleted)


@app.put("/item/{item_id}")
def update_item(request: CreateItemRequest, session: Annotated[Session, Depends(get_session)], item_id: int):
    item = get_item_by_id(session, item_id)
    item.price = request.price
    item.name = request.name
    item.deleted = False
    session.commit()
    return Item(id=item.id, name=item.name, price=item.price, deleted=item.deleted)

@app.patch("/item/{item_id}")
def patch_item(request: PatchItemRequest, session: Annotated[Session, Depends(get_session)], item_id: int):
    item = get_item_by_id(session, item_id)

    if item.deleted:
        raise HTTPException(status_code=304, detail="Item deleted")

    if request.name is not None:
        item.name = request.name

    if request.price is not None:
        item.price = request.price

    session.commit()
    return Item(id=item.id, name=item.name, price=item.price, deleted=item.deleted)