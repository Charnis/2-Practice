class Worker:
    def __init__(self, name, surname, rate, days):
        self.__name = name
        self.__surname = surname
        self.__rate = rate
        self.__days = days

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_rate(self):
        return self.__rate

    def get_days(self):
        return self.__days

    def GetSalary(self):
        return self.__rate * self.__days

    def display_info(self):
        print(f"Имя: {self.__name}")
        print(f"Фамилия: {self.__surname}")
        print(f"Ставка за день работы: {self.__rate}")
        print(f"Количество отработанных дней: {self.__days}")


Workers = [
    Worker("Иван", "Иванов", 1312, 30),
    Worker("Петр", "Петров", 1500, 30),
    Worker("Михаил", "Сидоров", 2160, 30),
    Worker("Григорий", "Гришаев", 1512, 30),
    Worker("Василий", "Васильев", 2000, 30)
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
            print("\nСписок всех рабочих:")
            for i, worker in enumerate(Workers, 1):
                print(f"Рабочий №{i}")
                worker.display_info()
                print("\n")

        elif choice == "2":
            print("\nСписок всех рабочих:")
            for i, worker in enumerate(Workers, 1):
                print(f"Рабочий №{i}")
                worker.display_info()
                salary = worker.GetSalary()
                print(f"Зарплата рабочего: {salary} рублей\n")

        elif choice == "3":
            print("\nПоиск Рабочего:")
            search_surname = input("Введите фамилию рабочего: ")

            found = False
            for worker in Workers:
                if worker.get_surname() == search_surname:
                    found = True
                    salary = worker.GetSalary()
                    print(f"\nНайден рабочий: {worker.get_name()} {worker.get_surname()}")
                    print(f"Зарплата рабочего: {salary} рублей")
                    break

            if not found:
                print("Рабочий не найден!")

        elif choice == "4":
            print("\nИзмененный список всех рабочих: ")
            for i, worker in enumerate(Workers, 1):
                print(f"Рабочий №{i}")
                worker.display_info()
                print("\n")
            break


if __name__ == "__main__":
    main_menu()