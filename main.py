from room import Room
from player import Player
from item import Item
from monster import Monster
from chest import Chest
from weather import Weather
import os
import updater
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import tkinter.messagebox
import sys
import random


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


playerA = Player("Sarah Whittle")
playerB = Player("Alan parrish")
player = None
room_list = []
switchRoomSuccess = False


def pickPlayerA():
    global player
    global p
    player = playerA
    p = playerB
    print("You have chosen Sarah Whittle")
    player.location = room_list[0]
    player.previous_location = room_list[0]
    pop.destroy()
    printSituation(player)


def pickPlayerB():
    global player
    global p
    player = playerB
    p = playerA
    print("You have chosen Alan Parrish")
    player.location = room_list[0]
    player.previous_location = room_list[0]
    pop.destroy()  # distroy custom popup box
    printSituation(player)


def createWorld():
    # Create rooms
    k = Room("Base", "collect some needed items from here", 0, 0, 0)
    a = Room("Swamp", "muddy grounds", 0.2, 0.2,random.randint(0, 1))
    b = Room("Rocky Mountains", "cool, difficult to run, great places to hide", 0.2, 0.7,random.randint(0, 1))
    c = Room("Desert", "dry, barren, hot with very little life", 0.5, 0.1, random.randint(0, 1))
    d = Room("Plains", "full of grass and wildlife, easy to run, difficult to hide", 0.8, 0.1,random.randint(0, 1))
    e = Room("Waterfall", "wetland, with windy weather", 0.5, 0.7, random.randint(0, 1))
    f = Room("Oasis", "flat dessert located near water", 0.5, 0.8, random.randint(0, 1))
    g = Room("Old Hospital", "can replenish your health on entry to room", 0, 0, random.randint(0, 1))
    h = Room("Switch Room", "can switch your character", 0, 0, random.randint(0, 1))
    final = Room("Final Room", "drop the heart of Jumanji in this room", 0, 0, random.randint(0, 1))

    # Connect rooms with exits
    room_list.extend([k, a, b, c, d, e, f, g, h, final])
    Room.connectRooms(k, "east", c, "west")
    Room.connectRooms(a, "east", b, "west")
    Room.connectRooms(c, "east", d, "west")
    Room.connectRooms(a, "north", c, "south")
    Room.connectRooms(b, "north", d, "south")
    Room.connectRooms(b, "south", e, "north")
    Room.connectRooms(e, "east", f, "west")
    Room.connectRooms(h, "west", b, "east")
    Room.connectRooms(h, "south", f, "north")
    Room.connectRooms(g, "west", f, "east")
    Room.connectRooms(final, "north", g, "south")

    # Create weather and randomly add to rooms
    lightening = Weather("Lightening", "This weather will slow you down drastically as you try to duck out of it", 2)
    lightening.putInRoom(b)
    sand_storm = Weather("Sand Storm", "This weather will slow you down", 2)
    sand_storm.putInRoom(c)
    rain = Weather("Rain", "This weather will slightly slow you down", 1)
    rain.putInRoom(e)
    heavy_wind = Weather("Heavy Wind", "This weather will speed you up through the room", -1) # health with increase in this weather
    heavy_wind.putInRoom(b)

    # Create chests

    chest_list = []
    chest = Chest("Base Chest", "This contains some of the necessary items to unlock each room", 0)
    chest.putInRoom(k)
    stch = Chest("Stone Chest", "This contains some of the necessary items", random.randint(0, 1))
    stch.moveRandRoom(room_list)
    snowch = Chest("Snow Chest", "This contains some of the necessary items", random.randint(0, 1))
    snowch.moveRandRoom(room_list)
    rust = Chest("Rusty Chest", "This contains some of the necessary items", random.randint(0, 1))
    rust.moveRandRoom(room_list)
    murk = Chest("Murky Chest", "This contains some of the necessary items", random.randint(0, 1))
    murk.moveRandRoom(room_list)
    clean = Chest("Clean Chest", "This contains some of the necessary items", random.randint(0, 1))
    clean.moveRandRoom(room_list)
    chest_list.extend([chest,stch,snowch,rust,murk,clean])

    for che in chest_list:
        if che.locked == 1:
            q = Item(che.name + " Key", "Used to unlock " + che.name)
            q.moveRandRoom(room_list)

    p = Item("Poison", "This is dangerous")
    p.moveRand(room_list)
    hj = Item("Heart of Jumanji", "You need to drop this in the final room")
    hj.moveRand(room_list, True)
    sw = Item("Sword", "Weapon", False, True)
    sw.moveRand(room_list)
    arr = Item("Bow and Arrow", "Weapon", False, True)
    arr.moveRand(room_list)
    axe = Item("Axe", "Weapon", False, True)
    axe.moveRand(room_list)
    sh = Item("Shield", "Protection", True, False)
    sh.moveRand(room_list)
    chep = Item("Chest Plate", "Protection", True, False)
    chep.moveRand(room_list)
    hm = Item("Helmet", "Protection", True, False)
    hm.moveRand(room_list)

    bg = Item("Board game", "What got you into this mess")
    bg.moveRand(room_list)
    cb = Item("Crystal ball", "Can forsee the future")
    cb.moveRand(room_list)
    dice = Item("Dice", "What got you into this mess")
    dice.moveRand(room_list)
    vg = Item("Video game", "What got you into this mess")
    vg.moveRand(room_list)
    pc = Item("Pound Cake", "Food")
    pc.moveRand(room_list)
    je = Item("Jaguar's Eye", "What got you into this mess")
    je.moveRand(room_list)
    fj = Item("Falcon Jewel", "What got you into this mess")
    fj.moveRand(room_list)


    for r in room_list:
        if r.locked == 1:
            rmi = Item(r.name + " Key", "Used to unlock " + r.name)
            rmi.putInChest(chest)

    # Create Monsters and randomly add to rooms
    hr = Monster("Herd of Rhinos", "Don’t be fooled, it isn’t thunder. Staying put would be a blunder.", 40, a, False)
    hr.moveRand(room_list)
    vf = Monster("Vines and Poisonous Flowers",
                 "They grow much faster than bamboo, take care or they’ll come after you.", 20, c, True)
    vf.moveRand(room_list)
    gm = Monster("Giant Mosquitoes", "A tiny bite can make you itch, make you sneeze, make you twitch.", 20, a, False)
    gm.moveRand(room_list)
    m = Monster("Monkeys", "This will not be an easy mission, monkeys slow the expedition.", 25, a, False)
    m.moveRand(room_list)
    sp = Monster("Spiders", "Need a hand? Why you just wait. We’ll help you out, we each have eight.", 15, a, True)
    sp.moveRand(room_list)
    vp = Monster("The hunter van pelt", "A hunter from the darkest wild makes you feel just like a child", 50, a, False)
    vp.moveRand(room_list)
    ba = Monster("Bats", "At night they fly, you better run. These winged things are not much fun.", 20, a, True)
    ba.moveRand(room_list)
    li = Monster("Lion", "His fangs are sharp. He likes your taste. Your party better move poste haste.", 50, a, False)
    li.moveRand(room_list)

    # Define Strengths and Weaknesses of player A and B
    playerA.addStrength(m)
    playerA.addStrength(gm)
    playerA.addWeakness(ba)
    playerA.addWeakness(li)
    playerB.addStrength(vp)
    playerB.addStrength(hr)
    playerB.addWeakness(sp)
    playerB.addWeakness(pc)
    playerB.addWeakness(vf)


