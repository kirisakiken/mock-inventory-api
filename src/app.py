from fastapi import FastAPI

from src.routes import hello_route

app = FastAPI()
# Routes
app.include_router(hello_route.router)