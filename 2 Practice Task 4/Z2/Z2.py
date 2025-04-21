import sqlite3
from typing import List, Dict, Optional
from datetime import datetime


class Ingredient:
    def __init__(self, id: int, name: str, type: str, strength: float,
                 volume: float, price: float, quantity: float):
        self.id = id
        self.name = name
        self.type = type
        self.strength = strength
        self.volume = volume
        self.price = price
        self.quantity = quantity


class Cocktail:
    def __init__(self, id: int, name: str, ingredients: Dict[int, float], price: float):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.price = price


class BarManager:
    def __init__(self, db_name: str = 'bar.db'):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('alcohol', 'non-alcohol')),
                strength REAL DEFAULT 0,
                volume REAL NOT NULL,
                price REAL NOT NULL,
                quantity REAL NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cocktails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cocktail_ingredients (
                cocktail_id INTEGER,
                ingredient_id INTEGER,
                amount_ml REAL NOT NULL,
                PRIMARY KEY (cocktail_id, ingredient_id),
                FOREIGN KEY (cocktail_id) REFERENCES cocktails(id),
                FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN ('sale', 'restock')),
                item_type TEXT NOT NULL CHECK(item_type IN ('cocktail', 'ingredient')),
                item_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                total_price REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS revenue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL DEFAULT CURRENT_DATE,
                total_sales REAL NOT NULL DEFAULT 0,
                total_restocks REAL NOT NULL DEFAULT 0,
                UNIQUE(date)
            )
        ''')

        conn.commit()
        conn.close()

    def add_ingredient(self, ingredient: Ingredient) -> int:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ingredients (name, type, strength, volume, price, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (ingredient.name, ingredient.type, ingredient.strength,
              ingredient.volume, ingredient.price, ingredient.quantity))
        ingredient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return ingredient_id

    def get_ingredient(self, ingredient_id: int) -> Optional[Ingredient]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ingredients WHERE id = ?', (ingredient_id,))
        row = cursor.fetchone()
        conn.close()
        return Ingredient(*row) if row else None

    def get_all_ingredients(self) -> List[Ingredient]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ingredients')
        ingredients = [Ingredient(*row) for row in cursor.fetchall()]
        conn.close()
        return ingredients

    def update_ingredient(self, ingredient: Ingredient) -> bool:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE ingredients 
            SET name = ?, type = ?, strength = ?, volume = ?, price = ?, quantity = ?
            WHERE id = ?
        ''', (ingredient.name, ingredient.type, ingredient.strength,
              ingredient.volume, ingredient.price, ingredient.quantity, ingredient.id))
        affected = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return affected

    def add_cocktail(self, cocktail: Cocktail) -> int:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cocktails (name, price)
            VALUES (?, ?)
        ''', (cocktail.name, cocktail.price))
        cocktail_id = cursor.lastrowid

        for ing_id, amount in cocktail.ingredients.items():
            cursor.execute('''
                INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id, amount_ml)
                VALUES (?, ?, ?)
            ''', (cocktail_id, ing_id, amount))

        conn.commit()
        conn.close()
        return cocktail_id

    def get_cocktail(self, cocktail_id: int) -> Optional[Cocktail]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, price FROM cocktails WHERE id = ?', (cocktail_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        cursor.execute('''
            SELECT ingredient_id, amount_ml 
            FROM cocktail_ingredients 
            WHERE cocktail_id = ?
        ''', (cocktail_id,))
        ingredients = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()

        return Cocktail(
            id=row[0],
            name=row[1],
            ingredients=ingredients,
            price=row[2]
        )

    def get_all_cocktails(self) -> List[Cocktail]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, price FROM cocktails')
        cocktails = []

        for row in cursor.fetchall():
            cursor.execute('''
                SELECT ingredient_id, amount_ml 
                FROM cocktail_ingredients 
                WHERE cocktail_id = ?
            ''', (row[0],))
            ingredients = {r[0]: r[1] for r in cursor.fetchall()}
            cocktails.append(Cocktail(
                id=row[0],
                name=row[1],
                ingredients=ingredients,
                price=row[2]
            ))

        conn.close()
        return cocktails

    def calculate_cocktail_strength(self, cocktail_id: int) -> float:
        cocktail = self.get_cocktail(cocktail_id)
        if not cocktail:
            return 0.0

        total_alcohol = 0.0
        total_volume = 0.0

        for ing_id, amount in cocktail.ingredients.items():
            ingredient = self.get_ingredient(ing_id)
            if ingredient and ingredient.type == 'alcohol':
                total_alcohol += amount * (ingredient.strength / 100)
            total_volume += amount

        return (total_alcohol / total_volume) * 100 if total_volume > 0 else 0.0

    def sell_cocktail(self, cocktail_id: int, amount: int = 1) -> bool:
        cocktail = self.get_cocktail(cocktail_id)
        if not cocktail:
            return False

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for ing_id, ing_amount in cocktail.ingredients.items():
            cursor.execute('SELECT quantity FROM ingredients WHERE id = ?', (ing_id,))
            row = cursor.fetchone()
            if not row or row[0] < ing_amount * amount:
                conn.close()
                return False

        for ing_id, ing_amount in cocktail.ingredients.items():
            cursor.execute('''
                UPDATE ingredients 
                SET quantity = quantity - ? 
                WHERE id = ?
            ''', (ing_amount * amount, ing_id))

        total_price = cocktail.price * amount
        cursor.execute('''
            INSERT INTO operations (type, item_type, item_id, amount, total_price)
            VALUES ('sale', 'cocktail', ?, ?, ?)
        ''', (cocktail_id, amount, total_price))

        # Обновляем выручку
        cursor.execute('''
            INSERT OR IGNORE INTO revenue (date, total_sales, total_restocks)
            VALUES (DATE('now'), 0, 0)
        ''')
        cursor.execute('''
            UPDATE revenue 
            SET total_sales = total_sales + ?
            WHERE date = DATE('now')
        ''', (total_price,))

        conn.commit()
        conn.close()
        return True

    def sell_ingredient(self, ingredient_id: int, amount: float) -> bool:
        ingredient = self.get_ingredient(ingredient_id)
        if not ingredient or ingredient.quantity < amount:
            return False

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE ingredients 
            SET quantity = quantity - ? 
            WHERE id = ?
        ''', (amount, ingredient_id))

        total_price = (amount / ingredient.volume) * ingredient.price
        cursor.execute('''
            INSERT INTO operations (type, item_type, item_id, amount, total_price)
            VALUES ('sale', 'ingredient', ?, ?, ?)
        ''', (ingredient_id, amount, total_price))

        # Обновляем выручку
        cursor.execute('''
            INSERT OR IGNORE INTO revenue (date, total_sales, total_restocks)
            VALUES (DATE('now'), 0, 0)
        ''')
        cursor.execute('''
            UPDATE revenue 
            SET total_sales = total_sales + ?
            WHERE date = DATE('now')
        ''', (total_price,))

        conn.commit()
        conn.close()
        return True

    def restock_ingredient(self, ingredient_id: int, amount: float) -> bool:
        ingredient = self.get_ingredient(ingredient_id)
        if not ingredient:
            return False

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE ingredients 
            SET quantity = quantity + ? 
            WHERE id = ?
        ''', (amount, ingredient_id))

        total_price = (amount / ingredient.volume) * ingredient.price
        cursor.execute('''
            INSERT INTO operations (type, item_type, item_id, amount, total_price)
            VALUES ('restock', 'ingredient', ?, ?, ?)
        ''', (ingredient_id, amount, total_price))

        # Обновляем выручку
        cursor.execute('''
            INSERT OR IGNORE INTO revenue (date, total_sales, total_restocks)
            VALUES (DATE('now'), 0, 0)
        ''')
        cursor.execute('''
            UPDATE revenue 
            SET total_restocks = total_restocks + ?
            WHERE date = DATE('now')
        ''', (total_price,))

        conn.commit()
        conn.close()
        return True

    def get_revenue(self, days: int = 7) -> List[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, total_sales, total_restocks, 
                   (total_sales - total_restocks) as profit
            FROM revenue
            ORDER BY date DESC
            LIMIT ?
        ''', (days,))

        result = []
        for row in cursor.fetchall():
            result.append({
                'date': row[0],
                'sales': row[1],
                'restocks': row[2],
                'profit': row[3]
            })

        conn.close()
        return result


