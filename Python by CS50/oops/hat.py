import random

class Hat:
    houses = ["Gryffindor","Hufflepuf","Ravenclaw","Slytherin"]

    @classmethod
    def sort(cls,name):
        print(name, "is in", random.choice(cls.houses))




Hat.sort("Harry")