import sqlite3
import psutil
from datetime import datetime
import time

def init_db():
    conn = sqlite3.connect('system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS monitor_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME,
                  cpu_load REAL,
                  memory_used REAL,
                  disk_usage REAL)''')
    conn.commit()
    conn.close()

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('/').percent

def save_to_db(cpu, memory, disk):
    conn = sqlite3.connect('system.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    c.execute('INSERT INTO monitor_data (timestamp, cpu_load, memory_used, disk_usage) VALUES (?, ?, ?, ?)',
              (timestamp, cpu, memory, disk))
    conn.commit()
    conn.close()

def view_history():
    conn = sqlite3.connect('system.db')
    c = conn.cursor()
    c.execute('SELECT * FROM monitor_data ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print("Нет доступных данных.")
        return
    
    print("\nИстория мониторинга:")
    for row in rows:
        print(f"Время: {row[1]}, CPU: {row[2]}%, Память: {row[3]}%, Диск: {row[4]}%")

def main():
    init_db()
    while True:
        print("\nМеню системного монитора:")
        print("1. Начать мониторинг")
        print("2. Просмотреть историю")
        print("3. Выход")
        choice = input("Выберите действие: ")
        
        if choice == '1':
            try:
                duration = int(input("Длительность мониторинга (сек): "))
                interval = int(input("Интервал сбора данных (сек): "))
                print("Мониторинг запущен")
                start_time = time.time()
                end_time = start_time + duration
                while time.time() < end_time:
                    cpu = get_cpu_usage()
                    memory = get_memory_usage()
                    disk = get_disk_usage()
                    save_to_db(cpu, memory, disk)
                    sleep_time = interval - (time.time() - start_time) % interval
                    time.sleep(max(sleep_time, 0))
            except KeyboardInterrupt:
                print("\nМониторинг прерван пользователем.")
            except ValueError:
                print("Ошибка: введите число.")
        elif choice == '2':
            view_history()
        elif choice == '3':
            print("Завершение работы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()