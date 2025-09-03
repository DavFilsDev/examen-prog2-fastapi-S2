from fastapi import FastAPI
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