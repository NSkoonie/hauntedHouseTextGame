#Written by Noah Schoonover
from random import randint
inventory = list()
prompt = ": "
gameOver = False
nothing = 42
#LOCATION CLASS
class Location:
    def __init__(self, initLocInfo, locInfo, *contained):
        self.initLocInfo = initLocInfo
        self.locInfo = locInfo
        self.containedItems = list(contained)
        self.discovered = False
        self.magicWord = nothing

    class Direction:
        def __init__(self):
            self.to = nothing           #this should be a Location object
            self.key = nothing          #this should be a boolean

        def go(self):
            global currentLocation
            if isinstance(self.to, str):
                print(self.to)
            elif callable(self.to):
                self.to()
            elif self.to == nothing:
                return currentLocation.readLocationInfo()
            else:
                if self.key == nothing or self.checkForKey():
                    currentLocation = self.to
                    currentLocation.readLocationInfo()
                else:
                    print(self.denyMsg)

        def setKey(self, key, keyItems, denyMsg):
            setattr(self, 'key', key)
            setattr(self, 'keyItems', keyItems)
            setattr(self, 'denyMsg', denyMsg)

        def checkForKey(self):
            if self.key in self.keyItems:
                return True
            else:
                return False

    def setRelatives(self, north, east, south, west):
        self.north = self.Direction()
        self.east = self.Direction()
        self.south = self.Direction()
        self.west = self.Direction()
        
        self.north.to = north
        self.east.to = east
        self.south.to = south
        self.west.to = west

    def addContainedItem(self, item):
        self.containedItems.append(item)

    def remContainedItem(self, item):
        self.containedItems.remove(item)

    def readLocationInfo(self):
        if not self.discovered:
            if (self.initLocInfo != ''):
                print(self.initLocInfo)
                print(self.locInfo)
            else:
                print(self.locInfo)
            self.discovered = True
        else:
            print(self.locInfo)
        for x in self.containedItems:
            print(x.floorDescription)

#GAMEITEM CLASS
class GameItem:
    def __init__(self, name, floorDescription):
        self.name = name
        self.floorDescription = floorDescription
        self.readable = nothing

    #GET ITEM
    def get(self):
        if self in currentLocation.containedItems:
            currentLocation.remContainedItem(self)
            inventory.append(self)
            print("OK.")
        else:
            print("THAT\'S NOT HERE.")

    #DROP ITEM
    def drop(self):
        if self in inventory:
            inventory.remove(self)
            currentLocation.addContainedItem(self)
            print("OK.")
        else:
            print("YOU DON'T HAVE IT.")

    #READ ITEM
    def read(self):
        if self.readable == nothing:
            print("YOU'RE NOT TOO BRIGHT, ARE YOU?")
        else:
            print(self.readable)

#PRINT INVENTORY
def printInv():
    if inventory:
        for x in inventory:
            print(x.name)
    else:
        print("YOU HAVE NOTHING.")
        

##############################################
            ### Game Assets ###
#GAME ITEMS

knife = GameItem("KNIFE", "THERE IS A KNIFE.")
rope = GameItem("ROPE", "A ROPE IS NEARBY.")
key = GameItem("KEY", "YOU SEE A KEY.")
deadBush = GameItem("DEAD BUSH", "YOU SEE A DEAD BUSH.")
note = GameItem("NOTE", "THERE IS A NOTE ON THE FLOOR.")
note.readable = "THE PASSCODE IS 485...\nTHE FOURTH NUMBER IS ILLEGIBLE."
letter = GameItem("LETTER", "A LETTER IS ON THE GROUND")
letter.readable = "DON'T PUSH THE BUTTONS. JUST SAY PEBBLE"

#GAME LOCATIONS

startLocation = Location("", "YOU ARE OUTSIDE.")
outside2 = Location("", "YOU ARE OUTSIDE.", letter)
foyer = Location("THE DOOR SLAMS BEHIND YOU.", "YOU ARE IN THE FOYER.", rope)
livingRoom = Location("", "YOU ARE IN THE LIVINGROOM.")
kitchen = Location("", "YOU ARE IN THE KITCHEN.")
pantry = Location("YOU UNLOCK THE DOOR WITH THE KEY.", "ARE IN THE PANTRY.", note)
diningRoomN = Location("", "YOU ARE IN THE DINING ROOM.")
diningRoomS = Location("", "YOU ARE IN THE DINING ROOM.")
bathroom = Location("", "YOU ARE IN THE BATHROOM.", key)
bedroom1 = Location("", "YOU ARE IN THE MASTER BEDROOM. THERE ARE FOUR BUTTONS ON THE WALL. \nWHICH ONE DO YOU PRESS?")
bedroom2 = Location("", "YOU ARE IN A BEDROOM.")
hallwayE = Location("", "YOU ARE AT THE EAST END OF THE HALLWAY.")
hallwayM = Location("", "YOU ARE IN THE MIDDLE OF THE HALLWAY.")
hallwayW = Location("", "YOU ARE AT THE WEST END OF THE HALLWAY.")

