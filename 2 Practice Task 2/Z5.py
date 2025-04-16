class MyClass:
    def __init__(self, prop1="def1", prop2="def2"):
        self.prop1 = prop1
        self.prop2 = prop2
        print(f"Создан объект с свойствами: {self.prop1}, {self.prop2}")

    def __del__(self):
        print(f"Удалён объект с свойствами: {self.prop1}, {self.prop2}")

def main_menu():

    while True:
        print("\nГлавное меню:")
        print("1. Создание объекта с параметрами по умолчанию:")
        print("2. Создание объекта с заданными параметрами:")
        print("3. Удаление объектов вручную:")
        print("4. Создание и автоматическое удаление временного объекта:")
        print("5. Завершить программу")

        choice = input("Выберите действие (1-5): ")
        print("\n")

        if choice == "1":
            obj1 = MyClass()
            print(f"Свойства obj1: {obj1.prop1}, {obj1.prop2}")

        if choice == "2":
            a = input("Введите слово: ")
            b = int(input("Введите число: "))
            obj2 = MyClass(a, b)
            print(f"Свойства obj2: {obj2.prop1}, {obj2.prop2}")

        if choice == "3":
            del obj1
            del obj2

        if choice == "4":
            i = input("Введите слово: ")
            j = input("Введите слово: ")
            temp_obj = MyClass(i, j)
            del temp_obj
        if choice == "5":
            print("Программа завершенна")
            break

if __name__ == "__main__":
    main_menu()
