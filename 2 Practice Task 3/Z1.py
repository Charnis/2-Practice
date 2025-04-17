class Worker:
    def __init__(self, name, surname, rate, days):
        self.name = name
        self.surname = surname
        self.rate = rate
        self.days = days

    def GetSalary(self):
        return self.rate * self.days

    def display_info(self):
        print(f"Имя: {self.name}")
        print(f"Фамилия: {self.surname}")
        print(f"Ставка за день работы: {self.rate}")
        print(f"Количество отработанных дней: {self.days}")

Workers = [
    Worker("Иван", "Иванов", 1312, 30),
    Worker("Петр", "Петров", 1500, 30),
    Worker("Михаил", "Сидоров", 2160, 30),
    Worker("Григорий","Гришаев",1512,30),
    Worker("Василий","Васильев",2000,30)
]

def main_menu():
    while True:
        print("\nГлавное меню:")
        print("1. Просмотреть список рабочих")
        print("2. Просмотреть зарплаты всех рабочих")
        print("3. Вывести зарплату определенного работника")
        print("4. Завершить редактирование")

        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            print("\nСписок всех студентов:")
            for i, Worker in enumerate(Workers, 1):
                print(f"Рабочий №{i}")
                Worker.display_info()
                print("\n")

        elif choice == "2":
            print("\nСписок всех студентов:")
            for i, Worker in enumerate(Workers, 1):
                print(f"Рабочий №{i}")
                Worker.display_info()
                salary = Worker.GetSalary()
                print(f"Зарплата рабочего: {salary} рублей\n")

        elif choice == "3":

            print("\nПоиск Рабочего:")
            search_surname = input("Введите фамилию рабочего: ")

            found = False
            for Worker in Workers:
                if Worker.surname == search_surname:
                    found = True
                    salary = Worker.GetSalary()
                    print(f"\nНайден рабочий: {Worker.name} {Worker.surname}")
                    print(f"Зарплата рабочего: {salary} рублей")
                    break

            if not found:
                print("Рабочий не найден!")

        elif choice == "4":
            print("\nИзмененный список всех студентов: ")
            for i, Worker in enumerate(Workers, 1):
                print(f"Студент №{i}")
                Worker.display_info()
                print("\n")
            break

if __name__ == "__main__":
    main_menu()