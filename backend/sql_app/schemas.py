from typing import *

from pydantic import BaseModel


class Restaurant(BaseModel):

    id: int
    name: str


class MenuItem(BaseModel):

    name: str
    id: int
    description: str
    price: float
    course: str
    restaurant_id: int
