from fastapi import FastAPI
from mobile.mobile import mobile_router

from auth.auth import auth_router
from renter.renter import renter_router

app = FastAPI()
app.include_router(mobile_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}




# app = FastAPI(title='User', version='1.0.0')

app.include_router(auth_router,prefix='/auth')
app.include_router(renter_router,prefix='/renter')

