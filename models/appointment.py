from pydantic import BaseModel
from datetime import datetime
from models.patient import Patient
from models.doctor import Doctor

class Appointment(BaseModel):
    id: int
    patient: Patient
    doctor: Doctor
    date: datetime
