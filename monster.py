import random
import updater


class Monster:
    def __init__(self, name, description, health, room, can_return):
        self.name = name
        self.desc = description
        self.inhealth = health
        self.health = health
        self.room = room
        self.can_return = can_return
        self.lives = 3  # Max number of lives for the monsters that can return
        room.addMonster(self)
        updater.register(self)
        self.loot = []

    def update(self):
        return
        #    if random.random() < .5:
        #       self.moveTo(self.room.randomNeighbor())

    def moveTo(self, room):
        self.room.removeMonster(self)
        self.room = room
        room.addMonster(self)

    def moveRand(self, room_list):
        self.room = room_list[random.randint(0, len(room_list) - 1)]
        while len(self.room.monsters) >= 3:
            self.room = room_list[random.randint(0, len(room_list) - 1)]

    def die(self):
        self.lives -= 1
        if (not self.can_return) or (self.can_return and self.lives <= 0):
            print("You have killed the monster.")
            if len(self.loot) > 0:
                print("This monster has loot. Which is now in the room:")
                self.displayloot()
                for l_item in self.loot:
                    self.room.items.append(l_item)
            self.room.removeMonster(self)
            updater.deregister(self)
        else:
            print("The monster has fled but may return")
            self.health = self.inhealth
            self.moveTo(self.room.randomNeighbor())

    def addloot(self, item):
        self.loot.append(item)

    def displayloot(self):
        str = ""
        for i in self.loot:
            str = str + i.name + ", "
        print(str)
