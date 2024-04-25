from fastapi import FastAPI
from routers.messages_router import message_router
from routers.users_router import users_router


app = FastAPI()

# app.include_router(categories_router)

app.include_router(users_router)
app.include_router(message_router)
