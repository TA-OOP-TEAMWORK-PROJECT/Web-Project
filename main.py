from fastapi import FastAPI
from routers.users import users_router
from routers.category import category_router
app = FastAPI()

app.include_router(users_router)
app.include_router(category_router)

