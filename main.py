import json
import os

class Student:
    def __init__(self, roll_no, name, branch, attendance_pct):
        self.roll_no = roll_no
        self.name = name
        self.branch = branch
        self.attendance_pct = attendance_pct

    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "branch": self.branch,
            "attendance_pct": self.attendance_pct
        }

class ManagementSystem:
    def __init__(self, filename="students_data.json"):
        self.filename = filename
        self.students = {}
        self.load_data()

    def add_student(self, roll_no, name, branch, attendance_pct):
        if roll_no in self.students:
            print("\n❌ This Roll Number already exists!")
            return
        
        student = Student(roll_no, name, branch, attendance_pct)
        self.students[roll_no] = student
        self.save_data()
        print(f"\n✅ Student '{name}' added successfully.")

    def display_all(self):
        if not self.students:
            print("\nℹ️ No records found.")
            return

        print("\n" + "="*60)
        print(f"{'Roll No':<10} | {'Name':<20} | {'Branch':<10} | {'Attendance (%)':<15}")
        print("="*60)
        for s in self.students.values():
            status = f"{s.attendance_pct}%"
            if s.attendance_pct < 75:
                status += " ⚠️ (Low)"
            print(f"{s.roll_no:<10} | {s.name:<20} | {s.branch:<10} | {status:<15}")
        print("="*60)

    def search_student(self, roll_no):
        student = self.students.get(roll_no)
        if student:
            print(f"\n🔍 Student Details Found:")
            print(f"Roll No: {student.roll_no}\nName: {student.name}\nBranch: {student.branch}\nAttendance: {student.attendance_pct}%")
        else:
            print("\n❌ Student not found.")

    def save_data(self):
        data = {roll: student.to_dict() for roll, student in self.students.items()}
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for roll, info in data.items():
                    self.students[roll] = Student(info['roll_no'], info['name'], info['branch'], info['attendance_pct'])

def main():
    system = ManagementSystem()

    while True:
        print("\n--- 🎓 STUDENT MANAGEMENT SYSTEM ---")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            roll = input("Enter Roll No: ")
            name = input("Enter Name: ")
            branch = input("Enter Branch: ")
            try:
                att = float(input("Enter Attendance Percentage: "))
                system.add_student(roll, name, branch, att)
            except ValueError:
                print("❌ Please enter a valid number for attendance.")
        
        elif choice == '2':
            system.display_all()
        
        elif choice == '3':
            roll = input("Enter Roll No to search: ")
            system.search_student(roll)
            
        elif choice == '4':
            print("\nThank you! Exiting program.")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()