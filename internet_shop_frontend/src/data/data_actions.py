import os


import requests
from dotenv import load_dotenv
from flask import session, flash

load_dotenv()
PRODS_URL = os.getenv("PRODS_URL")
USER_URL = os.getenv("USER_URL")
TOKEN_URL = os.getenv("TOKEN_URL")


def get_product(prod_id: str, url: str = PRODS_URL)-> dict:
    return requests.get(url + prod_id).json()


def get_products(url: str = PRODS_URL)-> dict:
    return requests.get(url).json()


def del_product(prod_id: str, url: str = PRODS_URL)-> dict:
    return requests.delete(url + prod_id).json()


def add_product(name: str, description: str, img_url: str, price: float, url: str = PRODS_URL) -> dict:
    body = dict(
        name=name,
        description=description,
        img_url=img_url,
        price=price
    )

    return requests.post(url, json=body).json()


def update_product(
    prod_id: str,
    name: str,
    description: str,
    img_url: str,
    price: float,
    url: str = PRODS_URL
) -> dict:

    body = dict(
        name=name,
        description=description,
        img_url=img_url,
        price=price
    )

    return requests.put(url + prod_id, json=body).json()



def signup(
    email: str,
    password: str,
    first_name:str|None = None,
    last_name:str|None = None,
    url: str = USER_URL
):
    body = dict(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )

    resp = requests.post(url, json=body)
    if resp.status_code == 201:
        flash("Користувач успішно зареєстрований!")



def login(email: str, password: str, url: str = TOKEN_URL):
    body = dict(email=email, password=password)
    resp = requests.post(url, json=body)
    if resp.status_code == 200:
        session.update(resp.json())
        return("Вхід успішний!")
    else:
        flash("Логін або пароль не вірний.")



def get_user(url: str = USER_URL):
    header = dict(
        Authorization=f"Bearer {session.get("access_token")}"
    )
    resp = requests.get(url, headers=header)
    if resp.status_code == 200:
        return resp.json()
    else:
        return get_new_token()
    

def get_new_token(url: str = TOKEN_URL):
    header = dict(
        Authorization=f"Bearer {session.get("refresh_token")}"
    )

    resp = requests.get(url, headers=header)
    if resp.status_code == 200:
        session.update(resp.json())
        return get_user()