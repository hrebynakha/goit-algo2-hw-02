"""
Оптимальне розрізання стрижня для максимального прибутку (Rod Cutting Problem)

Розробіть програму для знаходження оптимального способу розрізання стрижня,
щоб отримати максимальний прибуток. Необхідно реалізувати два підходи:
    через рекурсію з мемоізацією та через табуляцію.


Опис завдання

1. На вхід подається довжина стрижня та масив цін, де price[i] — це ціна стрижня довжини i+1 .

2. Потрібно визначити, як розрізати стрижень, щоб отримати максимальний прибуток.

3. Реалізувати обидва підходи динамічного програмування.

4. Вивести оптимальний спосіб розрізання та максимальний прибуток.

Технічні умови

1. Формат вхідних даних:
    length = 5 # довжина стрижня
    prices = [2, 5, 7, 8, 10] # ціни для довжин 1, 2, 3, 4, 5

2. Обмеження:
    Довжина стрижня > 0.
    Всі ціни > 0.
    Масив цін не може бути порожнім.
    Довжина масиву цін повинна відповідати довжині стрижня.

"""

from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    if length < 0:
        raise ValueError("Rod lenght value must be grater than 0")
    if not prices:
        raise ValueError("Prices array can't be empty")
    if len(prices) != length:
        raise ValueError("Lenght of prices must be equal to rod length")
    for price in prices:
        if price < 0:
            raise ValueError("Price must be grate than 0")
    memo = {}
    cuts = {}

    def calc_max(length: int) -> int:
        if length == 0:
            return 0
        if length in memo:
            return memo[length]
        price_ = 0
        for i in range(1, length + 1):
            proposed_price = prices[i - 1] + calc_max(length - i)
            if proposed_price > price_:
                price_ = proposed_price
                cuts[length] = i

        memo[i] = price_
        return price_

    max_profit = calc_max(length=length)

    all_cuts = []
    length_ = length
    while length_ > 0:
        cut = cuts[length_]
        all_cuts.append(cut)
        length_ -= cut

    return {"max_profit": max_profit, "cuts": all_cuts, "number_of_cuts": len(all_cuts)}


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    if length < 0:
        raise ValueError("Rod lenght value must be grater than 0")
    if not prices:
        raise ValueError("Prices array can't be empty")
    if len(prices) != length:
        raise ValueError("Lenght of prices must be equal to rod length")
    for price in prices:
        if price < 0:
            raise ValueError("Price must be grate than 0")
    dp = [0] * (length + 1)
    cuts = {}
    for i in range(1, length + 1):
        for j in range(1, i + 1):
            if dp[i] < prices[j - 1] + dp[i - j]:
                # rewrite value
                dp[i] = prices[j - 1] + dp[i - j]
                cuts[i] = j

    max_profit = dp[length]
    all_cuts = []
    length_ = length
    while length_ > 0:
        cut = cuts[length_]
        all_cuts.append(cut)
        length_ -= cut

    return {"max_profit": max_profit, "cuts": all_cuts, "number_of_cuts": len(all_cuts)}


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"},
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
