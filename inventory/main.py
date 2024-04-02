from typing import Union
from redis_om import HashModel
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

redisdb = redis.Redis(
  host='redis-17556.c323.us-east-1-2.ec2.cloud.redislabs.com',
  port=17556,
  password='uJ9FSfJeDEWKW4Ljl9uAd2hzyGBgW9yS',
  decode_responses = True)




class Product(HashModel):
    name: str
    price: float
    quantity: int #quantity avaliable

    class Meta:
        database = redisdb



@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        "id" : product.pk,
        "name" : product.name,
        "price" : product.price,
        "quantity" : product.quantity
    }


@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk : str):
    return Product.get(pk)
 

@app.delete('/products/{pk}')
def delete(pk : str):
    if (Product.delete(pk) == 1):
        return "Deleted Sucessfully"
    else:
        return 500
