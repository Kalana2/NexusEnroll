class CommandProcessor:
    def __init__(self):
        self.history = []

    def process(self, command):
        result = command.execute()
        self.history.append(command)
        return result
