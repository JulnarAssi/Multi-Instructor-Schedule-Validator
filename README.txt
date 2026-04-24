Multi-Instructor Schedule Validator 

A Python-based system that parses, validates, and analyzes teaching schedules for multiple instructors according to university policies and constraints.

---

Features

	>> Parse multiple input files (schedule, preferences, valid codes)
	>> Object-Oriented design with modular structure
	>> Teaching load calculation (lectures & office hours)
	>> Validation rules:

  > Teaching load (12–18 hours)
  > Office hours ≥ 50% of teaching load
  > Minimum teaching days distribution
  > Time conflict detection
  > Consecutive teaching rule
  > Course code validation
  > Instructor preference validation
  > Allowed teaching day groups (SMW / TTh)
  > Lab repetition rule

Detailed per-instructor validation reports

---

System Design

	>> Parser Module    → Reads and structures input data
	>> Processor Module → Applies validation rules
	>> Instructor Model → Stores schedule & preferences

---

Technologies Used

> Python
> Object-Oriented Programming (OOP)
> File Handling
> Data Structures (Lists, Dictionaries, Sets)

---

Project Structure


multi-instructor-schedule-validator/
│
├── src/
├── data/
├── docs/
└── README.md


---

How to Run

1. Make sure the following files exist in the same directory:

   > ValidCodes.txt
   > Preferences.txt
   > Schedule.txt

2. Run the program:


python3 main.py


---

Input Files

	>> ValidCodes.txt  → list of valid courses
	>> Preferences.txt → instructor preferences
	>> Schedule.txt    → weekly schedules

---

Output

> Per-instructor validation results
> Detailed error messages for invalid schedules
> Final VALID / INVALID status

---

Author

	> Julnar Nall Assi

	> MOHAMMED KHALIL INJASS

---

Notes

This project demonstrates strong skills in:

> Parsing structured data
> Constraint validation
> Algorithmic problem solving
> Clean modular programming

---

Future Improvements

> Add GUI visualization
> Export reports to files
> Improve error reporting format
