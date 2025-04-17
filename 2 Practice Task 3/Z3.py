class Calculation:
    def __init__(self):
        self.calculationLine = ""

    def SetCalculationLine(self, value):
        self.calculationLine = value

    def SetLastSymbolCalculationLine(self, symbol):
        self.calculationLine += symbol

    def GetCalculationLine(self):
        return self.calculationLine

    def GetLastSymbol(self):
        if self.calculationLine:
            return self.calculationLine[-1]
        return ""

    def DeleteLastSymbol(self):
        if self.calculationLine:
            self.calculationLine = self.calculationLine[:-1]


def main_menu():
    calc = Calculation()
    calc.SetCalculationLine("100")

    while True:
        print("\nГлавное меню:")
        print("1. Установить новое значение")
        print("2. Посмотреть текущее значение")
        print("3. Добавить символ в конец")
        print("4. Получить последний символ")
        print("5. Удалить последний символ")
        print("6. Выход")

        choice = input("Выберите действие (1-6): ")

        if choice == "1":
            new_value = input("Введите новое значение: ")
            calc.SetCalculationLine(new_value)
            print(f"Значение установлено: {calc.GetCalculationLine()}")

        elif choice == "2":
            print("\nТекущая строка:", calc.GetCalculationLine())

        elif choice == "3":
            symbol = input("Введите символ для добавления: ")
            calc.SetLastSymbolCalculationLine(symbol)
            print("Результат после добавления:", calc.GetCalculationLine())

        elif choice == "4":
            last_symbol = calc.GetLastSymbol()
            print("Последний символ:", last_symbol if last_symbol else "строка пуста")

        elif choice == "5":
            calc.DeleteLastSymbol()
            print("Последний символ удален.")
            print("Tекущая строка:", calc.GetCalculationLine())
        elif choice == "6":
            print("Программа завершенна")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите от 1 до 6.")


if __name__ == "__main__":
    main_menu()