def print_ingredient(ingredient: Ingredient):
    print(f"ID: {ingredient.id}")
    print(f"Название: {ingredient.name}")
    print(f"Тип: {'Алкогольный' if ingredient.type == 'alcohol' else 'Безалкогольный'}")
    if ingredient.type == 'alcohol':
        print(f"Крепость: {ingredient.strength}%")
    print(f"Объем: {ingredient.volume} мл")
    print(f"Цена: {ingredient.price:.2f} руб.")
    print(f"Количество на складе: {ingredient.quantity:.2f} мл")
    print()


def print_cocktail(cocktail: Cocktail, manager: BarManager):
    strength = manager.calculate_cocktail_strength(cocktail.id)
    print(f"ID: {cocktail.id}")
    print(f"Название: {cocktail.name}")
    print(f"Крепость: {strength:.1f}%")
    print("Состав:")
    for ing_id, amount in cocktail.ingredients.items():
        ingredient = manager.get_ingredient(ing_id)
        if ingredient:
            print(f"  - {ingredient.name}: {amount} мл")
    print(f"Цена: {cocktail.price:.2f} руб.")
    print()


def print_revenue(revenue_data: List[Dict]):
    print("\nОтчёт о выручке:")
    print("{:<12} {:<12} {:<12} {:<12}".format("Дата", "Продажи", "Закупки", "Прибыль"))
    print("-" * 50)
    for day in revenue_data:
        print("{:<12} {:<12.2f} {:<12.2f} {:<12.2f}".format(
            day['date'], day['sales'], day['restocks'], day['profit']
        ))
    print()