def switch():
    global player
    global p
    MsgBox = tk.messagebox.askyesno("Switch Player",
                                    "You have entered the switch room where you have the ability to switch your "
                                    "character\n before proceeding to the next challenges\n Do you want to switch your "
                                    "character to " + p.name)
    if MsgBox:
        temp = player
        player = p
        p = temp
        player.location = p.location
        player.items = p.items  # transfer items from current player to other player
        p.items = []
        print("New Player: " + player.name)
    else:
        print("You choose to continue with: " + player.name)


def heal():
    MsgBox = tk.messagebox.askyesno("Heal Question",
                                    "You have entered an old hospital which can replenish your health \n You "
                                    "can't gain back any lives but you can replenish your health. Would you like "
                                    "to? " + player.name)
    if MsgBox:
        player.health += 20


def printSituation(player):
    global switchRoomSuccess
    clear()

    print("\nYou are in room: " + player.location.name)
    print(" • " + player.location.desc)
    print()

    canvas1.moveto(playerImage, room_screen_locX[player.location.name] + 10, 10)

    if player.location.hasMonsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(" • " + m.name, ": ", m.desc)
        print()
    if player.location.hasItems():
        print("This room contains the following items:")
        for i in player.location.items:
            print(" • " + i.name)

    if player.location.hasChests():
        print("This room contains the following chests:")
        for i in player.location.chests:
            print(" • " + i.name)
        print()

    print("You can go in the following directions:")
    for e in player.location.exits:
        print(" • " + e[0] + ", leads to room: " + e[1].name)
    print()
    if player.location.name == "Old Hospital":
        if switchRoomSuccess:  # only heal once per entry in to the Old hospital room
            heal()
            switchRoomSuccess = False
    if player.location.name == "Switch Room":
        if switchRoomSuccess:  # only allow to switch player once open entry to the room
            switch()
            switchRoomSuccess = False
    print("======================================")


