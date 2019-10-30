from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    # items = relationship("MenuItem", back_populates="restaurant_id")


class MenuItem(Base):
    __tablename__ = "menu_item"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))

    # restaurant = relationship("Restaurant", back_populates="items")
    restaurant = relationship(Restaurant)
