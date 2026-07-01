"""
Adaptive Deadline-Aware Task Sorting (ADATS)
Syllabus Upload Version - Fixed File Path Version

This version fixes common upload/path problems on Windows:
- Removes quotation marks around file paths
- Checks if the file exists before opening it
- Supports .txt and .pdf files
- Gives clearer error messages
"""

from dataclasses import dataclass
from datetime import datetime
import heapq
import os
import re


@dataclass
class Task:
    name: str
    class_name: str
    due_date: str
    days_until_due: int
    difficulty: int
    hours_needed: float
    task_type: str


def clean_file_path(file_path: str) -> str:
    """
    Fixes common Windows path input issues.

    Example problem:
    User enters:
    "C:\\Users\\Downloads\\CS460_Course_syllabus.pdf"

    The quotation marks become part of the path and Python cannot find the file.
    This function removes those quotation marks.
    """

    file_path = file_path.strip()
    file_path = file_path.strip('"')
    file_path = file_path.strip("'")
    return file_path


def read_syllabus_file(file_path: str) -> str:
    """
    Reads a syllabus file.

    Supported:
    - .txt
    - .pdf if PyPDF2 is installed
    """

    file_path = clean_file_path(file_path)

    if not os.path.exists(file_path):
        print("\nERROR: File not found.")
        print("Check that the file path is correct.")
        print("Do not include extra quotation marks unless your terminal adds them automatically.")
        print(f"Path received: {file_path}")
        return ""

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    if extension == ".pdf":
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            print("\nERROR: PDF support requires PyPDF2.")
            print("Install it with:")
            print("pip install PyPDF2")
            return ""

        text = ""
        reader = PdfReader(file_path)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    print("\nERROR: Unsupported file type.")
    print("Please upload a .txt or .pdf syllabus.")
    return ""


def estimate_difficulty(task_name: str, task_type: str) -> int:
    text = task_name.lower()
    difficulty = 4

    if "final" in text:
        difficulty += 5
    elif "midterm" in text or "exam" in text:
        difficulty += 4
    elif "project" in text or "programming" in text or "coding" in text:
        difficulty += 4
    elif "essay" in text or "paper" in text or "lab" in text:
        difficulty += 3
    elif "quiz" in text:
        difficulty += 2
    elif "homework" in text or "assignment" in text:
        difficulty += 1

    if task_type == "exam_study":
        difficulty += 1
    elif task_type == "quiz_study":
        difficulty += 1

    return min(difficulty, 10)


def estimate_hours(task_type: str, difficulty: int) -> float:
    if task_type == "exam_study":
        return max(3, difficulty * 0.7)
    if task_type == "quiz_study":
        return max(1.5, difficulty * 0.4)
    if task_type == "project":
        return max(4, difficulty * 0.8)
    if task_type == "essay":
        return max(3, difficulty * 0.6)

    return max(1, difficulty * 0.35)


def classify_task_type(task_name: str) -> str:
    text = task_name.lower()

    if "final" in text or "midterm" in text or "exam" in text:
        return "exam_study"
    if "quiz" in text:
        return "quiz_study"
    if "project" in text:
        return "project"
    if "essay" in text or "paper" in text:
        return "essay"

    return "homework"


def parse_due_date(date_text: str):
    date_text = date_text.strip()

    formats = [
        "%m/%d/%Y",
        "%m/%d/%y",
        "%Y-%m-%d",
        "%b %d %Y",
        "%B %d %Y",
        "%b %d, %Y",
        "%B %d, %Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_text, fmt)
        except ValueError:
            pass

    return None


def extract_tasks_from_syllabus(text: str, class_name: str) -> list[Task]:
    keywords = [
        "homework", "assignment", "quiz", "exam", "midterm",
        "final", "project", "essay", "paper", "lab"
    ]

    date_patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{4}-\d{1,2}-\d{1,2}\b",
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b",
    ]

    tasks = []
    today = datetime.today()

    for line in text.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if not any(keyword in lower_line for keyword in keywords):
            continue

        due_date_text = "Unknown"
        due_date_object = None

        for pattern in date_patterns:
            match = re.search(pattern, clean_line, re.IGNORECASE)

            if match:
                due_date_text = match.group(0)
                due_date_object = parse_due_date(due_date_text.replace(".", ""))
                break

        if due_date_object:
            days_until_due = max((due_date_object - today).days, 1)
        else:
            days_until_due = 30

        task_type = classify_task_type(clean_line)
        difficulty = estimate_difficulty(clean_line, task_type)
        hours_needed = estimate_hours(task_type, difficulty)

        tasks.append(
            Task(
                name=clean_line,
                class_name=class_name,
                due_date=due_date_text,
                days_until_due=days_until_due,
                difficulty=difficulty,
                hours_needed=round(hours_needed, 1),
                task_type=task_type,
            )
        )

    return tasks


