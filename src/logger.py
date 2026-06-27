import time

# Constantes de colores
JP_RESET_ALL = "\033[0m"
JP_RED = '\033[91m'
JP_GREEN = "\033[32m"
JP_YELLOW = '\033[93m'
JP_BLUE = '\033[94m'

class logger_class():

    def __init__(self, function):
        self.function = function
        self.start_time = time.time()
        self.last_log_time = self.start_time

    def info(self, mensaje):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        elapsed_time = time.time() - self.start_time
        print(f"{JP_BLUE}[{current_time}] [INFO] [{self.function}] [{elapsed_time:.2f} segundos] {mensaje}{JP_RESET_ALL}")

    def success(self, mensaje):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        elapsed_time = time.time() - self.start_time
        print(f"{JP_GREEN}[{current_time}] [SUCCESS] [{self.function}] [{elapsed_time:.2f} segundos] {mensaje}{JP_RESET_ALL}")

    def percentage(self, i, N, mensaje = ""):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        elapsed_time = time.time() - self.start_time
        if i % max(1, N // 20) == 0 or elapsed_time - (self.last_log_time - self.start_time) >= 5 or i == N:
            percentage_completed = round((i / N) * 100, 2)
            print(f"{JP_BLUE}[{current_time}] [INFO] [{self.function}] [{elapsed_time:.2f} segundos] {mensaje}{JP_YELLOW}{percentage_completed}%{JP_RESET_ALL}")
            self.last_log_time = time.time()

    def error(self, error):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        elapsed_time = time.time() - self.start_time
        print(f"{JP_RED}[{current_time}] [ERROR] [{self.function}] [{elapsed_time:.2f} segundos] {error}{JP_RESET_ALL}")

    def warning(self, mensaje):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        elapsed_time = time.time() - self.start_time
        print(f"{JP_YELLOW}[{current_time}] [WARNING] [{self.function}] [{elapsed_time:.2f} segundos] {mensaje}{JP_RESET_ALL}")
