from pulp import *


def lb_2():
    distances = {'Одеса': {'Харків': 712, 'Чернігів': 610, 'Житомир': 501, 'Миколаїв': 150},
                 'Ужгород': {'Харків': 1296, 'Чернігів': 950, 'Житомир': 668, 'Миколаїв': 1095},
                 'Дніпро': {'Харків': 218, 'Чернігів': 543, 'Житомир': 617, 'Миколаїв': 329},
                 'Вінниця': {'Харків': 713, 'Чернігів': 401, 'Житомир': 153, 'Миколаїв': 502},
                 'Черкаси': {'Харків': 403, 'Чернігів': 297, 'Житомир': 321, 'Миколаїв': 317}}

    supplies = {'Одеса': 10, 'Ужгород': 11, 'Дніпро': 8, 'Вінниця': 10, 'Черкаси': 6}
    demands = {'Харків': 18, 'Чернігів': 11, 'Житомир': 9, 'Миколаїв': 7}

    prob = LpProblem("CandyTransportation", LpMinimize)

    # Визначення змінних
    transport_vars = LpVariable.dicts("Route", (supplies.keys(), demands.keys()), 0)

    # Додавання обмежень щодо постачань та потреб
    for supply in supplies:
        prob += lpSum(transport_vars[supply][demand] for demand in demands) <= supplies[supply]

    for demand in demands:
        prob += lpSum(transport_vars[supply][demand] for supply in supplies) == demands[demand]

    # Додавання обмежень заборонених маршрутів та обмежень на кількість тонн
    prob += transport_vars['Одеса']['Харків'] == 0
    prob += transport_vars['Ужгород']['Харків'] == 0
    prob += transport_vars['Ужгород']['Чернігів'] <= 4
    prob += lpSum(transport_vars['Одеса'][demand] for demand in demands) >= 3

    
    prob += lpSum(
        (5. if distances[supply][demand] <= 300 else 5 + 0.5 * (abs(distances[supply][demand] - 300) // 100)) *
        transport_vars[supply][demand]
        for supply in supplies for demand in demands)

    # Розв'язання задачі
    prob.solve()

    # Виведення результатів
    print("Оптимальний маршрут перевезення цукерок:")
    final_list = [
        f"{supply} -> {demand}: {transport_vars[supply][demand].value()} т"
        for supply in supplies
        for demand in demands
        if transport_vars[supply][demand].value() > 0
    ]

    # Виведення оптимальної вартості доставлення цукерок
    final_list.append(("Оптимальна вартість доставлення цукерок:" + str(value(prob.objective) * 1000) + " грн"))
    return final_list

# Call the lb_2() function and print the result
result = lb_2()
for item in result:
    print(item)