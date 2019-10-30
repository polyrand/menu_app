from sqlalchemy.orm import Session

from . import models, schemas

# filter vs filter_by:
# https://stackoverflow.com/a/2128558


# RESTAURANTS
def get_restaurants(db: Session):
    return db.query(models.Restaurant).all()


def get_restaurant(db: Session, restaurant_id: int):
    return (
        db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).one()
    )


def get_restaurant_by_name(db: Session, name: str):
    return db.query(models.Restaurant).filter(models.Restaurant.name == name).one()


def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(name=restaurant.name)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


# MENU ITEMS
def get_all_menu_items(db: Session):
    return db.query(models.MenuItem).all()


def get_menu_items(db: Session, restaurant_id: int):
    # restaurant = get_restaurant(db=db, restaurant_id=restaurant_id)
    return (
        db.query(models.MenuItem)
        .filter(models.MenuItem.restaurant_id == restaurant_id)
        .all()
    )


def create_menu_item(db: Session, item: schemas.MenuItemCreate, restaurant_id: int):
    name = item.name
    description = item.description
    price = item.price
    course = item.course
    restaurant_id = restaurant_id

    db_item = models.MenuItem(
        name=name,
        description=description,
        price=price,
        course=course,
        restaurant_id=restaurant_id,
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_menu_item(db: Session, restaurant_id: int, menu_id: int):

    # !!!
    # review form data from FastAPI docs
    db_item_edit = db.query(models.MenuItem).filter(models.MenuItem.id == menu_id).one()

    db.add(db_item_edit)
    db.commit()
    db.refresh(db_item_edit)

    return db_item_edit


def delete_menu_item(db: Session, restaurant_id: int, menu_id: int):
    db_item_delete = db.query(models.MenuItem).filter(models.MenuItem.id == menu_id)

    db.delete(db_item_delete)
    db.comit()
    db.refresh(db_item_delete)

    return db_item_delete
