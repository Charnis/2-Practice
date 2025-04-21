import sqlite3


class StudentDatabase:
    def __init__(self, db_name="student.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                middle_name TEXT NOT NULL,
                group_name TEXT NOT NULL,
                grades TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_student(self, first_name, last_name, middle_name, group_name, grades):
        grades_str = ','.join(map(str, grades))
        self.cursor.execute('''
            INSERT INTO students (first_name, last_name, middle_name, group_name, grades)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, middle_name, group_name, grades_str))
        self.connection.commit()

    def view_all_students(self):
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()

    def view_student(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = self.cursor.fetchone()
        if student:
            grades = list(map(int, student[5].split(',')))
            average_grade = sum(grades) / len(grades)
            return student, average_grade
        return None

    def update_student(self, student_id, first_name, last_name, middle_name, group_name, grades):
        grades_str = ','.join(map(str, grades))
        self.cursor.execute('''
            UPDATE students
            SET first_name = ?, last_name = ?, middle_name = ?, group_name = ?, grades = ?
            WHERE id = ?
        ''', (first_name, last_name, middle_name, group_name, grades_str, student_id))
        self.connection.commit()

    def delete_student(self, student_id):
        self.cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        self.connection.commit()

    def average_grade_by_group(self, group_name):
        self.cursor.execute('SELECT grades FROM students WHERE group_name = ?', (group_name,))
        grades_list = self.cursor.fetchall()
        if grades_list:
            all_grades = []
            for grades in grades_list:
                all_grades.extend(map(int, grades[0].split(',')))
            return sum(all_grades) / len(all_grades)
        return None

    def close(self):
        self.connection.close()

def main():
    db = StudentDatabase()

    while True:
        print("\nМеню:")
        print("1. Добавить нового студента")
        print("2. Просмотреть всех студентов")
        print("3. Просмотреть одного студента")
        print("4. Редактировать информацию о студенте")
        print("5. Удалить студента")
        print("6. Просмотреть средний балл студентов в группе")
        print("7. Выйти")

        choice = input("\nВыберите действие (1-7): ")

        if choice == "1":
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            middle_name = input("Введите отчество: ")
            group_name = input("Введите группу: ")
            grades = list(map(int, input("Введите 4 оценки через пробел: ").split()))
            if len(grades) == 4:
                db.add_student(first_name, last_name, middle_name, group_name, grades)
                print("Студент успешно добавлен!")
            else:
                print("Ошибка: необходимо ввести ровно 4 оценки.")

        elif choice == "2":
            students = db.view_all_students()
            print("\nСписок студентов:")
            for student in students:
                print(student)

        elif choice == "3":
            student_id = int(input("Введите ID студента: "))
            student_data = db.view_student(student_id)
            if student_data:
                student, avg_grade = student_data
                print(f"\nИнформация о студенте: {student}")
                print(f"Средний балл: {avg_grade}")
            else:
                print("Студент с таким ID не найден.")

        elif choice == "4":
            student_id = int(input("Введите ID студента для редактирования: "))
            first_name = input("Введите новое имя: ")
            last_name = input("Введите новую фамилию: ")
            middle_name = input("Введите новое отчество: ")
            group_name = input("Введите новую группу: ")
            grades = list(map(int, input("Введите 4 новые оценки через пробел: ").split()))
            if len(grades) == 4:
                db.update_student(student_id, first_name, last_name, middle_name, group_name, grades)
                print("Информация о студенте успешно обновлена!")
            else:
                print("Ошибка: необходимо ввести ровно 4 оценки.")

        elif choice == "5":
            student_id = int(input("Введите ID студента для удаления: "))
            db.delete_student(student_id)
            print("Студент успешно удалён!")

        elif choice == "6":
            group_name = input("Введите название группы: ")
            avg_grade = db.average_grade_by_group(group_name)
            if avg_grade is not None:
                print(f"Средний балл студентов группы {group_name}: {avg_grade}")
            else:
                print("В этой группе нет студентов.")

        elif choice == "7":
            db.close()
            print("Завершение программы")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите действие из меню.")


if __name__ == "__main__":
    main()