import sqlite3
from typing import List, Dict, Optional
from datetime import datetime


class SystemMetric:
    def __init__(self, id: int, timestamp: datetime, cpu_percent: float,
                 memory_percent: float, disk_percent: float):
        self.id = id
        self.timestamp = timestamp
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent
        self.disk_percent = disk_percent


class SystemMonitor:
    def __init__(self, db_name: str = 'system_monitor.db'):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        #Инициализация
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                cpu_percent REAL NOT NULL,
                memory_percent REAL NOT NULL,
                disk_percent REAL NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT NOT NULL CHECK(metric_type IN ('cpu', 'memory', 'disk')),
                threshold REAL NOT NULL,
                message TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id INTEGER,
                metric_value REAL NOT NULL,
                timestamp DATETIME NOT NULL,
                FOREIGN KEY (alert_id) REFERENCES alerts(id)
            )
        ''')

        conn.commit()
        conn.close()

    def save_current_metrics(self) -> int:
        #Сохранение текущих метрик системы
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO system_metrics (timestamp, cpu_percent, memory_percent, disk_percent)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, cpu, memory, disk))

        metric_id = cursor.lastrowid
        conn.commit()
        conn.close()

        #Проверка на срабатывание алертов
        self._check_alerts(cpu, memory, disk, timestamp)

        return metric_id

    def _check_alerts(self, cpu: float, memory: float, disk: float, timestamp: str):
        #Проверка метрик
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alerts WHERE is_active = 1')
        alerts = cursor.fetchall()

        for alert in alerts:
            alert_id, metric_type, threshold, message, _ = alert
            value = None

            if metric_type == 'cpu':
                value = cpu
            elif metric_type == 'memory':
                value = memory
            elif metric_type == 'disk':
                value = disk

            if value and value >= threshold:
                cursor.execute('''
                    INSERT INTO alert_history (alert_id, metric_value, timestamp)
                    VALUES (?, ?, ?)
                ''', (alert_id, value, timestamp))
                print(f"ALERT: {message} (Current: {value}%, Threshold: {threshold}%)")

        conn.commit()
        conn.close()

    def get_metrics(self, hours: int = 24) -> List[SystemMetric]:
        #Получение метрик за последние часы
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, timestamp, cpu_percent, memory_percent, disk_percent
            FROM system_metrics
            WHERE timestamp >= datetime('now', ?)
            ORDER BY timestamp DESC
        ''', (f'-{hours} hours',))

        metrics = []
        for row in cursor.fetchall():
            metrics.append(SystemMetric(
                id=row[0],
                timestamp=datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'),
                cpu_percent=row[2],
                memory_percent=row[3],
                disk_percent=row[4]
            ))

        conn.close()
        return metrics

    def add_alert(self, metric_type: str, threshold: float, message: str) -> int:
        #Добавление нового алерта
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO alerts (metric_type, threshold, message)
            VALUES (?, ?, ?)
        ''', (metric_type, threshold, message))

        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return alert_id

    def get_active_alerts(self) -> List[Dict]:
        #Получение активных алертов
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM alerts WHERE is_active = 1')
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'id': row[0],
                'metric_type': row[1],
                'threshold': row[2],
                'message': row[3]
            })

        conn.close()
        return alerts

    def get_alert_history(self, hours: int = 24) -> List[Dict]:
        #Получение истории алертов
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT ah.id, a.metric_type, a.threshold, a.message, 
                   ah.metric_value, ah.timestamp
            FROM alert_history ah
            JOIN alerts a ON ah.alert_id = a.id
            WHERE ah.timestamp >= datetime('now', ?)
            ORDER BY ah.timestamp DESC
        ''', (f'-{hours} hours',))

        history = []
        for row in cursor.fetchall():
            history.append({
                'id': row[0],
                'metric_type': row[1],
                'threshold': row[2],
                'message': row[3],
                'value': row[4],
                'timestamp': row[5]
            })

        conn.close()
        return history

    def get_metric_stats(self, hours: int = 24) -> Dict:
        #Получение статистики
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        stats = {}

        # CPU
        cursor.execute('''
            SELECT AVG(cpu_percent), MAX(cpu_percent), MIN(cpu_percent)
            FROM system_metrics
            WHERE timestamp >= datetime('now', ?)
        ''', (f'-{hours} hours',))
        cpu_stats = cursor.fetchone()
        stats['cpu'] = {
            'avg': cpu_stats[0],
            'max': cpu_stats[1],
            'min': cpu_stats[2]
        }

        # Memory
        cursor.execute('''
            SELECT AVG(memory_percent), MAX(memory_percent), MIN(memory_percent)
            FROM system_metrics
            WHERE timestamp >= datetime('now', ?)
        ''', (f'-{hours} hours',))
        memory_stats = cursor.fetchone()
        stats['memory'] = {
            'avg': memory_stats[0],
            'max': memory_stats[1],
            'min': memory_stats[2]
        }

        # Disk статистика
        cursor.execute('''
            SELECT AVG(disk_percent), MAX(disk_percent), MIN(disk_percent)
            FROM system_metrics
            WHERE timestamp >= datetime('now', ?)
        ''', (f'-{hours} hours',))
        disk_stats = cursor.fetchone()
        stats['disk'] = {
            'avg': disk_stats[0],
            'max': disk_stats[1],
            'min': disk_stats[2]
        }

        conn.close()
        return stats


