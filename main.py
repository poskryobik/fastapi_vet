from enum import Enum
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return 'get function'


@app.post('/post')
def get_post() -> Timestamp:
    new_id = post_db[-1].id + 1
    new_timestamp = Timestamp(id=new_id, timestamp=int(datetime.now().timestamp()))
    post_db.append(new_timestamp)
    return new_timestamp


@app.get('/dog')
def get_dogs(kind: DogType) -> List[Dog]:
    return_for_dogs = []
    for _, dog_info in dogs_db.items():
        if dog_info.kind == kind:
            return_for_dogs.append(dog_info)
    return return_for_dogs


@app.post('/dog')
def create_dog(dog: Dog) -> Dog:
    if dog.pk in dogs_db.keys():
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')
    dogs_db[dog.pk] = dog
    return dog


@app.get('/dog/{pk}')
def get_dogs_by_pk(pk: int) -> Dog:
    for _, dog in dogs_db.items():
        if dog.pk == pk:
            return dog
    else:
        raise HTTPException(status_code=409, 
                            detail='The specified PK not exists.')

@app.patch('/dog/{pk}')
def update_dog(pk: int, dog: Dog) -> Dog:
    if dogs_db.get(pk, None):
        dogs_db[pk] = dog
    else:
        raise HTTPException(status_code=409,
                            detail='The specified PK not exists.')
    return dog