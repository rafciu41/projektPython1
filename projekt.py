from dataclasses import dataclass
from typing import List
from pydantic import BaseModel, validator


class InvalidInput(Exception):
    pass


@dataclass
class Item:
    name: str
    description: str
    price: float


@dataclass
class Room:
    name: str
    description: str
    items: List[Item]


class Player(BaseModel):
    name: str
    email: str

    @validator('email')
    def validate_email(cls, value):
        if '@' not in value:
            raise InvalidInput("Invalid email address")
        return value


def view_inventory():
    print("Your inventory:")
    # TODO: Implement player inventory


def quit_game():
    print("Goodbye!")
    exit()


class AdventureGame:
    def __init__(self):
        self.rooms = [
            Room(name="Entrance Hall", description="A dusty old entrance hall", items=[
                Item(name="Key", description="A rusty old key", price=0),
                Item(name="Sword", description="A shiny new sword", price=50),
            ]),
            Room(name="Library", description="A quiet room filled with books", items=[
                Item(name="Book", description="A dusty old book", price=10),
            ]),
            Room(name="Treasure Room", description="A room filled with treasure", items=[
                Item(name="Gold Coin", description="A shiny gold coin", price=100),
                Item(name="Diamond", description="A sparkling diamond", price=500),
            ]),
        ]
        self.current_room = self.rooms[0]
        self.player = None

    def start(self):
        print("Welcome to the Adventure Game!")
        while True:
            print("Please enter your name:")
            name = input().strip()
            print("Please enter your email:")
            email = input().strip()
            try:
                self.player = Player(name=name, email=email)
                break
            except InvalidInput as e:
                print(e)

        self.play()


    def play(self):
        print(f"Welcome, {self.player.name}!")
        while True:
            print(f"You are in the {self.current_room.name}.")
            print(self.current_room.description)
            print("What would you like to do?")
            print("1. Look around")
            print("2. Move to another room")
            print("3. View inventory(soon)")
            print("4. Quit")
            choice = input().strip()
            try:
                if choice == "1":
                    self.look_around()
                elif choice == "2":
                    self.move()
                elif choice == "3":
                    view_inventory()
                elif choice == "4":
                    quit_game()
                else:
                    raise InvalidInput("Invalid choice")
            except InvalidInput as e:
                print(e)

    def look_around(self):
        print(f"You see {len(self.current_room.items)} items:")
        for item in self.current_room.items:
            print(f"{item.name}: {item.description}")

    def move(self):
        print("Which room would you like to move to?")
        for i, room in enumerate(self.rooms):
            if room != self.current_room:
                print(f"{i+1}. {room.name}")
        choice = input().strip()
        try:
            room_num = int(choice) - 1
            if room_num < 0 or room_num >= len(self.rooms) or self.rooms[room_num] == self.current_room:
                raise InvalidInput("Invalid choice")
            self.current_room = self.rooms[room_num]
        except ValueError:
            raise InvalidInput("Invalid choice")


game = AdventureGame()
game.start()
