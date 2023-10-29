from fastapi import FastAPI

from src.routes import store_routes, cabinet_routes, row_routes

app = FastAPI()
# Routes
app.include_router(store_routes.router)
app.include_router(cabinet_routes.router)
app.include_router(row_routes.router)
