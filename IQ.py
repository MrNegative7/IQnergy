from concurrent.futures import ProcessPoolExecutor, as_completed, wait
import time
'''Модуль concurrent.futures предоставляет высокоуровневый интерфейс для асинхронного выполнения вызываемых объектов (программирования), 
включая поддержку многопоточности и многопроцессорности.'''

class ProcessController:
    def __init__(self):
        '''В конструкторе (__init__) инициализируется пул процессоров, очередь будущих результатов и максимальное кол-во заданий'''
        self.executor = ProcessPoolExecutor(max_workers=1) # Запускается один процесс (для каждого задания)
        self.future_queue = []
        self.max_procs = None

    def set_max_proc(self, n):
        '''Метод set_max_proc дает максимальное кол-во заданий, которые могут быть запущены одновременно'''
        self.max_procs = n

    def start(self, tasks, max_exec_time):
        '''Метод start добавляет задания в очередь и запускает их выполнение до достижения максимального количества заданий в очереди.
        Каждое задание выполняется в отдельном потоке, и после его завершения проверяется таймаут max_exec_time.'''
        self.future_queue.extend([self.executor.submit(func, *args) for func, args in tasks])
        start_time = time.perf_counter()
        while self.future_queue:
            future = self.future_queue.pop(0)
            try:
                result = future.result(timeout=max_exec_time)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
            else:
                print(f"Задача успешно завершена с результатом: {result}")
            elapsed_time = time.perf_counter() - start_time
            if elapsed_time >= max_exec_time:
                print("Превышено максимальное время выполнения")
                break

    def wait(self):
        '''Метод wait ожидает завершения всех заданий, вызывая .result() для каждого будущего результата в очереди.'''
        for future in as_completed(self.future_queue):
            try:
                result = future.result()
                print(f"Задача успешно завершена с результатом: {result}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        self.future_queue = []

    def wait_count(self):
        '''Метод wait_count возвращает количество оставшихся заданий, которые еще должны быть запущены.'''
        return len(self.future_queue)

    def alive_count(self):
        '''Метод alive_count возвращает текущее количество активно выполняющихся заданий, используя as_completed.'''
        return len(list(as_completed(self.future_queue)))

def task_function(task_id):
    print(f"Выполнение задачи {task_id}")
    start = time.perf_counter()
    time.sleep(1)
    all_time = time.perf_counter() - start
    return f"Задача {task_id} выполнена! Выполнение заняло {all_time: .2f} секунд."

if __name__ == '__main__':
    # Создание экземпляра ProcessController.
    controller = ProcessController()
    # Установка максимального количества задач
    controller.set_max_proc(5)
    # Определить список задач, которые необходимо выполнить
    tasks = [(task_function, (1,)), (task_function, (2,)), (task_function, (3,))]
    # Приступить к выполнению задач
    controller.start(tasks, 3)
    # Дождитесь завершения всех задач
    controller.wait()
    # Получить количество оставшихся задач
    remaining_tasks = controller.wait_count()
    print(f"Оставшиеся задачи: {remaining_tasks}")
    # Получить количество выполняемых в данный момент задач
    executing_tasks = controller.alive_count()
    print(f"Выполнение задач: {executing_tasks}")
