from test import MyClass
from Zombie import *
from Ogre import *

zombie = Zombie(10, 1)

print(
    f"{zombie.enemy_type()} has {zombie.health_points} health points and can do attack of {zombie.attack_damage}"
)

zombie.talk()
zombie.walk_forward()
zombie.attack()
zombie.spread_disease()

ogre = Ogre(20, 3)
print(
    f"{ogre.enemy_type()} has {ogre.health_points} health points and can do attack of {ogre.attack_damage}"
)

ogre.talk()
