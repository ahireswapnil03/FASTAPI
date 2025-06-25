from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import models, schemas, crud, database, auth
from .database import engine
from .deps import get_db
from .deps import get_current_user
from .schemas import ProductCreate, ProductOut, ProductBulkCreate
from .crud import create_product, update_product, delete_product, create_products_bulk


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user

@app.post("/products/", response_model=ProductOut)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_product(db, product, user_id=current_user.id)

@app.get("/products/", response_model=list[ProductOut])
def list_my_products(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(models.Product).filter(models.Product.user_id == current_user.id).all()

@app.put("/products/{product_id}", response_model=ProductOut)
def update_my_product(product: ProductCreate, product_id: int = Path(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    updated = update_product(db, product_id, product, user_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found or not owned by user")
    return updated

@app.delete("/products/{product_id}", response_model=ProductOut)
def delete_my_product(product_id: int = Path(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    deleted = delete_product(db, product_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found or not owned by user")
    return deleted

@app.post("/products/bulk", response_model=list[ProductOut])
def create_products_in_bulk(bulk: ProductBulkCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_products_bulk(db, bulk.products, user_id=current_user.id)
