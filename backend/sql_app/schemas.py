# from typing import *

from pydantic import BaseModel

# Before creating an item, we don't know what will be the ID
# assigned to it, but when reading it (when returning it from the API)
# we will already know its ID.


class RestaurantBase(BaseModel):
    name: str


class RestaurantCreate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int

    class Config:
        orm_mode = True


class MenuItemBase(BaseModel):
    name: str
    description: str
    price: float
    course: str
    restaurant_id: int


class MenuItemCreate(MenuItemBase):
    pass


class MenuItem(MenuItemBase):
    id: int

    class Config:
        orm_mode = True
