from abc import ABC, abstractmethod

class Output(ABC):
    @abstractmethod
    def display_message(self, message):
        pass

    @abstractmethod
    def input(self, message):
        pass


class ConsoleOutput(Output):
    def display_message(self, message):
        print(message)

    def input(self, message):
        return input(message)