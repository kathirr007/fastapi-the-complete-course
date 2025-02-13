class Enemy:
    """
    Goal: Show Inheritance
    - Implement Zombie object
    - Explain Superclass / super()
    - Override talk function
    - Create SpreadDisease that Parent does not have
    - Create Ogre class
    - Implement Smash
    """

    def __init__(self, type_of_enemy, health_points, attack_damage):
        self.__type_of_enemy: str = type_of_enemy
        self.health_points = health_points
        self.attack_damage = attack_damage

    def enemy_type(self):
        return self.__type_of_enemy

    def set_enemy_type(self, type_of_enemy):
        self.__type_of_enemy = type_of_enemy

    def talk(self):
        print(f"I am a {self.enemy_type()}. Be prepared to fight!")

    def walk_forward(self):
        print(f"{self.enemy_type()} moves closer to you")

    def attack(self):
        print(f"{self.enemy_type()} attacks for {self.attack_damage} damage")
