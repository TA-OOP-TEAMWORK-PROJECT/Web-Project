import uvicorn
from fastapi import FastAPI
from routers.messages_router import message_router
from routers.auth_router import auth_router
from routers.topic_router import topic_router
from routers.reply_router import reply_router

app = FastAPI()
app.include_router(topic_router)
app.include_router(reply_router)
app.include_router(auth_router)
app.include_router(message_router)




if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8001)


