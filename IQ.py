from concurrent.futures import ThreadPoolExecutor, as_completed
import time
'''Модуль concurrent.futures предоставляет высокоуровневый интерфейс для асинхронного выполнения вызываемых объектов (программирования), 
включая поддержку многопоточности и многопроцессорности.'''

class ProcessController:
    def __init__(self):
        '''В конструкторе (__init__) инициализируется пул потоков, очередь будущих результатов и максимальное кол-во заданий'''
        self.executor = ThreadPoolExecutor()
        self.future_queue = []
        self.max_procs = None

    def set_max_proc(self, n):
        '''Функция set_max_proc дает максимальное кол-во заданий, которые могут быть запущены одновременно'''
        self.max_procs = n

    def start(self, tasks, max_exec_time):
        '''Функция start добавляет задания в очередь и запускает их выполнение до достижения максимального количества заданий в очереди.
        Каждое задание выполняется в отдельном потоке, и после его завершения проверяется таймаут max_exec_time.'''
        self.future_queue.extend([self.executor.submit(func, *args) for func, args in tasks])
        while len(self.future_queue) > self.max_procs and self.future_queue:
            future_to_remove = self.future_queue.pop(0)
            try:
                result = future_to_remove.result(timeout=max_exec_time)
            except Exception as e:
                print(f"Задача не выполнена с исключением {e}. Задача не выполнена.")
            else:
                print(f"Задача успешно завершена с результатом {result}")

    def wait(self):
        '''Метод wait ожидает завершения всех заданий, вызывая .result() для каждого будущего результата в очереди.'''
        while self.future_queue:
            future = self.future_queue.pop(0)
            try:
                result = future.result()
            except Exception as e:
                print(f"Задача не выполнена с исключением {e}. Задача не выполнена.")
            else:
                print(f"Задача успешно завершена с результатом {result}")

    def wait_count(self):
        '''Метод wait_count возвращает количество оставшихся заданий, которые еще должны быть запущены.'''
        return len(self.future_queue)

    def alive_count(self):
        '''Метод alive_count возвращает текущее количество активно выполняющихся заданий, используя as_completed.'''
        return len(list(as_completed(self.future_queue)))

# Пример использования класса ProcessController
# Пусть нам нужно узнать сколько ученик выполнил задач по математике. В качестве номера задачи будет выступать переменная task_id

def task_function(task_id):
    print(f"Выполнение задачи {task_id}")
    time.sleep(1)
    return f"Задача {task_id} выполнена!"

# Создание экземпляра ProcessController.
controller = ProcessController()

# Установка максимального количества задач
controller.set_max_proc(2)

# Определить список задач, которые необходимо выполнить
tasks = [(task_function, (1, )), (task_function, (2, )), (task_function, (3, ))]

# Приступить к выполнению задач
controller.start(tasks, 3) # (tasks, max_exec_time). Переменная max_exec_time берется на усмотрение

# Дождитесь завершения всех задач
controller.wait()

# Получить количество оставшихся задач
remaining_tasks = controller.wait_count()
print(f"Оставшиеся задачи: {remaining_tasks}")

# Получить количество выполняемых в данный момент задач
executing_tasks = controller.alive_count()
print(f"Выполнение задач: {executing_tasks}")

'''Этот подход позволяет эффективно управлять параллельным выполнением заданий с использованием пула потоков, 
обеспечивая ограничение на количество одновременно выполняемых заданий и возможность контролировать выполнение заданий через таймауты.'''