import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Chest:
    def __init__(self, name, desc, locked):
        self.name = name
        self.desc = desc
        self.loc = None
        self.locked = locked
        self.contains = []
    def describe(self):
        clear()
        print(self.desc)
        print()
        #input("Press enter to continue...")
    def putInRoom(self, room):
        self.loc = room
        room.addChest(self)

    def isChestLocked(self):
        if self.locked == 1:
            return True
        else:
            return False
    def unlockChest(self,player,key_need):
        for n in player.items:
            if key_need.lower() == n.name.lower():
                self.locked = 0
                print("You have unlocked the chest")
            else:
                print("You don't have the correct key, try again with a different key")
                return
    def addItem(self,item):
        self.contains.append(item)
    def removeItem(self,item):
        self.contains.remove(item)
    def displayI(self):
        print("This chest contains: ")
        str = ""
        for i in self.contains:
            str = str + i.name + ", "
        print(str)

    def moveRandRoom(self, room_list):
        room = room_list[random.randint(0, len(room_list) - 1)]
        self.putInRoom(room)