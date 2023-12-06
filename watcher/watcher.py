from watchfiles import run_process
import logging
from pathlib import Path

class UnknownEventException(Exception):
    pass

def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] --%(asctime)s - (%(name)s): %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

class FileWatcher():
    FILE_ADDED = 1
    FILE_MODIFIED = 2
    FILE_DELETED = 3

    def __init__(self, paths, on_add=None, on_modify=None, on_delete=None, backup_dest=None) -> None:
        self.paths = paths
        self.backup_dest = backup_dest
        self.add = on_add
        self.modify = on_modify
        self.delete = on_delete
        self.logger = get_logger()

    def check_execute_method(self, method, file):
        if callable(method):
            method(file)
        else:
            self.logger.warning("Method pass is '%s' or not defined." % (method.__name__ if callable(method) else type(method).__name__))

    def callback(self, changes):
        for change in changes:
            path_to_file = change[1]        # path to file that have been changed
            file_event = change[0]          # type of event that occured. 1-added, 2-modified, 3-deleted
            self.logger.debug("File event occured in file at: %s" % path_to_file)
            self.logger.debug("Event type: %s" % file_event)

            if file_event == 1:
                self.logger.debug("Executing method for the add event...")
                self.check_execute_method(self.add, file=path_to_file)
            elif file_event == 2:
                self.logger.debug("Executing method for the modify event...")
                self.check_execute_method(self.modify, file=path_to_file)
            elif file_event == 3:
                self.logger.debug("Executing method for the delete event...")
                self.check_execute_method(self.delete, file=path_to_file)
            else:
                raise UnknownEventException("No known event occured.")


    def monitor_file_events(self):
        print(self.paths)
        run_process(Path(self.paths), target=None, callback=self.callback)


if __name__ == "__main__":
    def modify(file):
        print(file)
        print("modify function!!!")
    
    def add():
        print("add function!!!")

    def delete():
        print("delete function!!!")
    x = FileWatcher(paths=r"E:\Playstation\ePSXe", on_modify=modify, on_add=add, on_delete=delete)
    x.monitor_file_events()

