class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say(self):
        pass


class Cat(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)

    def say(self):
        print('МЯУ')

class Dog(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)

    def say(self):
        print('ГАВ')



a = Dog('Bobik', 3)
b = Dog('Дружок', 5)
cat = Cat('Вася', 9)
print(f'Кличка {a.name}, возраст (лет): {a.age}')
print(f'Кличка {b.name}, возраст (лет): {b.age}')
print(f'Кличка {cat.name}, возраст (лет): {cat.age}')
a.say()
cat.say()
