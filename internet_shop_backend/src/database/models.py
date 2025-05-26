from typing import List
from datetime import datetime
from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from src.database.base import Base
from src.database.associative import rev_prod_assoc, user_prod_cart_assoc, user_shop_list_assoc, shop_list_prod_assoc


@dataclass
class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(), primary_key=True, default=uuid4().hex)
    text: Mapped[str] = mapped_column(String())
    rating: Mapped[float] = mapped_column()
    author: Mapped[str] = mapped_column(String())


@dataclass
class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    img_url: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column()
    reviews: Mapped[List[Review]] = relationship(secondary=rev_prod_assoc)


@dataclass
class ShopList(Base):
    __tablename__ = "shop_list"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    products: Mapped[List[Product]] = relationship(secondary=shop_list_prod_assoc)


@dataclass
class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    _password: Mapped[str] = mapped_column(String(), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    products_cart: Mapped[List[Product]] = relationship(secondary=user_prod_cart_assoc)
    shop_list: Mapped[List[ShopList]] = relationship(secondary=user_shop_list_assoc)

    @property
    def password(self):
        return "Don't use this"

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)


    def get_tokens(self, pwd):
        if check_password_hash(self._password, pwd):
            return {
                "accesss_token": create_access_token(identity=self.id),
                "refresh_token": create_refresh_token(identity=self.id)
            }
