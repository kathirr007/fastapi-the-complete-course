class MyClass:
    def __init__(self, value):
        self.__private_property = value

    def get_private_property(self):
        return self.__private_property

    def set_private_property(self, value):
        self.__private_property = value


# # Usage
# obj = MyClass(10)
# print(obj.get_private_property())  # Output: 10
# obj.set_private_property(20)
# print(obj.get_private_property())  # Output: 20

# Trying to access the private property directly will raise an AttributeError
# print(obj.__private_property)  # Uncommenting this line will cause an error