upRoomN = Location("", "YOU ARE IN A ROOM.")
balcony = Location("", "YOU ARE ON THE BALCONY.")
upRoomSW = Location("", "YOU ARE IN A ROOM.")
upRoomS = Location("", "YOU ARE IN A ROOM.")
upHallwayW = Location("", "YOU ARE IN THE HALLWAY")
upHallwayM = Location("", "YOU ARE IN THE HALLWAY")
upHallwayE = Location("", "YOU ARE IN THE HALLWAY")

#LOCATION MAGIC

foyer.magicWord = "UNLOCK"
def foyerMagic():
    print("YOU'RE A REAL GENIUS, HUH?")
foyer.doMagic = foyerMagic

bedroom2.magicWord = "PAINTING"
def bedroom2Magic():
    print("YOU SWING THE PAINTING TO THE SIDE TO REVEAL A FOUR DIGIT SAFE.")
    userAnswer = input("CODE: ")
    lastDigit = str(randint(1,3))
    code = "485" + lastDigit
    if userAnswer == code or userAnswer == "nOah":
        print("THE SAFE GRANTS YOU ENTRY.\nINSIDE IS A KNIFE. YOU TAKE IT.")
        inventory.append(knife)
    elif userAnswer.upper() == "OPEN":
        print("YOU ARE AN IDIOT. THE SAFE DOOR SWINGS OPEN AND KILLS YOU.")
        global gameOver
        gameOver = True
    else:
        print("A VOICE SPEAKS FROM ALL AROUND:\
            \n\"WRONG. THE LAST DIGIT IS " + lastDigit + ".\"")
bedroom2.doMagic = bedroom2Magic

def diningRoomDeath():
    print("AS YOU TOUCH THE DOOR HANDLE YOUR ENTIRE BODY CATCHES FIRE.\nYOU BURN TO DEATH.")
    global gameOver
    gameOver = True

def bedroom1Key():
    if knife in inventory:
        print("THE MUMMY FLEES AT THE SIGHT OF YOUR KNIFE.")
        global currentLocation
        currentLocation = bedroom1
        currentLocation.readLocationInfo()
    else:
        print("A MUMMY APPEARS AND EATS YOUR SOUL. \nYOU ARE DEAD.")
        global gameOver
        gameOver = True

bedroom1.magicWord = "PEBBLE"
def bedroom1Magic():
    print("YOU TELEPORT THROUGH THE CEILING.")
    global currentLocation
    currentLocation = upRoomSW
    currentLocation.readLocationInfo()
bedroom1.doMagic = bedroom1Magic

#SET LOCATION RELATIVES

startLocation.setRelatives(nothing, outside2, foyer, nothing)
outside2.setRelatives(nothing, nothing, nothing, startLocation)
foyer.setRelatives("THE DOOR IS LOCKED. YOU CAN'T OPEN IT.", livingRoom, nothing, nothing)
livingRoom.setRelatives(nothing, nothing, kitchen, foyer)
kitchen.setRelatives(livingRoom, diningRoomN, hallwayE, pantry)
pantry.setRelatives(nothing, kitchen, nothing, nothing)
diningRoomN.setRelatives(nothing, nothing, diningRoomS, kitchen)
diningRoomS.setRelatives(diningRoomN, nothing, diningRoomDeath, bathroom)
bathroom.setRelatives("THE DOOR WON'T BUDGE.", diningRoomS, nothing, nothing)
bedroom1.setRelatives(hallwayW, nothing, nothing, nothing)
bedroom2.setRelatives(hallwayM, "ON THE EAST WALL IS A PAINTING.", nothing, nothing)
hallwayE.setRelatives(kitchen, nothing, "THE DOOR TO THE BATHROOM WON'T BUDGE.", hallwayM)
hallwayM.setRelatives(nothing, hallwayE, bedroom2, hallwayW)
hallwayW.setRelatives(nothing, hallwayM, bedroom1Key, "THE STAIRS ARE COVERED IN BROKEN GLASS. YOU CAN'T GO UP.")

