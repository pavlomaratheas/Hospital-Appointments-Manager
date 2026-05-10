import json
from datetime import datetime


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):
        return f"Name: {self.name}, Age: {self.age}"


class Doctor(Person):
    def __init__(self, name, age, speciality, doctor_id):
        super().__init__(name, age)
        self.speciality = speciality
        self.doctor_id = doctor_id

    def show_info(self):
        return (
            f"Doctor ID: {self.doctor_id} | Name: {self.name} | "
            f"Age: {self.age} | Speciality: {self.speciality}"
        )


class Patient(Person):
    def __init__(self, name, age, patient_id, illness):
        super().__init__(name, age)
        self.patient_id = patient_id
        self.illness = illness

    def show_info(self):
        return (
            f"Patient ID: {self.patient_id} | Name: {self.name} | "
            f"Age: {self.age} | Illness: {self.illness}"
        )


class Appointment:
    def __init__(self, date, status, doctor_id, patient_id):
        self.date = date
        self.status = status
        self.doctor_id = doctor_id
        self.patient_id = patient_id

    def show_info(self):
        return (
            f"Date: {self.date} | Doctor: {self.doctor_id} | "
            f"Patient: {self.patient_id} | Status: {self.status}"
        )

    def cancel_appointment(self):
        self.status = "cancelled"
        return f"Appointment on {self.date} cancelled"


class HospitalManager:
    VALID_STATUSES = ["active", "completed", "cancelled"]

    def __init__(self):
        self.doctors = {}
        self.patients = {}
        self.appointments = []

    def validate_datetime(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    def add_doctor(self, name, age, speciality, doctor_id):
        if not name or not speciality or not doctor_id:
            return "Please fill all doctor fields"
        if doctor_id in self.doctors:
            return f"Doctor {doctor_id} already exists"
        self.doctors[doctor_id] = Doctor(name, age, speciality, doctor_id)
        return f"Doctor {doctor_id} added"

    def add_patient(self, name, age, patient_id, illness):
        if not name or not patient_id or not illness:
            return "Please fill all patient fields"
        if patient_id in self.patients:
            return f"Patient {patient_id} already exists"
        self.patients[patient_id] = Patient(name, age, patient_id, illness)
        return f"Patient {patient_id} added"

    def add_appointment(self, date, status, doctor_id, patient_id):
        if not date or not status or not doctor_id or not patient_id:
            return "Please fill all appointment fields"
        if not self.validate_datetime(date):
            return "Invalid date format. Use YYYY-MM-DD HH:MM"
        if status not in self.VALID_STATUSES:
            return "Invalid status"
        if doctor_id not in self.doctors:
            return "Doctor not found"
        if patient_id not in self.patients:
            return "Patient not found"

        for appointment in self.appointments:
            if (
                appointment.date == date
                and appointment.doctor_id == doctor_id
                and appointment.patient_id == patient_id
            ):
                return "Appointment already exists"

        appointment = Appointment(date, status, doctor_id, patient_id)
        self.appointments.append(appointment)
        self.appointments.sort(key=lambda x: x.date)
        return f"Appointment created for {date}"

    def cancel_appointment(self, doctor_id, patient_id, date):
        for appointment in self.appointments:
            if (
                appointment.doctor_id == doctor_id
                and appointment.patient_id == patient_id
                and appointment.date == date
            ):
                return appointment.cancel_appointment()
        return "Appointment not found"

    def search_appointments(self, doctor_id="", patient_id="", status="all"):
        results = []

        for appointment in self.appointments:
            if doctor_id and appointment.doctor_id != doctor_id:
                continue
            if patient_id and appointment.patient_id != patient_id:
                continue
            if status != "all" and appointment.status != status:
                continue
            results.append(appointment)

        if not results:
            return "No matching appointments found"

        lines = ["=== FILTERED APPOINTMENTS ==="]
        for appointment in results:
            lines.append(appointment.show_info())
        lines.append(f"Matches: {len(results)}")
        return "\n".join(lines)

    def list_all_doctors(self):
        if not self.doctors:
            return "No doctors registered"
        lines = ["=== ALL DOCTORS ==="]
        for doctor in self.doctors.values():
            lines.append(doctor.show_info())
        lines.append(f"Total doctors: {len(self.doctors)}")
        return "\n".join(lines)

    def list_all_patients(self):
        if not self.patients:
            return "No patients registered"
        lines = ["=== ALL PATIENTS ==="]
        for patient in self.patients.values():
            lines.append(patient.show_info())
        lines.append(f"Total patients: {len(self.patients)}")
        return "\n".join(lines)

    def list_all_appointments(self):
        if not self.appointments:
            return "No appointments"
        lines = ["=== ALL APPOINTMENTS ==="]
        for appointment in self.appointments:
            lines.append(appointment.show_info())
        lines.append(f"Total appointments: {len(self.appointments)}")
        return "\n".join(lines)

    def get_metrics(self):
        total_doctors = len(self.doctors)
        total_patients = len(self.patients)
        total_appointments = len(self.appointments)
        active_appointments = sum(1 for a in self.appointments if a.status == "active")

        return {
            "doctors": total_doctors,
            "patients": total_patients,
            "appointments": total_appointments,
            "active": active_appointments
        }

    def save_to_json(self, filename="hospital_data.json"):
        data = {
            "doctors": [],
            "patients": [],
            "appointments": []
        }

        for doctor in self.doctors.values():
            data["doctors"].append({
                "name": doctor.name,
                "age": doctor.age,
                "speciality": doctor.speciality,
                "doctor_id": doctor.doctor_id
            })

        for patient in self.patients.values():
            data["patients"].append({
                "name": patient.name,
                "age": patient.age,
                "patient_id": patient.patient_id,
                "illness": patient.illness
            })

        for appointment in self.appointments:
            data["appointments"].append({
                "date": appointment.date,
                "status": appointment.status,
                "doctor_id": appointment.doctor_id,
                "patient_id": appointment.patient_id
            })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return f"Data saved to {filename}"

    def load_from_json(self, filename="hospital_data.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return f"{filename} not found"

        self.doctors = {}
        self.patients = {}
        self.appointments = []

        for doctor_data in data.get("doctors", []):
            doctor = Doctor(
                doctor_data["name"],
                doctor_data["age"],
                doctor_data["speciality"],
                doctor_data["doctor_id"]
            )
            self.doctors[doctor.doctor_id] = doctor

        for patient_data in data.get("patients", []):
            patient = Patient(
                patient_data["name"],
                patient_data["age"],
                patient_data["patient_id"],
                patient_data["illness"]
            )
            self.patients[patient.patient_id] = patient

        for appointment_data in data.get("appointments", []):
            appointment = Appointment(
                appointment_data["date"],
                appointment_data["status"],
                appointment_data["doctor_id"],
                appointment_data["patient_id"]
            )
            self.appointments.append(appointment)

        self.appointments.sort(key=lambda x: x.date)
        return f"Data loaded from {filename}"