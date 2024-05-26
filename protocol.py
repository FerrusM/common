import enum


class Commands(enum.Enum):
    ADD_TOKEN = 1


class ClientRequest:
    """Запрос клиента."""
    def __init__(self, command: Commands, data=None):
        self.command: Commands = command
        self.data = data


class ServerResponse:
    """Ответ сервера."""
    def __init__(self, command: Commands, flag: bool, data=None):
        self.command: Commands = command
        self.flag: bool = flag
        self.data = data
