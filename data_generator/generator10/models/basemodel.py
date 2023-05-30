from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def print_data(self):
        pass

    @abstractmethod
    def get_row(self):
        pass

    @staticmethod
    @abstractmethod
    def get_csv_filename():
        pass

    @staticmethod
    @abstractmethod
    def get_csv_header():
        pass

def check_model_implementation(model_cls):
    if issubclass(model_cls, BaseModel):
        if not hasattr(model_cls, 'print_data') or not callable(model_cls.print_data):
            raise NotImplementedError(f"{model_cls.__name__} must implement 'print_data' method.")
        if not hasattr(model_cls, 'get_row') or not callable(model_cls.get_row):
            raise NotImplementedError(f"{model_cls.__name__} must implement 'get_row' method.")
        if not hasattr(model_cls, 'get_csv_filename') or not callable(model_cls.get_csv_filename):
            raise NotImplementedError(f"{model_cls.__name__} must implement 'get_csv_filename' method.")
        if not hasattr(model_cls, 'get_csv_header') or not callable(model_cls.get_csv_header):
            raise NotImplementedError(f"{model_cls.__name__} must implement 'get_csv_header' method.")
    else:
        raise TypeError(f"{model_cls.__name__} must inherit from BaseModel.")
