"""
Created by River Veek

Adventure Simulator v2 -> Adventure Simulator v3 (now with classes and objects!).
Culmination of skills from CIS 122, CIS 210, and CIS 211.

Latest updated: July 5, 2019
What's new?
- Buying/Trading mechanics
- Usable items
- Boss fights
"""

from typing import List
import random
import turtle as t

PLAYER = None  # character chosen by the player
X, Y = 0, 0  # starting position of player
OPPONENT = None  # random character that player will battle


ESCAPE = ["Congrats, you escaped",
          "You lucked out, the enemy couldn't keep up",
          "What a surprise, you got away",
          "You have successfully escaped",
          "You could do this all day",
          "Phew! You escaped, that was a close one"
          ]
FAIL = ["You failed to escape, prepare to battle",
        "Better luck next time, prepare to battle",
        "You tried to escape but tripped on your ego",
        "You weren't quick enough",
        "You failed to flee and got a little scuffed up",
        "You call that an escape plan?"
        ]
MATCHUP = ["Looks like you ran into some trouble",
           "A new challenger has approached",
           "You stumbled into the wrong neighborhood",
           "Prepare to battle",
           "It's time to fight",
           "You ran into an ememy, let's get this over with",
           "An enemy approaches! Let the games begin"
           ]
P_MISSED = ["Oh no, your attack missed!",
            "Terrible execution, your attack missed",
            "You slipped up and missed your attack"
            ]
O_MISSED = ["You lucked out, the enemy missed their shot",
            "The enemy missed",
            "That's embarrassing, the enemy missed",
            "The enemy's attack fell short"
            ]


class Character:
    """
    Creates a playable character.
    Includes name, 3 attacks, health, and luck.
    """
    def __init__(self, name: str, moves: List[List], health: int, luck: int):
        self.name = name
        self.moves = moves
        self.health = health
        self.luck = luck
        self.items = []
        self.money = 0
        # maybe add x, y position here for movement
        # maybe add ID tag/index

    def __repr__(self):
        return f"{self.name}"  # hides {self.moves}, {self.health}, {self.luck}

    def lucky(self):
        """Returns True if random number falls in list of lucky ints."""
        luck = [i for i in range(1, self.luck + 1)]
        chance = random.randint(1, 10)
        return chance in luck

    def fight_flight(self, choose: bool = False):
        if not choose:
            while True:
                choice = input("Do you want to [f]ight or [r]un? ").strip().lower()
                if not choice == 'f' and not choice == 'r':
                    print("Please enter a valid character\n")
                elif choice == 'f':
                    print("\nPrepare to battle\n")
                    return True
                else:
                    if self.lucky():
                        print(random.choice(ESCAPE))
                        return False  # False if escape, else True
                    else:
                        print(random.choice(FAIL))
                        return True
        else:
            if OPPONENT.lucky():
                print("The enemy escaped the battle!")
                return False
            else:
                print("The enemy tried to escape, but failed")
                return True

    def print_items(self, num: int, val: bool = False):
        ct = num  # num will be either 3 or 0
        for item in self.items:
            print(f"[{ct}] {item} ({item.dur} use(s) left):")
            if val:
                print(f"\tValue: {item.value}")
            if item.dmg:
                print(f"\tDamage: {item.dmg}")
            if item.hp:
                print(f"\tHealing points: {item.hp}")
            ct += 1

    def is_full(self):
        check = any(item.name == 'Backpack' for item in self.items)  # use any() to find if backpack in items
        if check and len(self.items) == 7:  #additional spot since backpack takes up a spot
            return True  # is full
        elif check and len(self.items) == 3:
            return False  # is not full
        elif len(self.items) == 3:
            return True
        return False  # removed else bc of redundancy

    def add_item(self, item: 'Item'):  # consider changing name to 'pick_up'
        # max_items = 6 if 'Backpack' in self.items else 3  # 'Backpack' increases carrying amount
        check = any(item.name == 'Backpack' for item in self.items)  # use any() to find if backpack in items
        if check:
            max_items = 6
        else:
            max_items = 3
        while True:
            add = input(f"A(n) {item}! Would you like to pick it up, [y]es or [n]o? ").strip().lower()
            if add == 'y' and len(self.items) < max_items:
                self.items.append(item)
                # FIXME: possible error, consider making Treasure/Coin subclass of Item
                self.money += item.value  # adds value of item to player money
                return True  # picks item up
            if add == 'n':
                return False  # leaves item
            elif add == 'y' and len(self.items) == max_items:
                print("Your inventory is already full")
                # FIXME: prompt to drop an item

    def consume_item(self, item: 'Item'):
        if item.hp:
            self.health += item.hp
            print(f"You have consumed a(n) {item}\n")
            item.use()
            if item.dur <= 0:
                self.items.remove(item)
        else:
            print(f"You cannot consume a(n) {item}\n")  # may not ever reach this

    def use_item(self, item: 'Item'):
        if item.dmg:
            OPPONENT.health -= item.dmg
            print(f"{OPPONENT}'s health - {item.dmg} = {max(0, OPPONENT.health)}\n")
            item.use()
            if item.dur <= 0:
                self.items.remove(item)
        else:
            print(f"You cannot attack with a(n) {item}\n")  # may not ever reach this


