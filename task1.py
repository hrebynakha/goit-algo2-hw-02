from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    """Print job class"""

    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    """PrinterConstraints"""

    max_volume: float
    max_items: int


def optimize_printing(
    print_jobs: List[PrintJob], constraints: PrinterConstraints
) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """

    def get_q_time(queue) -> int:
        return max(q.print_time for q in queue) if queue else 0

    def get_volume_size(queue) -> float:
        return sum(q.volume for q in queue)

    def is_volume_full(queue) -> bool:
        return constraints.max_volume <= get_volume_size(queue)

    def is_item_full(queue) -> bool:
        return constraints.max_items <= len(queue)

    print_order = []
    total_time = 0
    print_queue = []
    sorted_job = sorted(print_jobs, key=lambda x: x.priority)

    for job in sorted_job:
        if is_volume_full(print_queue) or is_item_full(print_queue):
            total_time += get_q_time(print_queue)
            print_queue = []
        if get_volume_size(print_queue) + job.volume > constraints.max_volume:
            total_time += get_q_time(print_queue)
            print_queue = []

        print_queue.append(job)
        print_order.append(job.id)

    total_time += get_q_time(print_queue)

    return {"print_order": print_order, "total_time": total_time}


# Тестування
def test_printing_optimization():
    """Test printing models"""
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        PrintJob(id="M1", volume=100, priority=1, print_time=120),
        PrintJob(id="M2", volume=150, priority=1, print_time=90),
        PrintJob(id="M3", volume=120, priority=1, print_time=150),
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        PrintJob(id="M1", volume=100, priority=2, print_time=120),  # лабораторна
        PrintJob(id="M2", volume=150, priority=1, print_time=90),  # дипломна
        PrintJob(id="M3", volume=120, priority=3, print_time=150),  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        PrintJob(id="M1", volume=250, priority=1, print_time=180),
        PrintJob(id="M2", volume=200, priority=1, print_time=150),
        PrintJob(id="M3", volume=180, priority=2, print_time=120),
    ]

    constraints = PrinterConstraints(max_volume=300, max_items=2)

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