def is_float(value: str) -> bool:
    if value.replace('.', '', 1).isdigit():
        return True
    return False


def input_float(prompt: str) -> float:
    while True:
        value = input(prompt)
        if is_float(value):
            return float(value)
        print("Пожалуйста, введите число")


def input_int(prompt: str) -> int:
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        print("Пожалуйста, введите целое число")


def input_ingredient() -> Ingredient:
    print("\nДобавление нового ингредиента:")
    name = input("Название: ")

    while True:
        type_ = input("Тип (alcohol/non-alcohol): ").lower()
        if type_ in ('alcohol', 'non-alcohol'):
            break
        print("Неверный тип. Введите 'alcohol' или 'non-alcohol'")

    strength = 0.0
    if type_ == 'alcohol':
        while True:
            strength = input_float("Крепость (%): ")
            if 0 <= strength <= 100:
                break
            print("Крепость должна быть от 0 до 100")

    volume = 0.0
    while True:
        volume = input_float("Объем (мл): ")
        if volume > 0:
            break
        print("Объем должен быть положительным")

    price = 0.0
    while True:
        price = input_float("Цена (руб): ")
        if price >= 0:
            break
        print("Цена не может быть отрицательной")

    quantity = 0.0
    while True:
        quantity = input_float("Количество на складе (мл): ")
        if quantity >= 0:
            break
        print("Количество не может быть отрицательным")

    return Ingredient(
        id=0,
        name=name,
        type=type_,
        strength=strength,
        volume=volume,
        price=price,
        quantity=quantity
    )


