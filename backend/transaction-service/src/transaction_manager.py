# transaction_manager.py
# Singleton, Memento, and Command patterns for atomic transactions using user and course services
from commands import Command

class TransactionMemento:
    def __init__(self, commands):
        self.commands = list(commands)

class TransactionManager:
    _instance = None

    def __init__(self):
        if TransactionManager._instance is not None:
            raise Exception("This class is a singleton!")
        self._commands = []
        TransactionManager._instance = self

    @staticmethod
    def get_instance():
        if TransactionManager._instance is None:
            TransactionManager()
        return TransactionManager._instance

    def begin(self):
        self._commands = []

    def execute(self, command: Command):
        command.execute()
        self._commands.append(command)

    def commit(self):
        self._commands = []

    def rollback(self):
        for command in reversed(self._commands):
            command.undo()
        self._commands = []

    def save_state(self):
        return TransactionMemento(self._commands)

    def restore_state(self, memento: TransactionMemento):
        self._commands = list(memento.commands)
