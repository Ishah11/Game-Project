import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, armor = None, weapons = None):
        self.name = name
        self.desc = desc
        self.loc = None
        self.armor = armor
        self.weap = weapons
    def describe(self):
        clear()
        print(self.desc)
        print()
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)
    def putInChest(self,chest):
        self.loc = chest
        chest.addItem(self)
    def putInLoot(self, mon):
        self.loc = mon
        mon.addloot(self)
    def moveRand(self, room_list, heart = None):
        r = random.randint(0,2) #0 = chest, 1= loot, 2=room
        room = room_list[random.randint(0, len(room_list) - 1)]
        if heart == True:
            while room == room_list[len(room_list)-1]:
                room = room_list[random.randint(0,len(room_list)-1)]
        if r == 1 and len(room.monsters) > 0:
            self.putInLoot(room.monsters[random.randint(0,len(room.monsters)-1)])
        elif r == 0 and len(room.chests) > 0:
            self.putInChest(room.chests[random.randint(0, len(room.chests) - 1)])
        else:
            self.putInRoom(room)

    def moveRandRoom(self,room_list):
        room = room_list[random.randint(0, len(room_list) - 1)]
        while room.locked == 1:
            room = room_list[random.randint(0, len(room_list) - 1)]
        self.putInRoom(room)

    def wearA(self,player):
        player.health = player.health + 20

    def useW(self,player):
        player.health = player.health + 15

