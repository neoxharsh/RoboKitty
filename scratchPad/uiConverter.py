import sys,os,subprocess
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class FileEvent(FileSystemEventHandler):

    def on_modified(self, event:FileSystemEvent):
        if os.path.splitext(event.src_path)[1] == '.ui':
            print(event.src_path)
            subprocess.call(["pyuic5", event.src_path ,"-o",os.path.splitext(event.src_path)[0] +".py"])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileEvent()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()