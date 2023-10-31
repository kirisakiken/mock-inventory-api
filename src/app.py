from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import store_routes, cabinet_routes, row_routes, sku_routes, brand_routes, lane_routes, query_routes

origins = [
    "http://localhost:7245",
    "https://localhost:7245",
]

app = FastAPI()
# Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routes
app.include_router(query_routes.router)
app.include_router(brand_routes.router)
app.include_router(store_routes.router)
app.include_router(cabinet_routes.router)
app.include_router(row_routes.router)
app.include_router(sku_routes.router)
app.include_router(lane_routes.router)
