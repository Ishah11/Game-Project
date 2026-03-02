import os
import random
import updater

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Weather: #can slow down speed, can transport you to a different room
    def __init__(self, name, desc, resist):
        self.name = name
        self.desc = desc
        self.loc = None
        self.resist = resist   # health resistance as the play moves to weather
        self.intprob = 0
        updater.register(self)

    def describe(self):
        print(self.desc)
        print()

    def putInRoom(self, room):
        self.loc = room
        room.addWeather(self)

    def transport(self,rooms,player):
        rand = random.randint(0, len(rooms)-1)
        while rooms[rand].isRoomLocked:
            rand = random.randint(0, len(rooms)-1)
        player.location = rooms[rand]

    def slow(self, player): #only want to slow for a certain amount of time before returning back to normal probability
        self.intprob = player.location.prob_run
        rand = random.uniform(0,1)
        while rand > self.intprob:
            rand = random.uniform(0, 1)
        player.location.prob_run = rand

    def returnProb(self, player):
        player.location.prob_run = self.intprob

    def moveTo(self, room):
        self.loc.removeWeather(self)
        self.loc = room
        room.addWeather(self)

    def update(self):
        if random.random() < .5:
            self.moveTo(self.loc.randomNeighbor())

