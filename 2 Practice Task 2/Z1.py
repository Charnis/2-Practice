class Student:
    def __init__(self, numbers, surname, birth_date, group_number, grades):
        self.numbers = numbers
        self.surname = surname
        self.birth_date = birth_date
        self.group_number = group_number
        self.grades = grades

    def update_surname(self, new_surname):
        self.surname = new_surname

    def update_birth_date(self, new_birth_date):
        self.birth_date = new_birth_date

    def update_group_number(self, new_group_number):
        self.group_number = new_group_number

    def display_info(self):
        print(f"Номер: {self.numbers}")
        print(f"Фамилия: {self.surname}")
        print(f"Дата рождения: {self.birth_date}")
        print(f"Номер группы: {self.group_number}")
        print(f"Успеваемость: {self.grades}")

students = [
    Student(1, "Иванов", "01.01.2000", "ГР-101", [4, 5, 5, 4, 5]),
    Student(2, "Петров", "15.05.2001", "ГР-102", [3, 4, 4, 3, 5]),
    Student(3, "Сидоров", "20.11.1999", "ГР-101", [4, 5, 5, 3, 3]),
    Student(4,"Гришаев","15.01.2002","ГР-103", [5, 4, 4, 4, 5]),
    Student(5,"Васильев","05.12.1998","ГР-102", [5, 3, 4, 3, 4])
]

def main_menu():
    while True:
        print("\nГлавное меню:")
        print("1. Просмотреть список студентов")
        print("2. Найти и изменить данные студента")
        print("3. Вывести информацию об определенном студенте")
        print("4. Завершить редактирование")

        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            print("\nСписок всех студентов:")
            for i, student in enumerate(students, 1):
                print(f"Студент №{i}")
                student.display_info()
                print("\n")

        elif choice == "2":
            print("\nПоиск студента:")
            search_surname = input("Введите фамилию студента: ")
            search_birth_date = input("Введите дату рождения (в формате ДД.ММ.ГГГГ): ")

            found = False
            for student in students:
                if student.surname == search_surname and student.birth_date == search_birth_date:
                    found = True
                    print("\nНайден студент:")
                    student.display_info()

                    print("\nВведите новые данные:")
                    student.update_surname(input("Фамилия студента: "))
                    student.update_birth_date(input("Дата рождения студента (**.**.****): "))
                    student.update_group_number(input("Группа студента (ГР-***): "))

                    print("\nДанные обновлены:")
                    student.display_info()
                    break

            if not found:
                print("Студент не найден!")

        elif choice == "3":
            b = int(input("\nВведите номер студента: "))
            j = 0
            if b == 1:
                j = 0
            elif b == 2:
                j = 1
            elif b == 3:
                j = 2
            elif b == 4:
                j = 3
            elif b == 5:
                j = 4
            student = students[j]
            student.display_info()

        elif choice == "4":
            print("\nИзмененный список всех студентов: ")
            for i, student in enumerate(students, 1):
                print(f"Студент №{i}")
                student.display_info()
                print("\n")
            break

if __name__ == "__main__":
    main_menu()