from lecture_2.hw.shop_api.db.session import get_session, get_connection_pool
from models import Cart, Item, CartToItem

engine = get_connection_pool()
session = get_session(engine)

session.query(Cart).delete()
session.query(Item).delete()
session.query(CartToItem).delete()

session.commit()