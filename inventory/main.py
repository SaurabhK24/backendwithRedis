from typing import Union
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

redis = get_redis_connection(host = "redis-17556.c323.us-east-1-2.ec2.cloud.redislabs.com:17556", 
                             port = 11844,
                             password = "uJ9FSfJeDEWKW4Ljl9uAd2hzyGBgW9yS",
                             decode_responses = True)



class Product(HashModel):
    name: str
    price: float
    quantity: int #quantity avaliable

    class Meta:
        database = redis

@app.get('/products')
def all():
    return Product.all_pks()

