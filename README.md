# Hospital Manager

A desktop hospital management application built with **Python** and **CustomTkinter**.

This project helps manage doctors, patients, and appointments through a modern GUI. It includes appointment date validation, search and filtering, dashboard metrics, and JSON save/load support.

## Screenshot

<img width="1367" height="821" alt="Screenshot 2026-05-10 at 12 24 43" src="https://github.com/user-attachments/assets/9dac403b-533f-4043-9a87-516e828b5a98" />
<img width="1374" height="888" alt="Screenshot 2026-05-10 at 12 31 14" src="https://github.com/user-attachments/assets/f8d49c9d-00e0-4877-bbff-2978e2d160fd" />


## Features

- Add doctors with ID, age, and speciality
- Add patients with ID, age, and illness
- Create appointments with validated date and time
- Cancel appointments
- Filter appointments by doctor ID, patient ID, and status
- Dashboard metrics for doctors, patients, appointments, and active appointments
- Save and load data with JSON
- Dark/light/system appearance mode

## Tech Stack

- Python
- CustomTkinter
- JSON
- Object-Oriented Programming (OOP)

## Project Structure

```bash
hospital-manager/
│
├── hospital_logic.py
├── hospital_gui.py
├── hospital_data.json (once you save a .json)
└── README.md
```

## How It Works

- `hospital_logic.py` contains the backend/business logic
- `hospital_gui.py` contains the frontend/GUI
- The GUI sends user input to the logic layer
- The logic layer validates, stores, and retrieves the data

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/pavlomaratheas/hospital-Appointments-Manager.git
cd hospital-manager
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install customtkinter
```

## Run the App

```bash
python3 hospital_gui.py
```

## Date Format

Appointments use this format:

```text
YYYY-MM-DD HH:MM
```

Example:

```text
2026-05-08 14:30
```

## Why I Built This

I built this project to practice:
- Python OOP design
- GUI development with CustomTkinter
- data validation
- JSON persistence
- separation between frontend and backend logic

## Future Improvements

- Edit doctor, patient, and appointment records
- Delete records with confirmation dialog
- Calendar/date picker widget
- CSV export
- Better appointment table layout
- Packaging as a desktop executable
- Unit tests
