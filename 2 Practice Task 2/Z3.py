class NumberPair:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def display_numbers(self):
        print(f"Число 1: {self.num1}, Число 2: {self.num2}")

    def change_numbers(self, new_num1, new_num2):
        self.num1 = new_num1
        self.num2 = new_num2
        print("Числа успешно изменены.")

    def calculate_sum(self):
        return self.num1 + self.num2

    def find_max(self):
        return max(self.num1, self.num2)


a = int(input("Введите первое число: "))
b = int(input("Введите второе число: "))
pair = NumberPair(a, b)

def main_menu():
    while True:
        print("\nГлавное меню:")
        print("1. Вывести информацию")
        print("2. Изменить числа")
        print("3. Завершить программу")

        choice = input("Выберите действие (1-3): ")
        print("\n")

        if choice == "1":
            pair.display_numbers()
            print(f"Наибольшее: {pair.find_max()}")
            print(f"Сумма: {pair.calculate_sum()}")


        if choice == "2":
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
            pair.change_numbers(a, b)
            pair.display_numbers()

        if choice == "3":
            print("Программа завершенна")
            break
if __name__ == "__main__":
    main_menu()