class Boss(Character):
    def __repr__(self):
        return self.name + ' (Boss)'


class Item:
    """Creates an item that can be added to a Character's item list."""
    def __init__(self, name: str, value: int, dur: int, dmg: int = 0, hp: int = 0):
        self.name = name
        self.value = value
        self.dur = dur
        self.dmg = dmg
        self.hp = hp

    def __repr__(self):
        return f"{self.name}"

    def use(self):
        self.dur -= 1


class Location:
    """Creates a location that can appear on the map."""
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class Shop(Location):
    """A type of location that sells weapons."""
    def __init__(self, name: str):
        super().__init__(name)
        self.items = []

    def print_items(self):
        ct = 0
        for item in self.items:
            print(f"[{ct}] {item}: {item.value} coin(s)")
            ct += 1
        print('\n')

    def greeting(self):
        print(f"Welcome to {self.name}")
        self.print_items()
        first_time = True
        while True:
            decide = input("Would you like to [b]uy, [t]rade something, or leave[enter]? ").lower().strip()
            if decide == '':
                # print("Goodbye.")
                break
            elif decide == 'b':
                self.buy(first_time)
                first_time = False
            elif decide == 't':
                self.trade(first_time)
                first_time = False
            else:
                print("Please enter a valid key.")
        return first_time

    def buy(self, first_time: bool):
        print(f"Total money: {PLAYER.money}")  # added shows current money
        if not first_time:
            self.print_items()
        while True:
            choose = input("Which item would you like to buy? ").lower().strip()
            try:
                if choose == '':  # leaves shop
                    break
                choose = self.items[int(choose)]
                if choose.value <= PLAYER.money:  # if player has enough money
                    if not PLAYER.is_full():  # if the player inventory is not full already
                        PLAYER.items.append(choose)
                        PLAYER.money -= choose.value
                        self.items.remove(choose)
                        print(f"You have bought a(n) {choose} for {choose.value} coins")
                        break
                    else:
                        while True:
                            choice = input("Your inventory is full, would you like to discard an item, [y]es or [n]o? ")
                            choice = choice.lower().strip()
                            if choice == 'y':
                                PLAYER.print_items(num = 0)
                                discard = input("Which item would you like to discard? ").strip()
                                try:
                                    discard = PLAYER.items[int(discard)]
                                    PLAYER.items.remove(discard)
                                    break  # maybe fixed
                                except ValueError:
                                    print("Please enter a valid key.")
                                    break  # maybe fixed
                            else:
                                break
                else:
                    print("You do not have enough money to purchase this item")  # maybe fixed
                    break
                # break
            except ValueError:
                print("Please enter a valid key.")
        print("Thanks for stopping by.")

    def trade(self, first_time: bool):
        print(f"Total money: {PLAYER.money}")  # added shows current money
        if not first_time:
            self.print_items()
            # print('\n')
        first_pass = True
        more = True
        if len(PLAYER.items) > 0:
            empty = False
        else:
            empty = True
        # empty = False if len(PLAYER.items) > 0 else True
        while True:
            if not first_pass:
                while True:
                    self.print_items()
                    # print('\n')
                    more = input("\nWould you like to trade anything else, [y]es or [n]o? ").strip().lower()
                    if more == 'y':
                        break
                    elif more == 'n':
                        print("Safe travels!")
                        more = False
                        break
                    else:
                        print("Please enter a valid key")
            if empty:
                print("You have no more items to trade.")
                break
            if not more:
                break
            ct = 0
            for item in PLAYER.items:
                print(f"[{ct}] {item}: {item.value} coin(s)")
                ct += 1
            item = input("\nWhich item would you like to trade? ").strip()
            if item == '':  # leaves shop
                break
            try:
                print(f"You have traded a(n) {PLAYER.items[int(item)]}.")
                item = PLAYER.items[int(item)]
                self.items.append(item)
                PLAYER.money += item.value
                PLAYER.items.remove(item)
            except ValueError:
                print("Please enter a valid key.")
            first_pass = False


