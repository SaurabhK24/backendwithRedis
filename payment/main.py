from typing import Union
from redis_om import HashModel
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests, time
from fastapi.background import BackgroundTasks


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)


# Ideally should be different db for different service (using same to avoid charges for now)
redisdb = redis.Redis(
  host='redis-17556.c323.us-east-1-2.ec2.cloud.redislabs.com',
  port=17556,
  password='uJ9FSfJeDEWKW4Ljl9uAd2hzyGBgW9yS',
  decode_responses = True)

class Order(HashModel):
    product_id : str
    price : float
    fee : float
    total : float # fees + price
    quantity : int 
    status : str #pending/completed/refunded

    class Meta:
        database : redisdb



@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')







