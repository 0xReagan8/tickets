from fastapi import FastAPI
from fastapi.responses import FileResponse

from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    item_id: int

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