# previously called 'fighters'
# each character follows Character('name', [moves], health: int, luck: int)
# CHARACTERS = List[tuples]
CHARACTERS = [('Giant',
                        [['STOMP', 75], ['BOULDER THROW', 40], ['SMASH', 60]],
                        110,
                        2),
              ('Ninja',
                        [['HADOUKEN', 25], ['TRIPLE PUNCH', 75], ['KICK', 30]],
                        75,
                        9),
              ('Knight',
                        [['SWORD', 30], ['CROSSBOW', 20], ['PUNCH', 20]],
                        90,
                        6),
              ('Cowboy',
                        [['QUICK DRAW', 25], ['LASSO', 10], ['BULLS-EYE', 50]],
                        90,
                        9),
              ('Spy',
                        [['POISON', 30], ['SNIPE', 40], ['SUBDUE', 60]],
                        30,
                        10),
              ('Skeleton',
                        [['DAGGER', 45], ['DE-SPINE', 50], ['BOW', 30]],
                        80,
                        4),
              ('Wizard',
                        [['SPELL OF CONFUSION', 10], ['ENERGY BEAM', 50], ['LIGHTNING BOLT', 40]],
                        80,
                        8),
              ('Phoenix',
                        [['FIREBALL', 40], ['INCINERATION', 80], ['CLOUD OF ASHES', 15]],
                        90,
                        5),
              ('Cyborg',
                        [['LASER BEAM', 30], ['ROCKET LAUNCHER', 50], ['PUNCH', 40]],
                        80,
                        5),
              ('Bear',
                        [['30-MPH CHARGE', 30], ['MAUL', 50], ['CLAW', 40]],
                        80,
                        6),
              ('Monkey',
                        [['SCREECH', 10], ['THROW BANANA PEEL', 20], ['THROW BARREL', 40]],
                        30,
                        9)
              ]
BOSSES = [('Dragon',
           [['FIRE BREATHING', 60], ['DRAGON CLAW', 50], ['HEAT WAVE', 80]],
           200,
           10),
          ('SERPENT',
           [['CONSTRICT', 60], ['VENOM', 80], ['ILLUSION', 50]],
           190,
           10),
          ('MECHA',
           [['BLAST CANNONS', 80], ['SEISMIC BLAST', 90], ['HEAT-SEEKING MISSILES', 75]],
          230,
          10)
          ]
# follows Item(name: str, value: int, duration: int, damage: int, healing points: int)
ITEMS = [('Healing Potion', 50, 1, 0, 40),
         ('Health Stim', 75, 1, 0, 100),
         ('Banana', 2, 1, 1, 5),
         ('Apple', 2, 1, 2, 5),
         ('Dead Fish', 0, 1, 1, 0),

         ('Poison Blow Dart Gun', 15, 5, 30, 0),
         ('Hand Grenade', 20, 1, 45, 0),
         ('Throwing Knife', 5, 20, 15, 0),
         ('Smoke Bomb', 10, 1, 2, 0),
         ('Throwing Star', 5, 10, 15, 0),

         ('Twig', 1, 1, 1, 0),
         ('Rock', 1, 1, 2, 0),
         ('Backpack', 50, 100, 0, 0),
         ('Gold Medallion', 30, 1, 0, 0),
         ('Gold coin', 20, 1, 0, 0),
         ('Silver coin', 15, 1, 0, 0),
         ('Diamond', 45, 1, 0, 0),
         ('Ruby', 30, 1, 0, 0),
         ('Gold Necklace', 30, 1, 0, 0),
         ('Silver Pendant', 25, 1, 0, 0)
         ]
LOCATIONS = ["The Trading Post",
             "Ye Olde Shoppe",
             "Riverside Pawn",
             "The Dragon's Den",
             "The Treasure Trove",
             "River's Gifts",
             "Cowboy's General Store",
             "The Giant's Landing Giftshop"
             ]


