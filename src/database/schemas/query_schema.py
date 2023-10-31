from typing import List

from pydantic import BaseModel

from src.database.schemas.brand_schema import Brand
from src.database.schemas.cabinet_schema import Cabinet
from src.database.schemas.lane_schema import Lane
from src.database.schemas.row_schema import Row
from src.database.schemas.sku_schema import Sku
from src.database.schemas.store_schema import Store


class StoreInfo(BaseModel):
    store: Store
    cabinets: List[Cabinet]
    rows: List[Row]
    lanes: List[Lane]


class BrandInfo(BaseModel):
    brand: Brand
    skus: List[Sku]
