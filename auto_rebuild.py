import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time


class RestartHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen(self.command, shell=True)

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}. Restarting...")
            self.start_process()

    def on_created(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected new file {event.src_path}. Restarting...")
            self.start_process()


def main():
    path = os.getcwd()  # Monitora o diretório atual
    command = "python frontappposto/login.py"  # Comando para rodar a aplicação

    event_handler = RestartHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print(f"Watching for changes in {path}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
