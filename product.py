from dataclasses import dataclass
from datetime import datetime




@dataclass
class Product:
    name: str
    order_time : datetime
    status: str
    price: float

