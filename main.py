import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
from database import Database
import os

class AttendanceSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize database
        self.db = Database()
        
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create main container
        self.create_main_page()
        
    def create_main_page(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create main frame with modern styling
        main_frame = ttk.Frame(self.root, padding="20", style="Main.TFrame")
        main_frame.pack(expand=True, fill="both")
        
        # Configure styles
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Title.TLabel", font=("Helvetica", 28, "bold"), background="#f0f0f0")
        style.configure("Button.TButton", font=("Helvetica", 12), padding=10)
        
        # Title with modern styling
        title = ttk.Label(main_frame, text="Face Recognition\nAttendance System", 
                         style="Title.TLabel", justify="center")
        title.pack(pady=40)
        
        # Buttons with modern styling
        button_frame = ttk.Frame(main_frame, style="Main.TFrame")
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.create_login_page, 
                  style="Button.TButton", width=25).pack(pady=10)
        ttk.Button(button_frame, text="Register", command=self.create_register_page, 
                  style="Button.TButton", width=25).pack(pady=10)
        
    def create_register_page(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create register frame with modern styling
        register_frame = ttk.Frame(self.root, padding="30", style="Main.TFrame")
        register_frame.pack(expand=True, fill="both")
        
        # Title
        ttk.Label(register_frame, text="Register New User", 
                 style="Title.TLabel").pack(pady=20)
        
        # Create form frame
        form_frame = ttk.Frame(register_frame, style="Main.TFrame")
        form_frame.pack(pady=20)
        
        # Entry fields with modern styling
        self.name_var = tk.StringVar()
        self.enrollment_var = tk.StringVar()
        self.college_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.section_var = tk.StringVar()
        
        # Configure entry style
        style = ttk.Style()
        style.configure("Entry.TEntry", padding=5)
        
        # Create form fields
        fields = [
            ("Name:", self.name_var),
            ("Enrollment Number:", self.enrollment_var),
            ("College:", self.college_var),
            ("Class:", self.class_var),
            ("Section:", self.section_var)
        ]
        
        for label_text, var in fields:
            field_frame = ttk.Frame(form_frame, style="Main.TFrame")
            field_frame.pack(pady=5, fill="x")
            ttk.Label(field_frame, text=label_text, 
                     style="Main.TLabel").pack(side="left", padx=5)
            ttk.Entry(field_frame, textvariable=var, 
                     style="Entry.TEntry", width=30).pack(side="right", padx=5)
        
        # Face capture section
        face_frame = ttk.Frame(register_frame, style="Main.TFrame")
        face_frame.pack(pady=20)
        
        self.face_label = ttk.Label(face_frame)
        self.face_label.pack(pady=10)
        
        # Buttons with modern styling
        button_frame = ttk.Frame(register_frame, style="Main.TFrame")
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Capture Face", command=self.capture_face,
                  style="Button.TButton", width=20).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Register", command=self.register,
                  style="Button.TButton", width=20).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Back", command=self.create_main_page,
                  style="Button.TButton", width=20).pack(side="left", padx=10)

    def capture_face(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                if len(faces) > 0:
                    face = gray[y:y+h, x:x+w]
                    self.face_template = cv2.resize(face, (100, 100))
                    
                    img = Image.fromarray(self.face_template)
                    img = img.resize((200, 200))
                    photo = ImageTk.PhotoImage(img)
                    self.face_label.configure(image=photo)
                    self.face_label.image = photo
                    
            cv2.imshow('Capture Face', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
    
    def register(self):
        if not all([
            self.name_var.get(),
            self.enrollment_var.get(),
            self.college_var.get(),
            self.class_var.get(),
            self.section_var.get(),
            hasattr(self, 'face_template')
        ]):
            messagebox.showerror("Error", "Please fill all fields and capture a face")
            return
            
        face_template = cv2.imencode('.jpg', self.face_template)[1].tobytes()
        
        if self.db.register_user(
            self.name_var.get(),
            self.enrollment_var.get(),
            self.college_var.get(),
            self.class_var.get(),
            self.section_var.get(),
            face_template
        ):
            messagebox.showinfo("Success", "Registration successful!")
            self.create_main_page()
        else:
            messagebox.showerror("Error", "Registration failed. Enrollment number might already exist.")
    
    def create_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        login_frame = ttk.Frame(self.root, padding="30", style="Main.TFrame")
        login_frame.pack(expand=True, fill="both")
        
        ttk.Label(login_frame, text="Login", 
                 style="Title.TLabel").pack(pady=30)
        
        # Create form frame
        form_frame = ttk.Frame(login_frame, style="Main.TFrame")
        form_frame.pack(pady=20)
        
        self.login_name_var = tk.StringVar()
        self.login_enrollment_var = tk.StringVar()
        
        # Login fields
        fields = [
            ("Name:", self.login_name_var),
            ("Enrollment Number:", self.login_enrollment_var)
        ]
        
        for label_text, var in fields:
            field_frame = ttk.Frame(form_frame, style="Main.TFrame")
            field_frame.pack(pady=10, fill="x")
            ttk.Label(field_frame, text=label_text, 
                     style="Main.TLabel").pack(side="left", padx=5)
            ttk.Entry(field_frame, textvariable=var, 
                     style="Entry.TEntry", width=30).pack(side="right", padx=5)
        
        # Buttons
        button_frame = ttk.Frame(login_frame, style="Main.TFrame")
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.login,
                  style="Button.TButton", width=20).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Back", command=self.create_main_page,
                  style="Button.TButton", width=20).pack(side="left", padx=10)
    
    def login(self):
        result = self.db.verify_login(self.login_name_var.get(), self.login_enrollment_var.get())
        if result:
            self.user_id = result[0]
            face_array = np.frombuffer(result[1], dtype=np.uint8)
            self.stored_template = cv2.imdecode(face_array, cv2.IMREAD_GRAYSCALE)
            self.stored_template = cv2.resize(self.stored_template, (100, 100))
            self.create_options_page()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def create_options_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        options_frame = ttk.Frame(self.root, padding="30", style="Main.TFrame")
        options_frame.pack(expand=True, fill="both")
        
        user_info = self.db.get_user_info(self.user_id)
        ttk.Label(options_frame, text=f"Welcome, {user_info[0]}", 
                 style="Title.TLabel").pack(pady=30)
        
        # Buttons with modern styling
        button_frame = ttk.Frame(options_frame, style="Main.TFrame")
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Take Attendance", command=self.take_attendance,
                  style="Button.TButton", width=25).pack(pady=10)
        ttk.Button(button_frame, text="View Attendance", command=self.view_attendance,
                  style="Button.TButton", width=25).pack(pady=10)
        ttk.Button(button_frame, text="Logout", command=self.create_main_page,
                  style="Button.TButton", width=25).pack(pady=10)
    
    def take_attendance(self):
        # Create a new window for attendance
        attendance_window = tk.Toplevel(self.root)
        attendance_window.title("Take Attendance")
        attendance_window.geometry("800x700")
        
        # Create frame for video feed
        video_frame = ttk.Frame(attendance_window)
        video_frame.pack(pady=20)
        
        # Create label for video feed
        self.video_label = ttk.Label(video_frame)
        self.video_label.pack()
        
        # Create frame for captured face
        captured_frame = ttk.Frame(attendance_window)
        captured_frame.pack(pady=10)
        
        # Create label for captured face preview
        self.captured_face_label = ttk.Label(captured_frame)
        self.captured_face_label.pack()
        
        # Create status label
        self.status_label = ttk.Label(attendance_window, text="Position your face in the frame", 
                                    font=("Helvetica", 12))
        self.status_label.pack(pady=10)
        
        # Create buttons frame
        button_frame = ttk.Frame(attendance_window)
        button_frame.pack(pady=20)
        
        # Create Show button
        ttk.Button(button_frame, text="Show", 
                  command=lambda: self.capture_and_mark_attendance(attendance_window),
                  style="Button.TButton", width=20).pack(side="left", padx=10)
        
        ttk.Button(button_frame, text="Close", 
                  command=attendance_window.destroy,
                  style="Button.TButton", width=20).pack(side="left", padx=10)
        
        # Start video capture
        self.cap = cv2.VideoCapture(0)
        self.update_video_feed()
        
        # Store window reference
        self.attendance_window = attendance_window
    
    def update_video_feed(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Draw rectangle around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Convert frame to PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((640, 480))
            photo = ImageTk.PhotoImage(image=img)
            
            # Update video label
            self.video_label.configure(image=photo)
            self.video_label.image = photo
            
            # Schedule next update
            self.video_label.after(10, self.update_video_feed)
    
    def capture_and_mark_attendance(self, window):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (100, 100))
                
                # Compare with stored template
                diff = cv2.absdiff(face, self.stored_template)
                if np.mean(diff) < 50:  # Threshold for similarity
                    # Show captured face in the label
                    img = Image.fromarray(face)
                    img = img.resize((200, 200))
                    photo = ImageTk.PhotoImage(img)
                    self.captured_face_label.configure(image=photo)
                    self.captured_face_label.image = photo
                    
                    # Get user info and mark attendance
                    user_info = self.db.get_user_info(self.user_id)
                    if user_info:
                        name, enrollment = user_info[0], user_info[1]
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Update attendance in database
                        success, message = self.db.mark_attendance(self.user_id, current_time)
                        if success:
                            self.status_label.config(text="Attendance marked successfully!")
                            messagebox.showinfo("Success", 
                                              f"Attendance marked successfully!\n\n"
                                              f"Name: {name}\n"
                                              f"Enrollment: {enrollment}\n"
                                              f"Time: {current_time}")
                            window.destroy()
                            self.cap.release()
                            self.view_attendance()  # Show updated attendance immediately
                        else:
                            messagebox.showwarning("Warning", message)
                else:
                    messagebox.showerror("Error", "Face not recognized. Please try again.")
            else:
                messagebox.showerror("Error", "No face detected. Please try again.")
    
    def view_attendance(self):
        records = self.db.get_attendance(self.user_id)
        
        attendance_window = tk.Toplevel(self.root)
        attendance_window.title("Attendance Records")
        attendance_window.geometry("1200x600")
        
        # Configure style for treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        
        # Create main frame
        main_frame = ttk.Frame(attendance_window, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Create header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="Your Attendance History", 
                 font=("Helvetica", 16, "bold")).pack(side="left")
        
        # Create treeview with scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        
        tree = ttk.Treeview(tree_frame, 
                           columns=("Name", "Enrollment", "College", "Class", "Section", "Date", "Time", "Status"),
                           show="headings")
        
        # Configure columns
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Pack widgets
        tree.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        
        # Add records to treeview
        for record in records:
            tree.insert("", "end", values=record)
        
        # Add summary frame
        summary_frame = ttk.Frame(main_frame)
        summary_frame.pack(fill="x", pady=(10, 0))
        
        # Calculate attendance statistics
        total_days = len(records)
        present_days = sum(1 for record in records if record[7] == "Present")
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        # Display statistics
        ttk.Label(summary_frame, 
                 text=f"Total Days: {total_days} | Present Days: {present_days} | Attendance: {attendance_percentage:.1f}%",
                 font=("Helvetica", 10)).pack(side="left")
        
        # Add close button
        ttk.Button(summary_frame, text="Close", 
                  command=attendance_window.destroy,
                  style="Button.TButton").pack(side="right")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AttendanceSystem()
    app.run()
