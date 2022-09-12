from fastapi import FastAPI
from redis_om import HashModel,get_redis_connection
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-15599.c293.eu-central-1-1.ec2.cloud.redislabs.com",
    port=15599,
    password="6PdZ4Uh60c962MKsIw16LVhU6oCFagjU",
    decode_responses=True
)


class Food(HashModel):
    name: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Food",
                "description": "Food"
            }
        }

    class Meta:
        database = redis



@app.get('/product')
async def get_product():
    return [format(pk) for pk in Food.all_pks()]

def format(pk:str):
    food = Food.get(pk)
    return {
        'id':food.pk,
        'name':food.name,
        'description': food.description
    }


@app.post('/product')
async def add_new_product(food:Food):
    return food.save()


@app.delete('/product/{pk}')
async def remove_product(pk:str):
    return Food.delete(pk)
    