def input_cocktail(manager: BarManager) -> Cocktail:
    print("\nДобавление нового коктейля:")
    name = input("Название: ")

    ingredients = {}
    print("\nДоступные ингредиенты:")
    for ing in manager.get_all_ingredients():
        print(f"{ing.id}: {ing.name} ({ing.type}, {ing.strength}%, {ing.quantity:.2f} мл в наличии)")

    while True:
        ing_id = input_int("Введите ID ингредиента (0 для завершения): ")
        if ing_id == 0:
            if not ingredients:
                print("Коктейль должен содержать хотя бы один ингредиент")
                continue
            break

        if ing_id in ingredients:
            print("Этот ингредиент уже добавлен")
            continue

        ingredient = manager.get_ingredient(ing_id)
        if not ingredient:
            print("Ингредиент не найден")
            continue

        amount = input_float(f"Количество {ingredient.name} (мл): ")
        if amount <= 0:
            print("Количество должно быть положительным")
            continue

        ingredients[ing_id] = amount

    price = 0.0
    while True:
        price = input_float("Цена коктейля (руб): ")
        if price >= 0:
            break
        print("Цена не может быть отрицательной")

    return Cocktail(
        id=0,
        name=name,
        ingredients=ingredients,
        price=price
    )


def main():
    manager = BarManager()

    while True:
        print("\n=== I Love Drink ===")
        print("1. Учет напитков")
        print("2. Управление коктейлями")
        print("3. Операции")
        print("4. Просмотр выручки")
        print("0. Выход")

        main_choice = input("Выберите раздел: ")

        if main_choice == '1':
            while True:
                print("\nУчет напитков:")
                print("1. Добавить ингредиент")
                print("2. Просмотреть все ингредиенты")
                print("3. Просмотреть один ингредиент")
                print("4. Редактировать ингредиент")
                print("0. Назад")

                choice = input("Выберите действие: ")

                if choice == '1':
                    ingredient = input_ingredient()
                    ing_id = manager.add_ingredient(ingredient)
                    print(f"Ингредиент добавлен с ID {ing_id}")

                elif choice == '2':
                    print("\nСписок всех ингредиентов:")
                    for ing in manager.get_all_ingredients():
                        print_ingredient(ing)

                elif choice == '3':
                    ing_id = input_int("Введите ID ингредиента: ")
                    ingredient = manager.get_ingredient(ing_id)
                    if ingredient:
                        print_ingredient(ingredient)
                    else:
                        print("Ингредиент не найден")

                elif choice == '4':
                    ing_id = input_int("Введите ID ингредиента для редактирования: ")
                    ingredient = manager.get_ingredient(ing_id)
                    if not ingredient:
                        print("Ингредиент не найден")
                        continue

                    print("\nТекущие данные:")
                    print_ingredient(ingredient)

                    print("\nВведите новые данные (оставьте пустым для сохранения текущего значения):")
                    name = input(f"Название [{ingredient.name}]: ") or ingredient.name

                    type_ = ingredient.type
                    change_type = input(f"Изменить тип? (y/n) [{type_}]: ").lower() == 'y'
                    if change_type:
                        while True:
                            new_type = input("Тип (alcohol/non-alcohol): ").lower()
                            if new_type in ('alcohol', 'non-alcohol'):
                                type_ = new_type
                                break
                            print("Неверный тип. Введите 'alcohol' или 'non-alcohol'")

                    strength = ingredient.strength
                    if type_ == 'alcohol':
                        change_strength = input(f"Изменить крепость? (y/n) [{strength}]: ").lower() == 'y'
                        if change_strength:
                            while True:
                                strength = input_float("Крепость (%): ")
                                if 0 <= strength <= 100:
                                    break
                                print("Крепость должна быть от 0 до 100")

                    volume_str = input(f"Объем (мл) [{ingredient.volume}]: ")
                    volume = float(volume_str) if volume_str else ingredient.volume

                    price_str = input(f"Цена (руб) [{ingredient.price}]: ")
                    price = float(price_str) if price_str else ingredient.price

                    quantity_str = input(f"Количество (мл) [{ingredient.quantity}]: ")
                    quantity = float(quantity_str) if quantity_str else ingredient.quantity

                    updated_ingredient = Ingredient(
                        id=ing_id,
                        name=name,
                        type=type_,
                        strength=strength,
                        volume=volume,
                        price=price,
                        quantity=quantity
                    )

                    if manager.update_ingredient(updated_ingredient):
                        print("Ингредиент успешно обновлен")
                    else:
                        print("Ошибка при обновлении ингредиента")

                elif choice == '0':
                    break

                else:
                    print("Некорректный выбор")

        elif main_choice == '2':
            while True:
                print("\nУправление коктейлями:")
                print("1. Добавить коктейль")
                print("2. Просмотреть все коктейли")
                print("3. Просмотреть один коктейль")
                print("0. Назад")

                choice = input("Выберите действие: ")

                if choice == '1':
                    if not manager.get_all_ingredients():
                        print("Сначала добавьте ингредиенты")
                        continue

                    cocktail = input_cocktail(manager)
                    cocktail_id = manager.add_cocktail(cocktail)
                    print(f"Коктейль добавлен с ID {cocktail_id}")

                elif choice == '2':
                    print("\nСписок всех коктейлей:")
                    for cocktail in manager.get_all_cocktails():
                        print_cocktail(cocktail, manager)

                elif choice == '3':
                    cocktail_id = input_int("Введите ID коктейля: ")
                    cocktail = manager.get_cocktail(cocktail_id)
                    if cocktail:
                        print_cocktail(cocktail, manager)
                    else:
                        print("Коктейль не найден")

                elif choice == '0':
                    break

                else:
                    print("Некорректный выбор")

        elif main_choice == '3':
            while True:
                print("\nОперации:")
                print("1. Продажа коктейля")
                print("2. Продажа ингредиента")
                print("3. Пополнение запасов")
                print("0. Назад")

                choice = input("Выберите действие: ")

                if choice == '1':
                    print("\nДоступные коктейли:")
                    for cocktail in manager.get_all_cocktails():
                        print(f"{cocktail.id}: {cocktail.name}")

                    cocktail_id = input_int("Введите ID коктейля: ")
                    amount = input_int("Количество: ")

                    if manager.sell_cocktail(cocktail_id, amount):
                        print("Продажа успешно оформлена")
                    else:
                        print("Ошибка: недостаточно ингредиентов или коктейль не найден")

                elif choice == '2':
                    print("\nДоступные ингредиенты:")
                    for ing in manager.get_all_ingredients():
                        print(f"{ing.id}: {ing.name} ({ing.quantity:.2f} мл в наличии)")

                    ing_id = input_int("Введите ID ингредиента (Введите 0 для отмены: ")
                    if ing_id == 0:
                        break
                    amount = input_float("Количество (мл): ")

                    if manager.sell_ingredient(ing_id, amount):
                        print("Продажа успешно оформлена")
                    else:
                        print("Ошибка: недостаточно ингредиента или он не найден")


                elif choice == '3':
                    print("\nДоступные ингредиенты:")
                    for ing in manager.get_all_ingredients():
                        print(f"{ing.id}: {ing.name} ({ing.quantity:.2f} мл в наличии)")

                    ing_id = input_int("Введите ID ингредиента: ")
                    amount = input_float("Количество (мл): ")

                    if manager.restock_ingredient(ing_id, amount):
                        print("Запас успешно пополнен")
                    else:
                        print("Ошибка: ингредиент не найден")

                elif choice == '0':
                    break

                else:
                    print("Некорректный выбор")

        elif main_choice == '4':
            days = input_int("За сколько дней показать выручку (по умолчанию 7): ") or 7
            revenue_data = manager.get_revenue(days)
            print_revenue(revenue_data)
            input("Нажмите Enter")

        elif main_choice == '0':
            print("Выход из программы")
            break

        else:
            print("Некорректный выбор")


if __name__ == "__main__":
    main()