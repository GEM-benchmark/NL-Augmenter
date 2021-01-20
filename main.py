import random

from transformations.Transformations import TransformationsList

if __name__ == '__main__':
    random.seed(0)
    transformationsList = TransformationsList()
    generations = transformationsList.generate("Andrew returned the book that I bought last week, to Mary .")