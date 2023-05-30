import sys

from abc import ABC, abstractmethod


class Generator(ABC):
    @abstractmethod
    def generate(self):
        pass


class DataGenerator:
    generators = {}

    # Singletone Pattern 을 사용해서 객체는 한번만 생성
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass

    def register_generator(self, data_type, generator):
        self.generators[data_type] = generator

    def register_print(self):
        print(self.generators)

    # Factory Pattern 을 사용해서 여러 유형의 객체를 유형별로 생성
    def generate_data(self, data_type, num_records):
        if data_type not in self.generators:
            print(f"지원되지 않는 데이터 유형입니다. {data_type}")
            sys.exit(1)

        generator = self.generators[data_type]
        data = [generator.generate() for _ in range(num_records)]  

        return data


def register_generator(data_type):
    def decorator(generator_cls):
        data_gen = DataGenerator()
        data_gen.register_generator(data_type, generator_cls())
        return generator_cls
    return decorator
