import os
import subprocess
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class RestartHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        # Mata o processo atual, se estiver rodando
        if self.process:
            try:
                os.kill(self.process.pid, signal.SIGTERM)
            except Exception as e:
                print(f"Erro ao finalizar processo: {e}")

        # Inicia um novo processo
        self.process = subprocess.Popen(self.command, shell=True)

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Alteração detectada em {event.src_path}. Reiniciando...")
            self.start_process()

    def on_created(self, event):
        if event.src_path.endswith(".py"):
            print(f"Novo arquivo detectado {event.src_path}. Reiniciando...")
            self.start_process()


def main():
    path = os.getcwd()  # Diretório atual
    command = "poetry run python login.py"  # Comando para rodar o app

    event_handler = RestartHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print(f"Monitorando alterações em {path}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            os.kill(event_handler.process.pid, signal.SIGTERM)
    observer.join()


if __name__ == "__main__":
    main()
