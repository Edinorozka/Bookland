import math
firstс = 0
secondс = 0

while True:
    try:
        firstс = int(input("Введите катет: "))
        secondс = int(input("Введите второй: "))
        break
    except ValueError:
        print("Вы не ввели два числа")
        continue
print("Площадь треугольника с катетами " + str(firstс) + " и " + str(secondс) + " = " + str(round((firstс * secondс) / 2, 2)))
print("Периметр треугольника " + str(firstс) + " и " + str(secondс) + " = " + str(round(math.sqrt(firstс ** 2 + secondс ** 2), 2)))
