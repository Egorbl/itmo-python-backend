from uuid import uuid4

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from lecture_2.hw.shop_api.db.models import Item, Base, Cart, CartToItem
import random

engine = create_engine('postgresql+psycopg2://postgres:@localhost:5432')
Base.metadata.create_all(engine)

with Session(engine) as session:
    item_id = random.randint(1, 100000)
    dildo = Item(id=item_id, name="smth", price=228)

    cart_id = random.randint(1, 100000)
    new_cart = Cart(id=cart_id)

    rel_id = random.randint(1, 100000)
    dildo_to_cart = CartToItem(id=rel_id, item_id=item_id, cart_id=cart_id)

    session.add_all([dildo, new_cart, dildo_to_cart])
    session.commit()

    stmt = select(CartToItem)

    rows = session.execute(stmt)
    for row in rows:
        print(row)

    print("____")

