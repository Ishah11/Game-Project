import random

class Room:
    def __init__(self, name, description, prob_run, prob_hide, locked):
        self.desc = description
        self.monsters = []
        self.exits = []
        self.items = []
        self.chests = []
        self.weathers = []
        self.name = name
        self.locked = locked  # if 1 then door is locked
        self.prob_run = prob_run
        self.prob_hide = prob_hide

    def addExit(self, exitName, destination):
        self.exits.append([exitName, destination])

    def getDestination(self, direction):
        for e in self.exits:
            if e[0] == direction:
                return e[1]
        return None

    def connectRooms(room1, dir1, room2, dir2):
        # creates "dir1" exit from room1 to room2 and vice versa
        room1.addExit(dir1, room2)
        room2.addExit(dir2, room1)

    def exitNames(self):
        return [x[0] for x in self.exits]

    def addItem(self, item):
        self.items.append(item)

    def removeItem(self, item):
        self.items.remove(item)

    def addWeather(self, weather):
        self.weathers.append(weather)

    def removeWeather(self, weather):
        self.weathers.remove(weather)

    def addChest(self, chest):
        self.chests.append(chest)

    def removeChest(self, chest):
        self.chests.remove(chest)

    def addMonster(self, monster):
        self.monsters.append(monster)

    def removeMonster(self, monster):
        if (monster in self.monsters):
            self.monsters.remove(monster)

    def hasChests(self):
        return self.chests != []

    def getItemByNameFromChest(self, name):
        for c in self.chests:
            for i in c.contains:
                if i.name.lower() == name.lower():
                    return i
        return False

    def hasItems(self):
        return self.items != []

    def getItemByName(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False

    def getChestByName(self, name):
        for i in self.chests:
            if i.name.lower() == name.lower():
                return i
        return False

    def hasMonsters(self):
        return self.monsters != []

    def getMonsterByName(self, name):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
        return False

    def randomNeighbor(self):
        return random.choice(self.exits)[1]

    def removeItemFromChest(self, item):
        for c in self.chests:
            if item in c.contains:
                c.removeItem(item)

    def unlockDoor(self, player, key_need):
        pickupSuccess = False
        for n in player.items:
            if key_need.lower() == n.name.lower():
                self.locked = 0
                print("You have unlocked the door")
                return
        print("You don't have the correct item, try again later")
        return

    def isRoomLocked(self):
        if self.locked == 1:
            return True
        else:
            return False
