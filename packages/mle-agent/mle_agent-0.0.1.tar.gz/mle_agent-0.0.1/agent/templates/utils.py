import os
import yaml
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError

from agent.types import Step

T = TypeVar('T', bound=BaseModel)


def load_step(file_name: str) -> Step:
    """
    Load a step from a .yaml file.
    :param file_name: the name of the configuration file.
    :return:
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    yml_path = os.path.join(dir_path, file_name)

    with open(yml_path, 'r') as file:
        data = yaml.safe_load(file)
    try:
        config = Step(**data)
        return config
    except ValidationError as e:
        print(f"Error in loading step file: {e}")
        raise


def get_step_mapping(step_num: int):
    """
    Get the step mapping based on the step number.
    :param step_num: the step number.
    :return: the step mapping.
    """
    step_mapping = {
        0: 'data_collection.yml',
        1: 'data_engineering.yml',
        2: 'model_selection.yml',
        3: 'model_training.yml',
        4: 'model_evaluation.yml',
        5: 'model_deployment.yml'
    }

    return step_mapping.get(step_num, None)


def load_yml_to_pydantic_model(file_path: str, model: Type[T]) -> T:
    """
    Loads YAML data from a file and converts it into a Pydantic model.

    Args:
    file_path (str): Path to the YAML file.
    model (Type[T]): The Pydantic model class to which the data should be converted.

    Returns:
    T: An instance of the specified Pydantic model class.
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return model(**data)