def printPlayerInformation():
    player_text.delete(1.0, tk.END)
    player_text.insert(tk.END, "Health: " + str(player.health) + "\n")
    player_text.insert(tk.END, "Lives: " + str(player.lives) + "\n")
    player_text.insert(tk.END, player.name + " Has:")
    for i in player.items:
        player_text.insert(tk.END, "\n  " + i.name)

    # Strength
    player_strength.delete(1.0, tk.END)
    player_strength.insert(tk.END, player.name + " strengths:")
    for i in player.strengths:
        player_strength.insert(tk.END, "\n  " + i.name)

    # Weakness
    player_weakness.delete(1.0, tk.END)
    player_weakness.insert(tk.END, player.name + " weaknesses:")
    for i in player.weaknesses:
        player_weakness.insert(tk.END, "\n  " + i.name)

def printWeatherInformation():
    weather_text.delete(1.0, tk.END)
    for room in room_list:
        for i in range(len(room.weathers)):
            weather_text.insert(tk.END, room.name + " has " + room.weathers[i].name + "\n")

def showHelp():
    clear()
    print("Objective: pickup the Heart of Jumanji and drop it in the final room")
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print("inspect -- displays items in current location and items in your inventory")
    print("open <chest> -- displays items in the chest")
    print("when monster appears:attack<monster>--hide from<monster")
    print("drop <item> is used to drop item from your inventory if it is too full")
    print("unlock room <room> or unlock chest <chest> is used to unlock rooms and chests if you have the correct key")
    print()


def wait():
    health_impact = 0
    command = entryW.get()
    commandT = command.split()
    time = abs(int(commandT[0]))
    while time > 0:
        player.weatherImpact()  # players health will change based on weather condition in the room
        updater.updateAll()
        time = time - 1


def abbrev(command, ins):
    bol = False
    if ins == "i" or ins == "in" or ins == "unlock":
        return False
    for i in range(len(ins)):
        if command[i] == ins[i]:
            bol = True
        else:
            return False
    return bol


createWorld()

# Create canvas and visual objects
root = tk.Tk()


