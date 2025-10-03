class Dog():
    def __init__(self,name,age):
        self.name = name
        self.age = age
        fullness = "hungry"
    
    def describe(self):
        print(f"this is my dog,named {self.name},aged {self.age},she's {fullness}")

    def feed(self):
        fullness = "full"
        print("now you feed the dog ,he's full!")

ceobe = Dog("ceobe",3)
ceobe.describe()
ceobe.feed()
ceobe.describe()