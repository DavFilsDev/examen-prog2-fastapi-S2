from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
app = FastAPI()

class Characteristic(BaseModel):
    ram_memory: int
    rom_memory: int

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

phones_store: List[Phone] = []

@app.get("/health")
def health():
    return "Ok"

@app.post("/phones", status_code=201)
def create_phones(new_phones: List[Phone]):
    phones_store.extend(new_phones)
    return [phone.model_dump() for phone in phones_store]

@app.get("/phones")
def list_phones():
    return [phone.model_dump() for phone in phones_store]

@app.get("/phones/{id}")
def get_phone(id: str):
    for phone in phones_store:
        if phone.identifier == id:
            return phone.model_dump()
    raise HTTPException(status_code=404, detail=f"Phone with id '{id}' not found")

@app.put("/phones/{id}/characteristics")
def update_characteristics(id: str, new_characteristics: Characteristic):
    for i, phone in enumerate(phones_store):
        if phone.identifier == id:
            updated_phone = phone.copy(update={"characteristics": new_characteristics})
            phones_store[i] = updated_phone
            return updated_phone.model_dump()
    raise HTTPException(status_code=404, detail=f"Phone with id '{id}' not found")