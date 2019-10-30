from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
# We need to have an independent database session/connection (SessionLocal)
# per request, use the same session through all the request and then close
# it after the request is finished.

# And then a new session will be created for the next request.

# For that, we will create a new dependency with yield, as explained before
# in the section about Dependencies with yield.

# Our dependency will create a new SQLAlchemy SessionLocal that will be used
# in a single request, and then close it once the request is finished.

# We put the creation of the SessionLocal() and
# handling of the requests in a try block.

# And then we close it in the finally block.

# This way we make sure the database session is always closed after
# the request. Even if there was an exception while processing the request.


def get_db():
    """DB dependency."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# RESTAURANTS
@app.get("/restaurant/", response_model=List[schemas.Restaurant])
def read_restaurants(db: Session = Depends(get_db)):
    """Read all restaurants."""
    restaurants = crud.get_restaurants(db)
    return restaurants


@app.get("/restaurant/{restaurant_id}", response_model=schemas.Restaurant)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """Read single restaurant id, returns: name."""
    db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=400, detail="User not found")
    return db_restaurant


@app.post("/restaurant/", response_model=schemas.Restaurant)
def create_restaurant(
    restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)
):
    """Create new restaurant (name)."""
    db_restaurant = crud.get_restaurant_by_name(db, name=restaurant.name)
    if db_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant already registered")
    return crud.create_restaurant(db=db, restaurant=restaurant)


# MENU ITEMS
@app.get("/menus/", response_model=List[schemas.MenuItem])
def read_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
    """Read ALL menu items."""
    menu_items = crud.get_all_menu_items(db)
    return menu_items


@app.get("/restaurant/{restaurant_id}/menu", response_model=List[schemas.MenuItem])
def read_menu_item(restaurant_id: int, db: Session = Depends(get_db)):
    """Read menu items from single restaurant."""
    menu_items = crud.get_menu_items(db, restaurant_id=restaurant_id)
    return menu_items


@app.post("restaurant/{restaurant_id}/", response_model=schemas.MenuItem)
def create_menu_item(
    menu_item: schemas.MenuItemCreate, restaurant_id: int, db: Session = Depends(get_db)
):
    """Create new menu item."""
    # db_restaurant_menu_items = crud.get_menu_items(db, restaurant_id=restaurant_id)
    # Here we don't check since we can have the same menu item
    # multiple times. A restaurant may have the same dish for example
    # for different courses of different prices ¯\_(ツ)_/¯
    # if db_menu_item:
    #     raise HTTPException(status_code=400, detail="Item already exist")

    return crud.create_menu_item(db=db, item=menu_item, restaurant_id=restaurant_id)


@app.post("restaurant/{restaurant_id}/delete", response_model=schemas.MenuItem)
def delete_menu_item(restaurant_id: int, menu_id: int, db: Session = Depends(get_db)):
    """Delete menu item (menu_id) from restaurant (restaurant_id)."""
    return crud.delete_menu_item(db=db, restaurant_id=restaurant_id, menu_id=menu_id)


def update_menu_item(db: Session = Depends(get_db)):
    """Update menu item."""
    pass
