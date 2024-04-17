from pydantic import BaseModel

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    is_available: bool = True
