# Задание
1. Реализовать класс ProcessController на языке python, который организует очередь заданий и параллельное выполнение заданий из очереди. Данный класс должен содержать следующие методы:
- set_max_proc - аргумент: n. Метод устанавилвает ограничение: максимальное число одновременно выполняемых заданий не должно превышать n.
- start - аргументы: tasks, max_exec_time: 1. tasks - список заданий. Задание представляет кортеж вида: (функция, кортеж входных аргументов для функции). Пример: tasks = [(function0, (f0_arg0, f0_arg1)), (function1, (f1_arg0, f1_arg1, f1_arg2)), (function2, (f2_arg0, ))]. 2. max_exec_time - максимальное время (в секундах) работы каждого задания из списка tasks. Данный метод помещает в очередь все задания из tasks. В случае, если не достигнуто ограничение на максимальное число одновременно работающих заданий, метод запускает выполнение заданий из очереди до тех пор, пока не будет достигнуто это ограничение. Запуск задания представляет порождение нового процесса, который выполняет соответствующую функцию с ее аргументами. При этом каждый запущенный процесс для задания из tasks не должен работать дольше max_exec_time.
- wait - (без аргументов) ждать пока не завершат свое выполнение все задания из очереди.
- wait_count - (без аргументов) возвращает число заданий, которые осталось запустить.
- alive_count - (без аргументов) возвращает число выполняемых в данный момент заданий.
- Придумать пример, который продемонстрирует корректность реализации класса ProcessController.
- Написанный код на языке Python должен соответствовать соглашению PEP8.
# Комментарий

Этот репозиторий представляет собой два одинаковых кода: в формате IPYNB (Чтобы Вы могли прочитать ввод и вывод примера реализации класса ProcessController) и в формате .py. В данном примере я использую модуль `concurrent.futures`, 
который предоставляет высокоуровневый интерфейс для асинхронного программирования, 
включая поддержку многопоточности и многопроцессорности.
Далее я реализую класс и его методы по условию:
- В конструкторе `(__init__)` инициализируется пул процессоров, очередь будущих результатов и максимальное кол-во заданий.
- Метод `set_max_proc` дает максимальное кол-во заданий, которые могут быть запущены одновременно.
- Метод `start` добавляет задания в очередь и запускает их выполнение до достижения максимального количества заданий в очереди.
        Каждое задание выполняется в отдельном процессе, и после его завершения проверяется таймаут max_exec_time. Если время превышает max_exec_time, то программа завершит свою работу.
- Метод `wait` ожидает завершения всех заданий, вызывая .result() для каждого будущего результата в очереди.
- Метод `wait_count` возвращает количество оставшихся заданий, которые еще должны быть запущены.
- Метод `alive_count` возвращает текущее количество активно выполняющихся заданий, используя as_completed.
# Пример использования класса ProcessController
В качестве примера я привел легкую задачку. Пусть нужно узнать сколько ученик выполнил задач по математике. В качестве номера задачи будет выступать переменная `task_id`. 
Метод `task_function` используется для выполнение и результата задачи через параллельное программирование класса ProcessController с вычислением времени выполнения.
Далее я реализую пример по следующим шагам:
- Создание экземпляра ProcessController.
- Установка максимального количества задач.
- Определить список задач, которые необходимо выполнить.
- Приступить к выполнению задач.
- Ожидание завершения всех задач.
- Получить количество оставшихся задач.
- Получить количество выполняемых в данный момент задач.
# Вывод
Этот подход позволяет эффективно управлять параллельным выполнением заданий с использованием пула процессоров, 
обеспечивая ограничение на количество одновременно выполняемых заданий и возможность контролировать выполнение заданий через таймауты.
P.S. Надеюсь, Вам понравится :)
