from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None

def create_product(db: Session, product: schemas.ProductCreate, user_id: int):
    db_product = models.Product(name=product.name, description=product.description, user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate, user_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.user_id == user_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.image_url = product.image_url
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int, user_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.user_id == user_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def create_products_bulk(db: Session, products: list[schemas.ProductCreate], user_id: int):
    db_products = [models.Product(name=prod.name, description=prod.description, user_id=user_id) for prod in products]
    db.add_all(db_products)
    db.commit()
    for prod in db_products:
        db.refresh(prod)
    return db_products
