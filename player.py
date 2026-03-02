from room import Room
import os
import random


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Player:
    def __init__(self, player_name):
        self.location = None
        self.name = player_name
        self.items = []
        self.health = 50
        self.alive = True
        self.lives = 3
        self.strengths = []
        self.weaknesses = []

    def goDirection(self, room, direction):
        if (room == None):
            print("This room does not exist")
        else:
            if room.isRoomLocked():
                print("This room is locked. Unable to go in without the key")
            else:
                self.location = self.location.getDestination(direction)
                return True
        return False

    def pickup(self, item):
        if len(self.items) >= 5:
            print("You have too many items in your inventory drop an item to continue")
            return
        self.items.append(item)
        item.loc = self
        if item in self.weaknesses:
            print("This item is one of your weaknesses you have lost a life")
            self.lives = self.lives - 1
        if item not in self.location.items:
            self.location.removeItemFromChest(item)
        else:
            self.location.removeItem(item)
        if item.weap:
            item.useW(self)
        if item.armor:
            item.wearA(self)

    def showInventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        # input("Press enter to continue...")

    def attackMonster(self, mon, tk):  # make more efficient
        you_win: bool = False
        clear()
        mon_is_weakness = False
        mon_is_strength = False
        for each_mon in self.weaknesses:
            if mon.name == each_mon.name:
                mon_is_weakness = True
        for each_mon in self.strengths:
            if mon.name == each_mon.name:
                mon_is_strength = True
        # PE+str/weak/PE+ME is the prob of winning or losing
        # whoever wins loses 10 health whoever loses health-other's healht then check if health is less than 0 or not
        if mon_is_weakness:
            MsgBox = tk.messagebox.askyesno("Attack Monster Question",
                                            "Your health is " + str(self.health) + ". " +
                                            mon.name + "'s health is " + str(mon.health) + ". " +
                                            mon.name + " are your weakness are you sure you want to attack?")
            if MsgBox == False:
                return
        print("You are attacking " + mon.name)
        print()
        rand = random.random()

        if mon_is_weakness and (rand < (self.health - 30) / (self.health + mon.health)):
            you_win = True
        elif mon_is_strength and (rand < (self.health + 30) / (self.health + mon.health)):
            you_win = True
        elif rand < self.health / (self.health + mon.health):
            you_win = True

        if you_win:
            self.health -= 10
            mon.health = 0
        else:
            self.health = 0
            mon.health -= 10

        if mon.health <= 0:
            self.location.removeMonster(mon)  # remove monster from current room it may re-apper in different room
            mon.die()
        if self.health <= 0:
            self.die(tk)
        print()

    #   def run(self, mon, tk):
    #        if random.random() > self.location.prob_run:
    #            MsgBox = tk.messagebox.askyesno("Run Question",
    #                                            "The monster caught up to you\n Do you want to attack?")
    #            if MsgBox:
    #                self.attackMonster(mon, tk)
    #        else:
    #            tk.messagebox.showinfo("Run Info", "The monster didn't catch up to you you're safe...for now")
    #        print()

    def hide(self, mon, tk):
        if random.random() > self.location.prob_hide:
            MsgBox = tk.messagebox.askyesno("Hide Question",
                                            "The monster found you. \n Do you want to attack?")
            if MsgBox:
                self.attackMonster(mon, tk)
        else:
            mon.moveRand()
            print("The monster didn't find you you're safe...for now")
        print()

    def inspect(self, room):
        print("There are currently:")
        print()
        item = ""
        for i in room.items:
            item = item + i.name + ", "
        print("In the room\n")
        print("My inventory:")
        self.showInventory()

    def drop(self, item):  # change to drop <item> in main
        for i in self.items:
            if i.name == item:
                if i.armor:
                    self.health = self.health - 20
                elif i.weap:
                    self.health = self.health - 15
                self.items.remove(i)
                self.location.addItem(i)
                return
        print("That item doesn't exist in your inventory")

    def me(self):
        print("You have " + str(self.lives) + " lives")
        strength = ""
        for s in self.strengths:
            strength = strength + s.name + ", "
        weak = ""
        for w in self.weaknesses:
            weak = weak + w.name + ", "
        print("Your strengths are " + strength)
        print("Your weaknesses are " + weak)
        print()

    def die(self, tk):
        self.lives = self.lives - 1
        tk.messagebox.showinfo("Die", " You lost a life.\n\nYou have " + str(self.lives) + " lives.")
        if self.lives == 0:
            tk.messagebox.showinfo("Die", "You couldn't save Jumanji from great peril. You lost")
            self.alive = False
            exit()
        else:
            self.health = 50

    def addStrength(self, strength):
        self.strengths.append(strength)

    def addWeakness(self, weak):
        self.weaknesses.append(weak)

    def weatherImpact(self):
        health_impact = 0
        for i in range(len(self.location.weathers)):
            health_impact += self.location.weathers[i].resist
        self.health -= health_impact
