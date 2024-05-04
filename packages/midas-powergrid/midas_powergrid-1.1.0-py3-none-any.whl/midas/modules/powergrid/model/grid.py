from abc import ABC, abstractmethod


class PowerGrid(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def set_value(self, etype, idx, attr, val):
        raise NotImplementedError

    @abstractmethod
    def run_powerflow(self):
        raise NotImplementedError

    def get_state(self, etype, idx, attr):
        raise NotImplementedError

    @abstractmethod
    def get_outputs(self):
        raise NotImplementedError

    @abstractmethod
    def to_json(self):
        raise NotImplementedError