def print_metric(metric: SystemMetric):
    """Вывод информации о метрике"""
    print(f"[{metric.timestamp}] CPU: {metric.cpu_percent:.1f}%, "
          f"Memory: {metric.memory_percent:.1f}%, "
          f"Disk: {metric.disk_percent:.1f}%")


def print_alert_history(history: List[Dict]):
    """Вывод истории алертов"""
    print("\nИстория алертов:")
    print("{:<25} {:<10} {:<10} {:<10} {:<40}".format(
        "Время", "Метрика", "Значение", "Порог", "Сообщение"))
    print("-" * 95)
    for alert in history:
        print("{:<25} {:<10} {:<10.1f} {:<10.1f} {:<40}".format(
            alert['timestamp'],
            alert['metric_type'],
            alert['value'],
            alert['threshold'],
            alert['message']
        ))


def print_metric_stats(stats: Dict):
    """Вывод статистики по метрикам"""
    print("\nСтатистика за последние 24 часа:")
    print("{:<10} {:<10} {:<10} {:<10}".format("Метрика", "Среднее", "Максимум", "Минимум"))
    print("-" * 40)
    for metric, values in stats.items():
        print("{:<10} {:<10.1f} {:<10.1f} {:<10.1f}".format(
            metric.upper(),
            values['avg'],
            values['max'],
            values['min']
        ))


def main():
    monitor = SystemMonitor()

    while True:
        print("\n=== Системный монитор ===")
        print("1. Сохранить текущие метрики")
        print("2. Просмотреть историю метрик")
        print("3. Управление алертами")
        print("4. Просмотреть статистику")
        print("5. Просмотреть историю алертов")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            metric_id = monitor.save_current_metrics()
            print(f"Метрики сохранены (ID: {metric_id})")

        elif choice == '2':
            hours = input("За сколько часов показать историю (по умолчанию 24): ") or 24
            try:
                hours = int(hours)
                metrics = monitor.get_metrics(hours)
                print(f"\nПоследние метрики (за {hours} часов):")
                for metric in metrics[:10]:  #только последние 10 записей
                    print_metric(metric)
                if len(metrics) > 10:
                    print(f"... и еще {len(metrics) - 10} записей")
            except ValueError:
                print("Некорректное количество часов")

        elif choice == '3':
            while True:
                print("\nУправление алертами:")
                print("1. Добавить алерт")
                print("2. Просмотреть активные алерты")
                print("0. Назад")

                sub_choice = input("Выберите действие: ")

                if sub_choice == '1':
                    print("\nДобавление нового алерта")
                    metric_type = input("Тип метрики (cpu/memory/disk): ").lower()
                    if metric_type not in ('cpu', 'memory', 'disk'):
                        print("Некорректный тип метрики")
                        continue

                    try:
                        threshold = float(input("Пороговое значение (%): "))
                        if not 0 <= threshold <= 100:
                            print("Значение должно быть от 0 до 100")
                            continue
                    except ValueError:
                        print("Некорректное значение")
                        continue

                    message = input("Сообщение алерта: ")
                    alert_id = monitor.add_alert(metric_type, threshold, message)
                    print(f"Алерт добавлен (ID: {alert_id})")

                elif sub_choice == '2':
                    alerts = monitor.get_active_alerts()
                    if not alerts:
                        print("Нет активных алертов")
                        continue

                    print("\nАктивные алерты:")
                    print("{:<5} {:<10} {:<10} {:<40}".format(
                        "ID", "Метрика", "Порог", "Сообщение"))
                    print("-" * 65)
                    for alert in alerts:
                        print("{:<5} {:<10} {:<10.1f} {:<40}".format(
                            alert['id'],
                            alert['metric_type'],
                            alert['threshold'],
                            alert['message']
                        ))

                elif sub_choice == '0':
                    break

                else:
                    print("Некорректный выбор")

        elif choice == '4':
            stats = monitor.get_metric_stats()
            print_metric_stats(stats)

        elif choice == '5':
            hours = input("За сколько часов показать историю (по умолчанию 24): ") or 24
            try:
                hours = int(hours)
                history = monitor.get_alert_history(hours)
                if history:
                    print_alert_history(history)
                else:
                    print("Нет записей в истории алертов")
            except ValueError:
                print("Некорректное количество часов")

        elif choice == '0':
            print("Выход из программы")
            break

        else:
            print("Некорректный выбор")


if __name__ == "__main__":
    import psutil
    main()