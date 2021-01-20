import random

from transformations.Transformations import TransformationsList

if __name__ == '__main__':
    random.seed(0)
    transformationsList = TransformationsList()
    generations = transformationsList.generate("Andrew finally returned the French book to Chris that I bought last week")