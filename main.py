from fastapi import FastAPI
from enum import Enum
from typing import Union

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


### Use type parameters to have automatic data validation
@app.get("/items/{item_id}")
async def read_item(item_id: int):
  return {"item_id": item_id}

##

### Order matters
# If the second path goes first, it can give an error
@app.get("/users/me")
async def read_user_me():
  return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
  return {"user_id": user_id}

##

### Predefined values
# This is converted to a dropdown menu in the swagger UI
class ModelName(str, Enum):
  alexnet = "alexnet"
  resnet = "restnet"
  lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
  # One way to get the Enum value
  if model_name == ModelName.alexnet:
    # return enumeration members - they will be converted to their corresponding values (str here) before returning them to the client
    return {"model_name": model_name, "message": "Deep Learning FTW!"}
  
  # Another way to get the Enum value
  if model_name.value == "lenet":
    return {"model_name": model_name, "message": "LeCNN all images"}

  # Third option: ModelName.lenet.value == "lenet"
  
  return {"model_name": model_name, "message": "Have some residuals"}

##

### Path parameters containing paths (not possible with OpenAPI)
# Using an option from Starlette
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
  return {"file_path": file_path}

##

### Query Parameters
# When declaring parameters not used in the path, it will be interpreted as "query" parameters (you can see it in the Swagger UI)

fake_items_db = [
  {"item_name": "Foo"},
  {"item_name": "Bar"},
  {"item_name": "Baz"}
]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
  return fake_items_db[skip : skip + limit]

# URL example in this case
# http://127.0.0.1:8000/items/?skip=0&limit=10
# http://127.0.0.1:8000/items/?skip=1

##

### Optional query parameters
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
  if q:
    return {"item_id": item_id, "q": q}
  return {"item_id": item_id}

##

### Query parameter type conversion
# In case of boolean parameter: short
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# URL examples will result short as true
# http://127.0.0.1:8000/items/foo?short=1
# http://127.0.0.1:8000/items/foo?short=True
# http://127.0.0.1:8000/items/foo?short=true
# http://127.0.0.1:8000/items/foo?short=on
# http://127.0.0.1:8000/items/foo?short=yes
# or any other case variation

##

### Multiple path and query parameters
# path parameters and query parameters detected by name
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

##

### Required query parameters
# Declare with specific type as here in needy
# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item

# URL example:
# http://127.0.0.1:8000/items/foo-item?needy=sooooneedy

# Different query parameters with different definitions
# needy: required; skip: default to 0; limit: optional
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# URL example:
# http://127.0.0.1:8000/items/3?needy=sooooneedy

# It's also possible to use Enum in the query parameter the same way as path parameter

##

### 