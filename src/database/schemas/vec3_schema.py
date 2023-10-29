from typing import Optional

from pydantic import BaseModel


class Vec3(BaseModel):
    x: Optional[float] = 0
    y: Optional[float] = 0
    z: Optional[float] = 0
