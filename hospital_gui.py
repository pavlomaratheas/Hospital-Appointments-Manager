import customtkinter as ctk
from tkinter import messagebox
from hospital_logic import HospitalManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MetricCard(ctk.CTkFrame):
    def __init__(self, master, title, value="0"):
        super().__init__(master, corner_radius=14)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 14)
        )
        self.title_label.grid(row=0, column=0, padx=15, pady=(12, 4), sticky="w")

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Arial", 26, "bold")
        )
        self.value_label.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")

    def set_value(self, value):
        self.value_label.configure(text=str(value))


class HospitalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.hm = HospitalManager()

        self.title("Hospital Manager Pro")
        self.geometry("1380x860")
        self.minsize(1180, 760)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        self.main = ctk.CTkFrame(self, corner_radius=18)
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.build_sidebar()
        self.build_main()
        self.refresh_dashboard()

    def build_sidebar(self):
        title = ctk.CTkLabel(self.sidebar, text="Hospital Manager", font=("Arial", 24, "bold"))
        title.pack(pady=(30, 10), padx=20)

        subtitle = ctk.CTkLabel(self.sidebar, text="Professional UI", font=("Arial", 14))
        subtitle.pack(pady=(0, 25), padx=20)

        self.mode_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["dark", "light", "system"],
            command=self.change_mode
        )
        self.mode_menu.set("dark")
        self.mode_menu.pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.sidebar, text="Dashboard", command=self.refresh_dashboard).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Show Doctors", command=self.show_doctors).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Show Patients", command=self.show_patients).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Show Appointments", command=self.show_appointments).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Save JSON", command=self.save_json).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Load JSON", command=self.load_json).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Clear Output", command=self.clear_output).pack(pady=10, padx=20, fill="x")

    def build_main(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self.main, corner_radius=14)
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)

        for col in range(4):
            self.scroll_frame.grid_columnconfigure(col, weight=1)

        # Dashboard
        dashboard_title = ctk.CTkLabel(self.scroll_frame, text="Dashboard", font=("Arial", 22, "bold"))
        dashboard_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w", columnspan=4)

        self.card_doctors = MetricCard(self.scroll_frame, "Doctors")
        self.card_doctors.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.card_patients = MetricCard(self.scroll_frame, "Patients")
        self.card_patients.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.card_appointments = MetricCard(self.scroll_frame, "Appointments")
        self.card_appointments.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.card_active = MetricCard(self.scroll_frame, "Active Appointments")
        self.card_active.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        # Add Doctor
        doctor_title = ctk.CTkLabel(self.scroll_frame, text="Add Doctor", font=("Arial", 18, "bold"))
        doctor_title.grid(row=2, column=0, padx=20, pady=(25, 10), sticky="w", columnspan=2)

        self.doc_name = ctk.CTkEntry(self.scroll_frame, placeholder_text="Doctor name")
        self.doc_name.grid(row=3, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        self.doc_age = ctk.CTkEntry(self.scroll_frame, placeholder_text="Doctor age")
        self.doc_age.grid(row=4, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        self.doc_speciality = ctk.CTkEntry(self.scroll_frame, placeholder_text="Speciality")
        self.doc_speciality.grid(row=5, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        self.doc_id = ctk.CTkEntry(self.scroll_frame, placeholder_text="Doctor ID")
        self.doc_id.grid(row=6, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        ctk.CTkButton(self.scroll_frame, text="Add Doctor", command=self.add_doctor).grid(
            row=7, column=0, padx=20, pady=12, sticky="ew", columnspan=2
        )

        # Add Patient
        patient_title = ctk.CTkLabel(self.scroll_frame, text="Add Patient", font=("Arial", 18, "bold"))
        patient_title.grid(row=2, column=2, padx=20, pady=(25, 10), sticky="w", columnspan=2)

        self.pat_name = ctk.CTkEntry(self.scroll_frame, placeholder_text="Patient name")
        self.pat_name.grid(row=3, column=2, padx=20, pady=8, sticky="ew", columnspan=2)

        self.pat_age = ctk.CTkEntry(self.scroll_frame, placeholder_text="Patient age")
        self.pat_age.grid(row=4, column=2, padx=20, pady=8, sticky="ew", columnspan=2)

        self.pat_id = ctk.CTkEntry(self.scroll_frame, placeholder_text="Patient ID")
        self.pat_id.grid(row=5, column=2, padx=20, pady=8, sticky="ew", columnspan=2)

        self.pat_illness = ctk.CTkEntry(self.scroll_frame, placeholder_text="Illness")
        self.pat_illness.grid(row=6, column=2, padx=20, pady=8, sticky="ew", columnspan=2)

        ctk.CTkButton(self.scroll_frame, text="Add Patient", command=self.add_patient).grid(
            row=7, column=2, padx=20, pady=12, sticky="ew", columnspan=2
        )

        # Create Appointment
        app_title = ctk.CTkLabel(self.scroll_frame, text="Create Appointment", font=("Arial", 18, "bold"))
        app_title.grid(row=8, column=0, padx=20, pady=(25, 10), sticky="w", columnspan=2)

        self.app_date = ctk.CTkEntry(self.scroll_frame, placeholder_text="Date (YYYY-MM-DD HH:MM)")
        self.app_date.grid(row=9, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        self.app_status = ctk.CTkComboBox(
            self.scroll_frame,
            values=["active", "completed", "cancelled"]
        )
        self.app_status.grid(row=10, column=0, padx=20, pady=8, sticky="ew", columnspan=2)
        self.app_status.set("active")

        self.app_doc_id = ctk.CTkEntry(self.scroll_frame, placeholder_text="Doctor ID")
        self.app_doc_id.grid(row=11, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        self.app_pat_id = ctk.CTkEntry(self.scroll_frame, placeholder_text="Patient ID")
        self.app_pat_id.grid(row=12, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        ctk.CTkButton(self.scroll_frame, text="Create Appointment", command=self.add_appointment).grid(
            row=13, column=0, padx=20, pady=12, sticky="ew", columnspan=2
        )

        # Search / Filter
        search_title = ctk.CTkLabel(self.scroll_frame, text="Search Appointments", font=("Arial", 18, "bold"))
        search_title.grid(row=8, column=2, padx=20, pady=(25, 10), sticky="w", columnspan=2)

        self.search_doc_id = ctk.CTkEntry(self.scroll_frame, placeholder_text="Filter by Doctor ID")
        self.search_doc_id.grid(row=9, column=2, padx=20, pady=8, sticky="ew", columnspan=2)

        self.search_pat_id = ctk.CTkEntry(self.scroll_frame, placeholder_text="Filter by Patient ID")
        self.search_pat_id.grid(row=10, column=2, padx=20, pady=8, sticky="ew", columnspan=2)

        self.search_status = ctk.CTkComboBox(
            self.scroll_frame,
            values=["all", "active", "completed", "cancelled"]
        )
        self.search_status.grid(row=11, column=2, padx=20, pady=8, sticky="ew", columnspan=2)
        self.search_status.set("all")

        ctk.CTkButton(self.scroll_frame, text="Search", command=self.search_appointments).grid(
            row=12, column=2, padx=20, pady=12, sticky="ew", columnspan=2
        )

        ctk.CTkButton(self.scroll_frame, text="Reset Filters", command=self.reset_filters).grid(
            row=13, column=2, padx=20, pady=0, sticky="ew", columnspan=2
        )

        # Cancel Appointment
        cancel_title = ctk.CTkLabel(self.scroll_frame, text="Cancel Appointment", font=("Arial", 18, "bold"))
        cancel_title.grid(row=14, column=0, padx=20, pady=(25, 10), sticky="w", columnspan=2)

        self.cancel_date = ctk.CTkEntry(self.scroll_frame, placeholder_text="Date (YYYY-MM-DD HH:MM)")
        self.cancel_date.grid(row=15, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        self.cancel_doc_id = ctk.CTkEntry(self.scroll_frame, placeholder_text="Doctor ID")
        self.cancel_doc_id.grid(row=16, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        self.cancel_pat_id = ctk.CTkEntry(self.scroll_frame, placeholder_text="Patient ID")
        self.cancel_pat_id.grid(row=17, column=0, padx=20, pady=8, sticky="ew", columnspan=2)

        ctk.CTkButton(self.scroll_frame, text="Cancel Appointment", command=self.cancel_appointment).grid(
            row=18, column=0, padx=20, pady=12, sticky="ew", columnspan=2
        )

        # Output
        output_title = ctk.CTkLabel(self.scroll_frame, text="Output", font=("Arial", 18, "bold"))
        output_title.grid(row=19, column=0, padx=20, pady=(25, 10), sticky="w", columnspan=4)

        self.output_box = ctk.CTkTextbox(self.scroll_frame, height=260)
        self.output_box.grid(row=20, column=0, columnspan=4, padx=20, pady=(0, 20), sticky="nsew")

    def change_mode(self, choice):
        ctk.set_appearance_mode(choice)

    def write_output(self, text):
        self.output_box.delete("0.0", "end")
        self.output_box.insert("0.0", text)

    def clear_output(self):
        self.output_box.delete("0.0", "end")

    def refresh_dashboard(self):
        metrics = self.hm.get_metrics()
        self.card_doctors.set_value(metrics["doctors"])
        self.card_patients.set_value(metrics["patients"])
        self.card_appointments.set_value(metrics["appointments"])
        self.card_active.set_value(metrics["active"])
        self.write_output("Dashboard refreshed")

    def add_doctor(self):
        try:
            age = int(self.doc_age.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Doctor age must be a number")
            return

        result = self.hm.add_doctor(
            self.doc_name.get().strip(),
            age,
            self.doc_speciality.get().strip(),
            self.doc_id.get().strip()
        )
        messagebox.showinfo("Doctor", result)
        self.refresh_dashboard()
        self.show_doctors()

    def add_patient(self):
        try:
            age = int(self.pat_age.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Patient age must be a number")
            return

        result = self.hm.add_patient(
            self.pat_name.get().strip(),
            age,
            self.pat_id.get().strip(),
            self.pat_illness.get().strip()
        )
        messagebox.showinfo("Patient", result)
        self.refresh_dashboard()
        self.show_patients()

    def add_appointment(self):
        result = self.hm.add_appointment(
            self.app_date.get().strip(),
            self.app_status.get().strip(),
            self.app_doc_id.get().strip(),
            self.app_pat_id.get().strip()
        )
        messagebox.showinfo("Appointment", result)
        self.refresh_dashboard()
        self.show_appointments()

    def cancel_appointment(self):
        result = self.hm.cancel_appointment(
            self.cancel_doc_id.get().strip(),
            self.cancel_pat_id.get().strip(),
            self.cancel_date.get().strip()
        )
        messagebox.showinfo("Cancel Appointment", result)
        self.refresh_dashboard()
        self.show_appointments()

    def search_appointments(self):
        result = self.hm.search_appointments(
            self.search_doc_id.get().strip(),
            self.search_pat_id.get().strip(),
            self.search_status.get().strip()
        )
        self.write_output(result)

    def reset_filters(self):
        self.search_doc_id.delete(0, "end")
        self.search_pat_id.delete(0, "end")
        self.search_status.set("all")
        self.show_appointments()

    def show_doctors(self):
        self.write_output(self.hm.list_all_doctors())

    def show_patients(self):
        self.write_output(self.hm.list_all_patients())

    def show_appointments(self):
        self.write_output(self.hm.list_all_appointments())

    def save_json(self):
        result = self.hm.save_to_json()
        messagebox.showinfo("Save JSON", result)

    def load_json(self):
        result = self.hm.load_from_json()
        messagebox.showinfo("Load JSON", result)
        self.refresh_dashboard()
        self.show_appointments()


if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()