from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

from interfaces.SentenceTransformation import SentenceTransformation


def load(module, cls):
    my_class = getattr(module, cls.__name__)
    return my_class()


class TransformationsList:

    def __init__(self):
        transformations = []
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> Transformations.py
        for (_, m, _) in iter_modules([package_dir.parent.joinpath("transformations")]):
            t_py = import_module(f"transformations.{m}.transformation")
            transformations.extend([load(t_py, cls) for cls in SentenceTransformation.__subclasses__() if
                                    hasattr(t_py, cls.__name__)])
            self.transformations = transformations

    def generate(self, sentence: str):
        print(f"Original Input : {sentence}")
        generations = {"Original": sentence}
        for transformation in self.transformations:
            generations[transformation.name()] = transformation.generate(sentence)
        return generations