upRoomSW.setRelatives(upHallwayW, nothing, "THERE IS A PICTURE OF A KNIFE ON THE WALL.", nothing)
upRoomS.setRelatives(upHallwayM, nothing, nothing, "THERE IS A PICTURE OF A LETTER ON THE WALL.")
upRoomN.setRelatives(nothing, "THERE IS A PICTURE OF A KEY ON THE WALL.", upHallwayM, nothing)
balcony.setRelatives(nothing, nothing, upHallwayE, nothing)
upHallwayW.setRelatives(nothing, upHallwayM, upRoomSW, "THE STAIRS ARE COVERED IN GLASS. YOU CAN'T GO DOWN.")
upHallwayM.setRelatives(upRoomN, upHallwayE, upRoomS, upHallwayW)
upHallwayE.setRelatives(nothing, nothing, nothing, upHallwayM)

#LOCATION/DIRECTION KEYS

kitchen.west.setKey(key, inventory, "THIS DOOR IS LOCKED.")

currentLocation = startLocation

###############################################

USE_COMMANDS = ["GET", "DROP", "READ"]
BAD_WORDS = ["CUNT", "DICK", "BITCH", "SUCK", "NUT", "TIT", "WHORE", "BALLS", "NIGGER", "PENIS", "FUCK", "PUSSY", "NIGGA", "VAGINA", "RETARD"]
BEDROOM1_KILL_WORDS = ["1", "2", "3", "4", "ONE", "TWO", "THREE", "FOUR"]

def getAnswer(): #GETS ANSWER FROM USER
    userAnswer = input(prompt).upper()
    if userAnswer == "N":
        currentLocation.north.go()
    elif userAnswer == "E":
        currentLocation.east.go()
    elif userAnswer == "S":
        currentLocation.south.go()
    elif userAnswer == "W":
        currentLocation.west.go()
    elif userAnswer == "LOOK":
        currentLocation.readLocationInfo()
    elif userAnswer == "INVENTORY" or userAnswer == "INV":
        printInv()
    elif currentLocation.magicWord != nothing and currentLocation.magicWord in userAnswer:
            currentLocation.doMagic()
    elif userAnswer == "HELP":
        print('THE BASIC COMMANDS ARE:\nN\nE\nS\nW\nLOOK\nGET\nDROP\nREAD\nINVENTORY OR INV\nHELP')
    elif any(x in userAnswer for x in BAD_WORDS):
        print("WATCH YOUR PROFANITY")
        global gameOver
        gameOver = True
    elif "HATE" in userAnswer:
        print("HATE IS A STRONG WORD.")
    elif currentLocation == bedroom1 and any(x in userAnswer for x in BEDROOM1_KILL_WORDS):
        print("YOU PRESS THE BUTTON AND YOUR EYES MELT FROM YOUR SKULL.\nYOU ARE DEAD.")
        gameOver = True
    else:
        firstWord = userAnswer.split(" ",1)[0]
        if firstWord in USE_COMMANDS: #CHECKS IF FIRST WORD IS IN COMMANDS
            itemIsHere = False
            try:
                secondWord = userAnswer.split(" ",1)[1] #GETS SECOND WORD (OR WORDS)
            except IndexError:
                print("WHAT?")
                secondWord = input(prompt) #ASKS FOR SECOND WORD WHEN EMPTY
            for x in currentLocation.containedItems + inventory:
                if secondWord == x.name:
                    referencedItem = x
                    performAction(firstWord, referencedItem)
                    itemIsHere = True
            if not itemIsHere:
                print("I DON'T UNDERSTAND.")
        else:
            print("I DON'T UNDERSTAND.")

def performAction(firstWord, item):
    if firstWord == "GET":
        getattr(item, "get")()
    elif firstWord == "DROP":
        getattr(item, "drop")()
    elif firstWord == "READ":
        getattr(item, "read")()
    else:
        print("I DON'T UNDERSTAND")


currentLocation.readLocationInfo()

while not gameOver:

    getAnswer()

    if currentLocation == upHallwayE:
        if (key in upRoomN.containedItems) and (letter in upRoomS.containedItems) and (knife in upRoomSW.containedItems):
            upHallwayE.north.to = balcony
        else:
            upHallwayE.north.to = nothing

    if currentLocation == balcony:
        if (rope in balcony.containedItems):
            print("YOU DROP THE ROPE FROM THE BALCONY AND CLIMB TO SAFETY.\nCONGRATULATIONS, YOU BEAT THE GAME.")
            gameOver = True

while gameOver:
    for x in range(7):
        trashAnswer = input("")
    print("GAME OVER")