def command_processing(optional_arg):
    global player
    global switchRoomSuccess

    text_console.delete(1.0, tk.END)  # clear screen ***** Not working

    if player is None:
        print("Pick a Player by clicking Player selection button.")
        return

    commandSuccess = True
    command = entry1.get()
    print("Command Entered: " + command)
    entry1.delete(0, "end")

    if command == "":
        print("Command is empty")
        commandSuccess = False
        text_console.yview_pickplace("end")
        return
    commandWords = command.split()
    if abbrev("go", commandWords[0].lower()):  # cannot handle multi-word directions
        if len(commandWords) < 2:
            print("go command syntax: go <direction>")
            text_console.yview_pickplace("end")
            return
        # check and return number of monsters in this room
        if len(player.location.monsters) <= 0:
            switchRoomSuccess = player.goDirection(player.location.getDestination(commandWords[1]), commandWords[1])
        else:
            printSituation(player)
            print("There are still monsters in the room. \n You need to hide from or attack monster before "
                  "moving to different room")
            text_console.yview_pickplace("end")
            return
    elif abbrev("open", commandWords[0].lower()):
        #targetName = command[5:]
        target = player.location.getChestByName(commandWords[1] + " " + commandWords[2])
        if target:
            target.displayI()
        else:
            print("No such Chest")
    elif abbrev("pickup", commandWords[0].lower()):  # can handle multi-word objects
        # check and return number of monsters in this room
        if len(player.location.monsters) > 0:
            print("There are still monsters in the room. \n You need to hide from or attack monster before "
                  "picking up items")
            text_console.yview_pickplace("end")
            return
        targetName = " ".join(commandWords[1:])
        target = player.location.getItemByName(targetName)
        target2 = player.location.getItemByNameFromChest(targetName)
        if target != False:
            player.pickup(target)
        elif target2 != False:
            player.pickup(target2)
        else:
            print("No such item.")
            commandSuccess = False
    elif abbrev("inventory", commandWords[0].lower()):
        player.showInventory()
    elif abbrev("help", commandWords[0].lower()):
        showHelp()
    elif abbrev("inspect", commandWords[0].lower()):
        player.inspect(player.location)
    elif abbrev("drop", commandWords[0].lower()):
        targetName = " ".join(commandWords[1:])
        player.drop(targetName)

    elif abbrev("exit", commandWords[0].lower()):
        MsgBox = tk.messagebox.askyesno("Exit Game",
                                        "Are you sure you want to exit?")
        if MsgBox:
            root.destroy()
        return
    elif abbrev("me", commandWords[0].lower()):
        player.me()
    elif abbrev("attack", commandWords[0].lower()):
        targetName = " ".join(commandWords[1:])
        target = player.location.getMonsterByName(targetName)
        if target != False:
            player.attackMonster(target, tk)
        else:
            print("No such monster.")
            commandSuccess = False
    elif abbrev("hide from", commandWords[0].lower()):
        targetName = " ".join(commandWords[2:])
        target = player.location.getMonsterByName(targetName)
        if target != False:
            player.hide(target, tk)
        else:
            print("No such monster.")
            commandSuccess = False
    elif abbrev("unlock room", " ".join(commandWords[0:2]).lower()):
        targetName = " ".join(commandWords[2:])
        room_unlocked = False
        for rm in room_list:
            if rm.name.lower() == targetName.lower():
                rm.unlockDoor(player, targetName + " Key")
                room_unlocked = True
        if not room_unlocked:
            print("This room does not exist")
    elif abbrev("unlock chest", " ".join(commandWords[0:2]).lower()):
        targetName = " ".join(commandWords[2:])
        for c in player.location.chests:
            if c.name.lower() == targetName.lower():
                c.unlockChest(player, targetName + " Key")
        else:
            print("This room does not exist")
    else:
        print("Not a valid command")
        commandSuccess = False

    if commandSuccess:
        wait()
        printSituation(player)
        printPlayerInformation()
        printWeatherInformation()

    if room_list[9].getItemByName("Heart of Jumanji"):
        tk.messagebox.showinfo("Hurray!!!", "When you reflect on actions past, the quest you're on will end at last\n "
                                            "Congratulations you won!")
        exit()  # You Win Game End

    text_console.yview_pickplace("end")