class Game:
    """Adds text, prompts, and other game elements."""
    def print_characters(self, stats: bool = False):
        ct = 0
        for character in CHARACTERS:
            print(f"[{ct}] {character[0]}")
            ct += 1
            if stats:
                print("MOVES:")
                for move, hit in character[1]:
                    print(f"\t{move}: {hit}")
                print(f"HEALTH: {character[2]}\nLUCK: {character[3]}\n")

    def choose_character(self):
        """Prompts player to select a character or display character stats."""
        global PLAYER
        while True:
            PLAYER = input("\nChoose your character; for character stats, press [s] --> ").strip().lower()
            if PLAYER == 's':
                print()
                self.print_characters(True)
            elif PLAYER == '':
                print("Goodbye.")
                break
            else:
                try:
                    PLAYER = int(PLAYER)
                    if 0 <= PLAYER <= len(CHARACTERS) - 1:
                        print(f"You have chosen {CHARACTERS[PLAYER][0]}\n")
                        PLAYER = Character(* CHARACTERS[PLAYER])
                        break
                    else:
                        print("Please enter a valid key.")
                except ValueError:
                    print("Please enter a valid key.")

    def matchup(self):
        global OPPONENT
        print(f"{random.choice(MATCHUP)}\n")
        # OPPONENT = Character(* random.choice(CHARACTERS))
        print(f"You ({PLAYER}) vs. {OPPONENT}")

    def battle(self):
        self.matchup()
        active = None  # True if player goes first, else False
        if random.randint(0, 1):  # coin toss to determine who gets first move
            print("You get the first move.\n")
            active = True
        else:
            print(f"{OPPONENT} gets the first move.\n")
            active = False

        while PLAYER.health > 0 and OPPONENT.health > 0:

            if active:  # player's move
                if PLAYER.fight_flight():  # player's move only if they do not run/fail to run
                    ct = 0
                    for move, hit in PLAYER.moves:
                        print(f"[{ct}] {move}: {hit}")
                        ct += 1
                    print()

                    if PLAYER.items:
                        PLAYER.print_items(num = 3)

                    move = input("\nWhich move or item would you like to choose? ").strip()  # choose move
                    # print()
                    if not move:
                        print("Goodbye.")  # exits game
                        break
                    try:
                        move = int(move)
                        if len(PLAYER.items) > 0 and 2 < move < len(PLAYER.moves) + len(PLAYER.items):
                            move -= 3  # offsets list since it is indexed differently
                            item = PLAYER.items[move]
                            print(f"You chose {item}")
                            item.use()
                            # print(item.hp, item.dmg)
                            if item.hp:
                                PLAYER.consume_item(item)
                            elif item.dmg:
                                PLAYER.use_item(item)
                            else:
                                print(f"You cannot use a(n) {item} right now.\n")
                            active = False  # may need to delete this line and add to each conditional except else
                        else:
                            while True:
                                if not -1 < move < len(PLAYER.moves):
                                    print("Please enter a valid move number.\n")
                                    break
                                else:
                                    print(f"You chose {PLAYER.moves[move][0]}\n")
                                    if PLAYER.lucky():
                                        # current = OPPONENT.health
                                        OPPONENT.health -= PLAYER.moves[move][1]  # deals damage
                                        print(
                                            f"{OPPONENT}'s health - {PLAYER.moves[move][1]} = {max(0, OPPONENT.health)}\n")
                                    else:
                                        print(f"{random.choice(P_MISSED)}\n")  # if attack misses
                                    active = False
                                    break
                    except ValueError:
                        print("Please enter a valid move number.\n")
                else:
                    return 'ran'  # work around if you manage to escape

            else:  # opponent's move
                check = random.randint(1, 10) == random.randint(1, 10)
                if check:
                    if OPPONENT.fight_flight(check):
                        move = random.randint(0, len(OPPONENT.moves) - 1)  # choose move
                        print(f"{OPPONENT} used {OPPONENT.moves[move][0]}\n")  # changed 'chose' to 'used'
                        if OPPONENT.lucky():
                            # current = OPPONENT.health
                            PLAYER.health -= OPPONENT.moves[move][1]  # deals damage
                            print(f"Your ({PLAYER}'s) health - {OPPONENT.moves[move][1]} = {max(0, PLAYER.health)}")
                        else:
                            print(f"{random.choice(O_MISSED)}\n")  # if attack misses
                        active = True
                else:
                    move = random.randint(0, len(OPPONENT.moves) - 1)  # choose move
                    print(f"{OPPONENT} used {OPPONENT.moves[move][0]}\n")  # changed 'chose' to 'used'
                    if OPPONENT.lucky():
                        # current = OPPONENT.health
                        PLAYER.health -= OPPONENT.moves[move][1]  # deals damage
                        print(f"Your ({PLAYER}'s) health - {OPPONENT.moves[move][1]} = {max(0, PLAYER.health)}")
                    else:
                        print(f"{random.choice(O_MISSED)}\n")  # if attack misses
                    active = True

        # if either health levels equal or drop below 0, round ends
        if PLAYER.health <= 0:
            print("Oh no, you have been defeated!")
            return False
        if OPPONENT.health <= 0:
            if type(OPPONENT) == Boss:
                print(f"Congradulations, {PLAYER} (you) have defeated {OPPONENT}!")
                print("You win, thanks for playing.")
                return None
            print(f"You have defeated {OPPONENT}!")
            # health and money are boosted
            h = 50
            m = random.randint(5, 50)
            PLAYER.health += h
            PLAYER.money += m
            print(f"+{h} health")
            print(f"+{m} coins")
            return True

    def create_field(self, test=False):  # maybe make field global?
        """Creates field that player can move around."""
        size = 10  # size of field, both length and height, makes a square
        field = []
        for i in range(size):  # creates the field
            field.append([])
            for j in range(size):
                field[i].append(None)
        if not test:
            field[X][Y] = PLAYER  # 0,0 reserved for player
            for row in range(len(field)):
                for col in range(len(field)):
                    chance = random.random()
                    if field[row][col] is None:
                        if chance <= .20:
                            field[row][col] = Character(* random.choice(CHARACTERS))
                        elif .20 < chance <= .45:
                            field[row][col] = Item(* random.choice(ITEMS))
                        elif .45 < chance <= .75:
                            field[row][col] = Shop(random.choice(LOCATIONS))
                            for i in range(random.randint(2, 5)):
                                field[row][col].items.append(Item(* random.choice(ITEMS)))
                        else:
                            field[row][col] = None  # about 25% of field is unfilled (None)
            # adds one boss
            field[random.randint(1, size - 1)][random.randint(1, size - 1)] = Boss(* random.choice(BOSSES))
            field[X][Y] = None  # removes the player object representation
        else:
            # for testing
            s = Shop(random.choice(LOCATIONS))
            s.items.append(Item(*random.choice(ITEMS)))
            # field[0][2] = Item(* random.choice(ITEMS))
            # field[0][3] = s
            field[0][4] = Character(* CHARACTERS[0])
            # field[0][4] = Boss(* BOSSES[0])
        return field

    def choose_direction(self):
        print("North[w], East[a], South[s], or West[d]\n.\n.\n.")
        # direction = input("Which way do you want to go? ").strip().lower()
        # print('\n')
        while True:
            direction = input("Which way do you want to go? ").strip().lower()
            print('\n')
            if direction == '':
                print("Goodbye.")
                return None
            if direction == 'w':  # north
                return -1, 0
            if direction == 'a':  # west
                return 0, -1
            if direction == 's':  # south
                return 1, 0
            if direction == 'd':  # east
                return 0, 1
            else:
                print("Please enter a valid key.")

    def walk(self, field: List[List], d: tuple):
        if d is None:
            return None  # choose_direction returns None, ends game
        global X, Y, OPPONENT
        x, y = d  # new movement vector
        old = X, Y  # old pos
        X += x
        Y += y
        new = X, Y  # new pos
        # print(type(event))
        if not 0 <= new[0] <= len(field[0]) - 1 or not 0 <= new[1] <= len(field) - 1:  # if either x, y out of bounds
            print(f"You cannot go any further in that direction, current position {old}")  # FIXME: take out current pos
            X, Y = old
        event = field[X][Y]  # content of next pos
        if type(event) == Item:
            if PLAYER.add_item(event):
                field[X][Y] = None  # player takes item
        if type(event) == Shop:
            # print(event.items)
            event.greeting()
        if type(event) == Character or type(event) == Boss:
            OPPONENT = event
            b = self.battle()  # maybe fixed
            if b:
                field[X][Y] = None
                return True  # maybe fixed
            if b == 'ran':
                return True
            if not b:
                return None  # loss
            else:
                return None  # beats boss
        if event is None:
            pass  # no event at this pos
        return True  # arbitrary, allows a return of None to end the game

    # FIXME: add Map item that can reveal nearby areas
    # FIXME: create player movement with arrow-key inputs; may be impossible
    # FIXME: maybe add a create-your-own-character option
    # FIXME: refactor battle()


def character_graphic():
    screen = t.Screen()
    # character = t.Turtle()
    screen.bgpic()  # add pic name
    screen.update()
    # character.fd(100)
    screen.exitonclick()

def main():
    """
    Runs the simulation.
    """
    print("Welcome to River's Adventure Simulator v3!")
    print("Collect items, battle enemies, and defeat the boss the win.")
    print("--> If, at any time, you would like to quit, press [enter] <--")
    print("--> Use [w][a][s][d] to move <--\n")

    
    # runs game
    game = Game()
    field = game.create_field()  # pass True in if testing
    game.print_characters()
    game.choose_character()
    d = True
    while d is not None:
        # print(field)
        d = game.choose_direction()
        w = game.walk(field, d)
        if w is None:  # loss by enemy or win against boss
            return None
    
    # for graphics to be implemented in the future
    # character_graphic()

main()
