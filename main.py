import random

from Transformations import TransformationsList

if __name__ == '__main__':
    random.seed(0)
    transformationsList = TransformationsList()
    generations = transformationsList.generate("Andrew finally returned the French book to Chris that "
                                               "I bought last week")
    generations = transformationsList.generate("My sister has a dog. She loves him. Being a firefighter, "
                                               "she often uses that dog at work.")
