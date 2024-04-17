from fastapi import FastAPI, HTTPException, status
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from datetime import datetime

app = FastAPI()

# In-memory database
patients = []
doctors = []
appointments = []

@app.get("/")
def read_root():
    return {"message": "Hello, welcome to the API!"}


# CRUD endpoints for Patients
@app.post("/patients/", status_code=status.HTTP_201_CREATED)
def create_patient(patient: Patient):
    patients.append(patient)
    return patient

@app.get("/patients/")
def get_patients():
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, updated_patient: Patient):
    for index, patient in enumerate(patients):
        if patient.id == patient_id:
            patients[index] = updated_patient
            return updated_patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int):
    for index, patient in enumerate(patients):
        if patient.id == patient_id:
            del patients[index]
            return
    raise HTTPException(status_code=404, detail="Patient not found")

# CRUD endpoints for Doctors
@app.post("/doctors/", status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: Doctor):
    doctors.append(doctor)
    return doctor

@app.get("/doctors/")
def get_doctors():
    return doctors

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for doctor in doctors:
        if doctor.id == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, updated_doctor: Doctor):
    for index, doctor in enumerate(doctors):
        if doctor.id == doctor_id:
            doctors[index] = updated_doctor
            return updated_doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int):
    for index, doctor in enumerate(doctors):
        if doctor.id == doctor_id:
            del doctors[index]
            return
    raise HTTPException(status_code=404, detail="Doctor not found")

# Endpoints for Appointments
@app.post("/appointments/", status_code=status.HTTP_201_CREATED)
def create_appointment(patient_id: int, date: datetime):
    # To check if patient exists
    patient = next((p for p in patients if p.id == patient_id), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #To find the first available doctor
    available_doctor = next((doc for doc in doctors if doc.is_available), None)
    if not available_doctor:
        raise HTTPException(status_code=400, detail="No available doctors")

    # Create appointment
    new_appointment = Appointment(
        id=len(appointments) + 1,
        patient=patient,
        doctor=available_doctor,
        date=date
    )
    appointments.append(new_appointment)
    # Update doctor's availability
    available_doctor.is_available = False
    return new_appointment

@app.post("/appointments/{appointment_id}/complete", status_code=status.HTTP_200_OK)
def complete_appointment(appointment_id: int):
    appointment = next((app for app in appointments if app.id == appointment_id), None)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Complete appointment and make doctor available again
    appointment.doctor.is_available = True
    appointments.remove(appointment)
    return {"message": "Appointment completed"}

@app.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_appointment(appointment_id: int):
    appointment = next((app for app in appointments if app.id == appointment_id), None)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Cancel appointment and make doctor available again
    appointment.doctor.is_available = True
    appointments.remove(appointment)
    return

# Endpoint for setting doctor availability status
@app.patch("/doctors/{doctor_id}/availability")
def set_doctor_availability(doctor_id: int, is_available: bool):
    doctor = next((doc for doc in doctors if doc.id == doctor_id), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    doctor.is_available = is_available
    return doctor
