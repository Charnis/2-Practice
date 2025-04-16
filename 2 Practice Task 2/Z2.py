class Train:
    def __init__(self, Destination, numbers_train, Departure_time):
        self.numbers_train = numbers_train
        self.Destination = Destination
        self.numbers_train = numbers_train
        self.Departure_time = Departure_time

    def update_Destination(self, new_Destination):
        self.Destination = new_Destination

    def update_numbers_train_date(self, new_numbers_train_date):
        self.numbers_train_date = new_numbers_train_date

    def update_Departure_timer(self, new_Departure_time):
        self.Departure_time = new_Departure_time

    def display_info(self):
        print(f"Пункт назначения: {self.Destination}")
        print(f"Номер поезда: {self.numbers_train}")
        print(f"Время отправления: {self.Departure_time}")

Trains = [
    Train("Moscow", "1", "25.12.2024, 13:00"),
    Train("Tomsk", "2", "15.01.2025, 16:10"),
    Train("Novosibirsk", "3", "10.07.2025, 17:00"),
    Train("Saint-Petersburg","4","15.05.2025, 20:10")
]

def main_menu():
    while True:
        print("\nГлавное меню:")
        print("1. Просмотреть список поездов")
        print("2. Вывести информацию об определенном поезде")
        print("3. Завершить программу")

        choice = input("Выберите действие (1-3): ")

        if choice == "1":
            print("\nСписок всех поездов:")
            for i, train in enumerate(Trains, 1):
                print(f"Поезд №{i}")
                train.display_info()
                print("\n")


        elif choice == "2":
            b = int(input("\nВведите номер поезда: "))
            j = 0
            if b == 1:
                j = 0
            elif b == 2:
                j = 1
            elif b == 3:
                j = 2
            elif b == 4:
                j = 3
            train = Trains[j]
            train.display_info()

        elif choice == "3":
            print("Программа завершенна")
            break

if __name__ == "__main__":
    main_menu()