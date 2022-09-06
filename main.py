from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# var_url = 'mongodb+srv://shubham3408:Ab167501026*@cluster0.d4acmgn.mongodb.net/?retryWrites=true&w=majority'

# client = MongoClient(var_url)
# mydb = client['DataPoem']
# mycol = mydb['ProductsData']

@app.get("/", response_class=HTMLResponse)
def read_root(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})            
    

SECRET_KEY = "f611fc53ccc7a0924a5b884960830c07ccbc601b67ef418907a335b4662b18d8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

fake_products_db = [
{
    "id": 1,
    "title": "iPhone 9",
    "description": "An apple mobile which is nothing like apple",
    "price": 549,
    "discountPercentage": 12.96,
    "rating": 4.69,
    "stock": 94,
    "brand": "Apple",
    "category": "smartphones",
    "thumbnail": "https://dummyjson.com/image/i/products/1/thumbnail.jpg",
    "images": [
    "https://dummyjson.com/image/i/products/1/1.jpg",
    "https://dummyjson.com/image/i/products/1/2.jpg",
    "https://dummyjson.com/image/i/products/1/3.jpg",
    "https://dummyjson.com/image/i/products/1/4.jpg",
    "https://dummyjson.com/image/i/products/1/thumbnail.jpg"
    ]
},
{
    "id": 2,
    "title": "iPhone X",
    "description": "SIM-Free, Model A19211 6.5-inch Super Retina HD display with OLED technology A12 Bionic chip with ...",
    "price": 899,
    "discountPercentage": 17.94,
    "rating": 4.44,
    "stock": 34,
    "brand": "Apple",
    "category": "smartphones",
    "thumbnail": "https://dummyjson.com/image/i/products/2/thumbnail.jpg",
    "images": [
    "https://dummyjson.com/image/i/products/2/1.jpg",
    "https://dummyjson.com/image/i/products/2/2.jpg",
    "https://dummyjson.com/image/i/products/2/3.jpg",
    "https://dummyjson.com/image/i/products/2/thumbnail.jpg"
    ]
},
{
    "id": 3,
    "title": "Samsung Universe 9",
    "description": "Samsung's new variant which goes beyond Galaxy to the Universe",
    "price": 1249,
    "discountPercentage": 15.46,
    "rating": 4.09,
    "stock": 36,
    "brand": "Samsung",
    "category": "smartphones",
    "thumbnail": "https://dummyjson.com/image/i/products/3/thumbnail.jpg",
    "images": [
    "https://dummyjson.com/image/i/products/3/1.jpg"
    ]
},
{
    "id": 4,
    "title": "OPPOF19",
    "description": "OPPO F19 is officially announced on April 2021.",
    "price": 280,
    "discountPercentage": 17.91,
    "rating": 4.3,
    "stock": 123,
    "brand": "OPPO",
    "category": "smartphones",
    "thumbnail": "https://dummyjson.com/image/i/products/4/thumbnail.jpg",
    "images": [
    "https://dummyjson.com/image/i/products/4/1.jpg",
    "https://dummyjson.com/image/i/products/4/2.jpg",
    "https://dummyjson.com/image/i/products/4/3.jpg",
    "https://dummyjson.com/image/i/products/4/4.jpg",
    "https://dummyjson.com/image/i/products/4/thumbnail.jpg"
    ]
},
{
    "id": 5,
    "title": "Huawei P30",
    "description": "Huawei’s re-badged P30 Pro New Edition was officially unveiled yesterday in Germany and now the device has made its way to the UK.",
    "price": 499,
    "discountPercentage": 10.58,
    "rating": 4.09,
    "stock": 32,
    "brand": "Huawei",
    "category": "smartphones",
    "thumbnail": "https://dummyjson.com/image/i/products/5/thumbnail.jpg",
    "images": [
    "https://dummyjson.com/image/i/products/5/1.jpg",
    "https://dummyjson.com/image/i/products/5/2.jpg",
    "https://dummyjson.com/image/i/products/5/3.jpg"
    ]
},
{
    "id": 6,
    "title": "MacBook Pro",
    "description": "MacBook Pro 2021 with mini-LED display may launch between September, November",
    "price": 1749,
    "discountPercentage": 11.02,
    "rating": 4.57,
    "stock": 83,
    "brand": "APPle",
    "category": "laptops",
    "thumbnail": "https://dummyjson.com/image/i/products/6/thumbnail.png",
    "images": [
    "https://dummyjson.com/image/i/products/6/1.png",
    "https://dummyjson.com/image/i/products/6/2.jpg",
    "https://dummyjson.com/image/i/products/6/3.png",
    "https://dummyjson.com/image/i/products/6/4.jpg"
    ]
},
{
    "id": 7,
    "title": "Samsung Galaxy Book",
    "description": "Samsung Galaxy Book S (2020) Laptop With Intel Lakefield Chip, 8GB of RAM Launched",
    "price": 1499,
    "discountPercentage": 4.15,
    "rating": 4.25,
    "stock": 50,
    "brand": "Samsung",
    "category": "laptops",
    "thumbnail": "https://dummyjson.com/image/i/products/7/thumbnail.jpg",
    "images": [
    "https://dummyjson.com/image/i/products/7/1.jpg",
    "https://dummyjson.com/image/i/products/7/2.jpg",
    "https://dummyjson.com/image/i/products/7/3.jpg",
    "https://dummyjson.com/image/i/products/7/thumbnail.jpg"
    ]
},
{
    "id": 8,
    "title": "Microsoft Surface Laptop 4",
    "description": "Style and speed. Stand out on HD video calls backed by Studio Mics. Capture ideas on the vibrant touchscreen.",
    "price": 1499,
    "discountPercentage": 10.23,
    "rating": 4.43,
    "stock": 68,
    "brand": "Microsoft Surface",
    "category": "laptops",
    "thumbnail": "https://dummyjson.com/image/i/products/8/thumbnail.jpg",
    "images": [
    "https://dummyjson.com/image/i/products/8/1.jpg",
    "https://dummyjson.com/image/i/products/8/2.jpg",
    "https://dummyjson.com/image/i/products/8/3.jpg",
    "https://dummyjson.com/image/i/products/8/4.jpg",
    "https://dummyjson.com/image/i/products/8/thumbnail.jpg"
    ]
},
{
    "id": 9,
    "title": "Infinix INBOOK",
    "description": "Infinix Inbook X1 Ci3 10th 8GB 256GB 14 Win10 Grey – 1 Year Warranty",
    "price": 1099,
    "discountPercentage": 11.83,
    "rating": 4.54,
    "stock": 96,
    "brand": "Infinix",
    "category": "laptops",
    "thumbnail": "https://dummyjson.com/image/i/products/9/thumbnail.jpg",
    "images": [
    "https://dummyjson.com/image/i/products/9/1.jpg",
    "https://dummyjson.com/image/i/products/9/2.png",
    "https://dummyjson.com/image/i/products/9/3.png",
    "https://dummyjson.com/image/i/products/9/4.jpg",
    "https://dummyjson.com/image/i/products/9/thumbnail.jpg"
    ]
},
{
    "id": 10,
    "title": "HP Pavilion 15-DK1056WM",
    "description": "HP Pavilion 15-DK1056WM Gaming Laptop 10th Gen Core i5, 8GB, 256GB SSD, GTX 1650 4GB, Windows 10",
    "price": 1099,
    "discountPercentage": 6.18,
    "rating": 4.43,
    "stock": 89,
    "brand": "HP Pavilion",
    "category": "laptops",
    "thumbnail": "https://dummyjson.com/image/i/products/10/thumbnail.jpeg",
    "images": [
    "https://dummyjson.com/image/i/products/10/1.jpg",
    "https://dummyjson.com/image/i/products/10/2.jpg",
    "https://dummyjson.com/image/i/products/10/3.jpg",
    "https://dummyjson.com/image/i/products/10/thumbnail.jpeg"
    ]
}
]

@app.get("/get_all_products")                                    #http://127.0.0.1:8000/get_all_products
async def get_all_products(): 
    # list = mycol.find({}, {"_id": 0})
    # new_list = []
    # for doc in list:
    #     new_list.append(doc)
    # products_list = {"products":new_list}
    products_list = {"products":fake_products_db}
    return products_list

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def verify_password(plain_password, hashed_password):
    # print(hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_class=HTMLResponse)
async def login_for_access_token(request: Request,form_data: OAuth2PasswordRequestForm = Depends()):
    # print(form_data)
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    # return {"success": True,"access_token": access_token}
    # with open("templates/index.html") as f:
    #     return HTMLResponse(content=f.read(), status_code=200)
    return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/login/")
# async def login(username: str = Form(), password: str = Form()):
#     return {"username": username}

# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]



# @app.get("/login")
# async def login(token: str = Depends(oauth2_scheme)):
#     print(token)                                                     #If it prints, it means user has been verified
#     return {
#         "success": True,
#         "message": "user is logged in"
#     }
    
