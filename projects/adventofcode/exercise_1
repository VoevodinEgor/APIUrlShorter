print("Введите количество эльфов")
elfs_count = int(input())
elfs_food = []
print("Введите для каждого эльфа количество каллорий каждого продукта через ','")
for elf in range(elfs_count):
    elfs_food.append(list(map(int, input().split(','))))
max_callories = max(list(map(sum, elfs_food)))
for i, food in enumerate(elfs_food):
    sum_callories = sum(food)
    if sum_callories == max_callories:
        print(f"У эльфа под номером {i+1} наибольшее количество калорий {sum_callories}")