# Adaptive Deadline-Aware Task Sorting (ADATS)

## Algorithms Final Project

**Author:** Renz Ryan Santillana  
**Course:** CS460 – Algorithms

---

# Project Overview

Adaptive Deadline-Aware Task Sorting (ADATS) is an intelligent scheduling algorithm designed to help college students manage their academic workload.

Instead of manually organizing assignments, ADATS allows students to upload their course syllabus for each class. The algorithm analyzes the syllabus, extracts assignments, quizzes, projects, and exams, estimates their difficulty, and creates a recommended study schedule using a **Priority Queue (Heap)**.

ADATS also reserves study time before quizzes and exams and estimates the student's chance of earning an **A** based on current coursework and study progress.

# Features

- Upload one syllabus for each class (.PDF or .TXT)
- Automatically detect:
  - Homework
  - Assignments
  - Projects
  - Quizzes
  - Midterms
  - Final Exams
- Estimate assignment difficulty
- Calculate task priority
- Schedule homework and study sessions
- Predict current letter grades (A–F)
- Estimate probability of earning an A
- Works with any number of college classes

---

# Algorithm

ADATS uses a **Priority Queue (Heap)** to determine which task should be completed first.

Priority is calculated using:

```
Priority Score =
Urgency +
Difficulty +
Estimated Hours +
Study Bonus
```

Where:

```
Urgency = 10 / Days Until Due
```

Additional priority is given to quiz and exam study sessions.

# Time Complexity

| Operation | Complexity |
|-----------|------------|
| Insert Task | O(log n) |
| Remove Highest Priority | O(log n) |
| Schedule All Tasks | O(n log n) |

Space Complexity:

```
O(n)
```

---

# Project Structure

```
ADATS/
│
├── adats_main.py
├── README.md
├── requirements.txt
├── tests/
│   └── test_adats.py
├── sample_syllabus/
│   ├── CS460_Syllabus.pdf
│   └── Math_Syllabus.pdf
└── docs/
```

# Requirements

- Python 3.10 or newer

Install the required package for PDF support:

```bash
pip install PyPDF2
```

(Optional)

```bash
pip install pytest
```

# Build Instructions

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ADATS.git
```

Go to the project folder:

```bash
cd ADATS
```

(Optional) Create a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

# Run Instructions

Start the program:

```bash
python adats_main.py
```

The program displays:

```
Adaptive Deadline-Aware Task Sorting (ADATS)

1. Run demo syllabus
2. Upload my syllabus files
```

Choose:

```
2
```

Then enter:

```
How many classes are you taking?

5
```

Example:

```
Computer Science
Math
English
Computer Architecture
Algorithm
```

For each class, provide the syllabus file location:

```
C:\Users\YourName\Documents\Syllabi\CS460.pdf
```

ADATS will:

- Read the syllabus
- Find assignments
- Estimate difficulty
- Detect quizzes and exams
- Calculate priorities
- Generate a recommended schedule

# Example Output

```
ADATS Recommended Schedule

1. Programming Project
2. Study for Midterm
3. Homework 4
4. Quiz Review
5. Essay Draft
```

# Running Tests

Run the automated tests:

```bash
pytest
```

or

```bash
python -m pytest
```

# Test Cases

The project includes tests for:

- Priority calculation
- Assignment extraction
- Quiz detection
- Exam detection
- Difficulty estimation
- Schedule ordering

# Current Limitations

- PDF parsing depends on the formatting of the syllabus.
- Some scanned PDFs may require OCR before text can be extracted.
- Due dates are detected only when written in supported date formats.

---

# Future Improvements

- Canvas integration
- Google Calendar synchronization
- Automatic OCR for scanned PDFs
- AI-powered syllabus understanding
- Mobile application
- Notifications and reminders
- Improved grade prediction using real assignment scores

# Version

Final Submission Tag

```
v1.0-final
```

Create the tag:

```bash
git tag v1.0-final
git push origin v1.0-final
```