def selectPlayer():
    global pop
    pop = tk.Toplevel(root)
    pop.title("Select Player")
    pop.geometry("250x150")
    pop.config(bg="green")

    pop_label = tk.Label(pop, text="Select Player!!")
    pop_label.pack(pady=10)

    my_frame = tk.Frame(pop, bg="light yellow")
    my_frame.pack(pady=5)

    buttonA = tk.Button(my_frame, text='Sarah Whittle', bg="light blue", command=pickPlayerA)
    buttonA.grid(row=1, column=1)

    buttonB = tk.Button(my_frame, text='Alan Parrish', bg="light blue", command=pickPlayerB)
    buttonB.grid(row=1, column=2)


############################################################################################

canvas1 = tk.Canvas(root, width=2000, height=1000, relief='raised')
root.title("Jumanji!!")
root.geometry("1100x750")
canvas1.pack()
room_screen_locX = {}

for r in range(len(room_list)):
    room_screen_locX[room_list[r].name] = r * 110
    canvas1.create_rectangle(0 + (r * 110), 0, 100 + (r * 110), 100, outline='black')
    label2 = tk.Label(root, text=room_list[r].name)
    label2.config(font=('helvetica', 10))
    canvas1.create_window(50 + (r * 110), 100, window=label2)

playerImage = canvas1.create_rectangle(10, 10, 20, 20, outline='black')

label1 = tk.Label(root, text='Player Information:')  # Create text for player.display
label1.config(font=('helvetica', 10))
canvas1.create_window(70, 130, window=label1)

player_text = tk.Text(root, height=7, width=25, bg="light cyan")
player_text.config(font=('helvetica', 10))
canvas1.create_window(100, 200, window=player_text)

player_strength = tk.Text(root, height=7, width=25, bg="light green")
player_strength.config(font=('helvetica', 10))
canvas1.create_window(300, 200, window=player_strength)

player_weakness = tk.Text(root, height=7, width=25, bg="pink")
player_weakness.config(font=('helvetica', 10))
canvas1.create_window(500, 200, window=player_weakness)

# label2 = tk.Label(root, text='Monster Information:')
# label2.config(font=('helvetica', 10))
# canvas1.create_window(6 * 110, 200, window=label2)

label2 = tk.Label(root, text='Weather Information:')  # Create text for player.display
label2.config(font=('helvetica', 10))
canvas1.create_window(680, 130, window=label2)

weather_text = tk.Text(root, height=7, width=35, bg="light cyan")
weather_text.config(font=('helvetica', 10))
canvas1.create_window(740, 200, window=weather_text)

label4 = tk.Label(root, text='Wait Time')
label4.config(font=('helvetica', 10))
canvas1.create_window(6 * 110, 400, window=label4)

entryW = tk.Entry(root, width=15)
entryW.insert(0, "5")
canvas1.create_window(6 * 110, 420, window=entryW)

label3 = tk.Label(root, text='Input command:')
label3.config(font=('helvetica', 10))
canvas1.create_window(6 * 110, 500, window=label3)

entry1 = tk.Entry(root, width=15)
canvas1.create_window(6 * 110, 520, window=entry1)
entry1.bind('<Return>', command_processing)

button1 = tk.Button(text='Enter', command=lambda: command_processing("yes"))
canvas1.create_window(6 * 110, 550, window=button1)

text_console = scrolledtext.ScrolledText(root, background='#fcef91', borderwidth=2, height=25, width=70)  # add border
text_console.config(font=('helvetica', 10))
canvas1.create_window(300, 500, window=text_console)

# buttonW = tk.Button(text='Wait time', bg ="blue", command=wait)
# canvas1.create_window(6*110, 450, window=buttonW)

sys.stdout = TextRedirector(text_console, "stdout")
sys.stderr = TextRedirector(text_console, "stderr")

tk.messagebox.showinfo("Welcome to Jumanji, The text-based game",
                       "A game for those who seek to find a way to leave their world behind."
                       "The goal for you I'll recite in verse; return the jewel and lift the curse."
                       "If you wish to leave the game, you must save Jumanji\n\n")

selectPlayer()

root.mainloop()
