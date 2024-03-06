from fastapi import FastAPI
from fastapi.responses import FileResponse

from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    item_id: int
    item_name: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item/{item_id. item_name}")
async def read_item(item_id: int, item_name: str):
    return {"item_id": item_id, "item_name": "test"}

# curl -i -XGET https://sore-cyan-ostrich-fez.cyclic.app/item/1
# curl -i -XGET https://sore-cyan-ostrich-fez.cyclic.app/items/
# curl -i -XPOST https://sore-cyan-ostrich-fez.cyclic.app/items/ --data '{"item_id":1,"name":"Bob"}' -H 'content-type: application/json'