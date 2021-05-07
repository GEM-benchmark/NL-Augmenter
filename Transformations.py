from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

from transformations.SentenceTransformation import SentenceTransformation


def load(module, class_name):
    my_class_py = getattr(module, class_name)
    my_class = getattr(my_class_py, class_name)
    return my_class()


class TransformationsList:

    def __init__(self):
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> Transformations.py
        for (_, m, _) in iter_modules([package_dir.parent.joinpath("transformations")]):
            import_module(f"transformations.{m}")

        module = __import__("transformations")
        transformations = [load(module, cls.__name__) for cls in SentenceTransformation.__subclasses__()]
        self.transformations = transformations

    def generate(self, sentence: str):
        print(f"Original Input : {sentence}")
        generations = {"Original": sentence}
        for transformation in self.transformations:
            generations[transformation.name()] = transformation.generate(sentence)
        return generations
