"""
Adaptive Deadline-Aware Task Sorting (ADATS)

This program helps a student taking 5 classes:
1. Computer Science
2. Math
3. English
4. Computer Architecture
5. Algorithm

The program does two main things:
1. Creates a homework/study schedule using a priority queue.
2. Predicts each class grade and the probability of earning an A.

ADATS considers:
- Due dates
- Assignment difficulty
- Estimated hours needed
- Quiz/exam study time
- Homework completion rate
- Study time completion rate
"""

from dataclasses import dataclass
import heapq


@dataclass
class Task:
    name: str
    class_name: str
    days_until_due: int
    difficulty: int          # 1 = easy, 10 = very hard
    hours_needed: float
    task_type: str           # homework, quiz_study, exam_study


@dataclass
class ClassProgress:
    class_name: str
    current_score: float
    completed_homework: int
    total_homework: int
    actual_study_hours: float
    required_study_hours: float


def calculate_priority(task: Task) -> float:
    """
    Calculates a priority score for a task.

    Higher score means the task should be completed earlier.
    """

    # Assignments due sooner receive higher urgency.
    urgency_score = 10 / max(task.days_until_due, 1)

    # Study blocks receive extra priority so quizzes and exams are not ignored.
    study_bonus = 0

    if task.task_type == "quiz_study":
        study_bonus = 3
    elif task.task_type == "exam_study":
        study_bonus = 5

    # Final priority formula.
    priority = urgency_score + task.difficulty + task.hours_needed + study_bonus

    return priority


def create_schedule(tasks):
    """
    Creates a recommended task order using a priority queue.

    Python heapq is a min-heap.
    Negative priority is used so the highest score comes out first.
    """

    priority_queue = []

    for index, task in enumerate(tasks):
        priority = calculate_priority(task)
        heapq.heappush(priority_queue, (-priority, index, task))

    schedule = []

    while priority_queue:
        negative_priority, _, task = heapq.heappop(priority_queue)
        priority = -negative_priority
        schedule.append((task, priority))

    return schedule


def get_letter_grade(score: float) -> str:
    """
    Converts a number score into a letter grade.
    """

    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def calculate_a_probability(class_progress: ClassProgress) -> float:
    """
    Estimates the probability of earning an A.

    The model uses:
    - 60% homework completion rate
    - 40% study time completion rate

    This is a simple algorithmic estimate, not a guaranteed prediction.
    """

    if class_progress.total_homework == 0:
        homework_rate = 1
    else:
        homework_rate = class_progress.completed_homework / class_progress.total_homework

    if class_progress.required_study_hours == 0:
        study_rate = 1
    else:
        study_rate = class_progress.actual_study_hours / class_progress.required_study_hours

    # Cap study rate at 1 so extra studying does not exceed 100%.
    study_rate = min(study_rate, 1)

    probability = (homework_rate * 0.60 + study_rate * 0.40) * 100

    return round(probability, 2)


def print_schedule(schedule):
    """
    Prints the ADATS recommended weekly schedule.
    """

    print("ADATS Recommended Weekly Schedule")
    print("=" * 50)

    total_hours = 0

    for rank, (task, priority) in enumerate(schedule, start=1):
        total_hours += task.hours_needed

        print(f"{rank}. {task.name}")
        print(f"   Class: {task.class_name}")
        print(f"   Type: {task.task_type}")
        print(f"   Due in: {task.days_until_due} day(s)")
        print(f"   Difficulty: {task.difficulty}/10")
        print(f"   Hours needed: {task.hours_needed}")
        print(f"   Priority score: {priority:.2f}")
        print()

    print(f"Total planned homework/study time: {total_hours} hours")
    print()


def print_grade_predictions(classes):
    """
    Prints score, letter grade, and chance of earning an A.
    """

    print("Grade Prediction")
    print("=" * 50)

    for class_progress in classes:
        letter_grade = get_letter_grade(class_progress.current_score)
        a_probability = calculate_a_probability(class_progress)

        print(f"{class_progress.class_name}")
        print(f"   Current Score: {class_progress.current_score}")
        print(f"   Predicted Grade: {letter_grade}")
        print(f"   Homework Completed: {class_progress.completed_homework}/{class_progress.total_homework}")
        print(f"   Study Hours: {class_progress.actual_study_hours}/{class_progress.required_study_hours}")
        print(f"   Chance of Getting an A: {a_probability}%")
        print()


def main():
    """
    Example scenario:
    A student is taking 5 classes and has about 8 homework assignments
    due during the week, plus quiz and exam study time.
    """

    tasks = [
        Task("Programming Lab", "Computer Science", 2, 9, 4, "homework"),
        Task("Python Discussion Post", "Computer Science", 4, 5, 1, "homework"),

        Task("Linear Algebra Homework", "Math", 1, 7, 2, "homework"),
        Task("Study for Math Quiz", "Math", 2, 8, 2, "quiz_study"),

        Task("Essay Draft", "English", 3, 6, 3, "homework"),
        Task("Reading Response", "English", 5, 4, 1.5, "homework"),

        Task("CPU Design Worksheet", "Computer Architecture", 2, 8, 3, "homework"),
        Task("Memory Hierarchy Notes", "Computer Architecture", 4, 6, 2, "homework"),

        Task("Graph Algorithm Assignment", "Algorithm", 1, 9, 3, "homework"),
        Task("Study for Algorithm Midterm", "Algorithm", 6, 10, 5, "exam_study"),
    ]

    classes = [
        ClassProgress("Computer Science", 95, 2, 2, 5, 5),
        ClassProgress("Math", 88, 1, 2, 2, 3),
        ClassProgress("English", 91, 2, 2, 3, 3),
        ClassProgress("Computer Architecture", 84, 2, 2, 3, 4),
        ClassProgress("Algorithm", 97, 1, 1, 5, 5),
    ]

    schedule = create_schedule(tasks)

    print_schedule(schedule)
    print_grade_predictions(classes)


if __name__ == "__main__":
    main()
