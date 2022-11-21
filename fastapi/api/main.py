from fastapi import FastAPI
from database import engine
import models
from routers import products, orders, users, validation


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Center HUB")

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(users.router)
app.include_router(validation.router)