def calculate_priority(task: Task) -> float:
    urgency_score = 10 / max(task.days_until_due, 1)

    study_bonus = 0
    if task.task_type == "quiz_study":
        study_bonus = 3
    elif task.task_type == "exam_study":
        study_bonus = 5

    return urgency_score + task.difficulty + task.hours_needed + study_bonus


def create_schedule(tasks: list[Task]) -> list[tuple[Task, float]]:
    heap = []

    for index, task in enumerate(tasks):
        priority = calculate_priority(task)
        heapq.heappush(heap, (-priority, index, task))

    schedule = []

    while heap:
        negative_priority, _, task = heapq.heappop(heap)
        schedule.append((task, round(-negative_priority, 2)))

    return schedule


def print_schedule(schedule: list[tuple[Task, float]]) -> None:
    print("\nADATS Recommended Schedule")
    print("=" * 70)

    if not schedule:
        print("No tasks were found.")
        print("Try using a syllabus where assignment lines include words like:")
        print("homework, assignment, quiz, exam, midterm, final, project, essay, lab")
        return

    for rank, (task, priority) in enumerate(schedule, start=1):
        print(f"{rank}. {task.name}")
        print(f"   Class: {task.class_name}")
        print(f"   Type: {task.task_type}")
        print(f"   Due Date: {task.due_date}")
        print(f"   Days Until Due: {task.days_until_due}")
        print(f"   Estimated Difficulty: {task.difficulty}/10")
        print(f"   Estimated Hours Needed: {task.hours_needed}")
        print(f"   Priority Score: {priority}")
        print()


def demo_mode():
    class_name = "Algorithm"

    sample_syllabus = """
    Homework 1 - Big O Practice due 09/10/2026
    Quiz 1 - Sorting Algorithms due 09/15/2026
    Programming Project - Priority Queue Scheduler due 09/25/2026
    Midterm Exam - Graphs and Dynamic Programming due 10/12/2026
    Final Exam - Comprehensive Review due 12/10/2026
    """

    tasks = extract_tasks_from_syllabus(sample_syllabus, class_name)
    schedule = create_schedule(tasks)
    print_schedule(schedule)


def upload_syllabus_mode():
    all_tasks = []

    try:
        number_of_classes = int(input("How many classes are you taking? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for i in range(number_of_classes):
        class_name = input(f"\nEnter class #{i + 1} name: ")
        file_path = input(f"Enter syllabus file path for {class_name} (.txt or .pdf): ")

        syllabus_text = read_syllabus_file(file_path)

        if not syllabus_text:
            print(f"No text found for {class_name}. Skipping.")
            continue

        tasks = extract_tasks_from_syllabus(syllabus_text, class_name)
        all_tasks.extend(tasks)

        print(f"Found {len(tasks)} possible tasks for {class_name}.")

    schedule = create_schedule(all_tasks)
    print_schedule(schedule)


def main():
    print("Adaptive Deadline-Aware Task Sorting (ADATS)")
    print("1. Run demo syllabus")
    print("2. Upload my syllabus files")

    choice = input("Choose option 1 or 2: ")

    if choice == "2":
        upload_syllabus_mode()
    else:
        demo_mode()


if __name__ == "__main__":
    main()
