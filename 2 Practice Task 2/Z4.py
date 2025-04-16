import random




class NumberPair:
    def __init__(self, num1):
        self.num1 = num1

    def display_numbers(self):
        print(f"Число: {self.num1}")

    def change_numbers(self, new_num1):
        self.num1 = new_num1
        print("Число успешно изменено.")

b = 0
default = b
pair = NumberPair(b)
print("Число по умолчанию = 0")


def main_menu():
    global default
    global b
    while True:
        print("\nГлавное меню:")
        print("1. Вывести информацию")
        print("2. Изменить числа")
        print("3. Вернуть число по умолчанию")
        print("4. Для увеличения или уменьшения числа на единицу")
        print("5. Завершить программу")

        choice = input("Выберите действие (1-5): ")
        print("\n")

        if choice == "1":
            pair.display_numbers()

        if choice == "2":
            j = int(input("Выберите число по умолчанию. (1 = 0, 2 - произвольное (от 1 до 100): "))
            if j == 1:
                b = 0
                pair.change_numbers(b)
                default = b
            elif j == 2:
                b = random.randint(1,100)
                pair.change_numbers(b)
                default = b
            else:
                print("Неверно указанно число")

        if choice == "3":
            #default = b
            pair.change_numbers(default)

        if choice == "4":
            plus_minus = input("Введите '+' для увеличения числа на 1, или '-' для уменьшения числа на 1: ")
            if plus_minus == "+":
                b += 1
                pair.change_numbers(b)
            elif plus_minus == "-":
                b -= 1
                pair.change_numbers(b)
        if choice == "5":
            print("Программа завершенна")
            break

if __name__ == "__main__":
    main_menu()