import abc
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class TsInterface(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def load() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def process(json_input: str) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def validate() -> str:
        pass

    @staticmethod
    def get_validation_output_schema():
        return TsInterface._get_schema('validation_output_schema')

    @staticmethod
    def get_load_output_schema():
        return TsInterface._get_schema('load_output_schema')

    @staticmethod
    def get_process_input_schema():
        return TsInterface._get_schema('process_input_schema')

    @staticmethod
    def get_process_output_schema():
        return TsInterface._get_schema('process_output_schema')

    @staticmethod
    def _get_schema(name: str):
        with open(os.path.join(BASE_DIR, 'schema', name + '.json')) as schema:
            schema = json.load(schema)
        return schema

    @staticmethod
    def get_schemas():
        schema_dir = os.path.join(BASE_DIR, 'schema')
        return [os.path.join(schema_dir, p) for p in os.listdir(schema_dir)]


if __name__ == '__main__':
    print(TsInterface.validation_output_schema())
