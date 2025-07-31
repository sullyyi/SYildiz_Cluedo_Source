import random

# Define room layout using a 10x10 grid
ROOMS = {
    "Study": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "Hall": [(0, 4), (0, 5), (1, 4), (1, 5)],
    "Lounge": [(0, 8), (0, 9), (1, 8), (1, 9)],
    "Library": [(4, 0), (5, 0), (4, 1), (5, 1)],
    "Gaming Room": [(4, 4), (5, 4), (4, 5), (5, 5)],
    "Dining Room": [(4, 8), (5, 8), (4, 9), (5, 9)],
    "Theater": [(8, 0), (9, 0), (8, 1), (9, 1)],
    "Fireplace": [(8, 4), (9, 4), (8, 5), (9, 5)],
    "Kitchen": [(8, 8), (9, 8), (8, 9), (9, 9)],
}

DOORS = {
    "Study": [(2, 1)],
    "Hall": [(2, 4)],
    "Lounge": [(2, 8)],
    "Library": [(3, 0)],
    "Gaming Room": [(3, 4)],
    "Dining Room": [(3, 8)],
    "Theater": [(7, 0)],
    "Fireplace": [(7, 4)],
    "Kitchen": [(7, 8)],
}

SECRET_PASSAGES = {
    "Study": "Kitchen",
    "Kitchen": "Study",
    "Lounge": "Library",
    "Library": "Lounge",
}

CHARACTERS = ["Sherlock", "Watson", "Daniel", "Ivy", "James", "Lilith"]
WEAPONS = ["Trophy", "Iron", "Bust", "Fire Poker", "Meat Tenderizer", "Rat Poison"]
ROOM_NAMES = list(ROOMS.keys())

START_POSITIONS = {
    "Sherlock": (2, 1),
    "Watson": (2, 4),
    "Daniel": (2, 8),
    "Ivy": (7, 0),
    "James": (7, 4),
    "Lilith": (7, 8),
}

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.cards = []

class CluedoGame:
    def __init__(self):
        self.num_players = self.ask_player_count()
        self.players = [Player(CHARACTERS[i], START_POSITIONS[CHARACTERS[i]]) for i in range(self.num_players)]
        self.current_player_idx = 0
        self.solution = self.select_solution()
        self.deal_cards()

    def ask_player_count(self):
        while True:
            try:
                num = int(input("How many players (2-6)? "))
                if 2 <= num <= 6:
                    return num
                else:
                    print("Please enter a number between 2 and 6.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def select_solution(self):
        return (
            random.choice(CHARACTERS),
            random.choice(WEAPONS),
            random.choice(ROOM_NAMES)
        )

    def deal_cards(self):
        full_deck = [card for card in CHARACTERS + WEAPONS + ROOM_NAMES if card not in self.solution]
        random.shuffle(full_deck)
        for i, card in enumerate(full_deck):
            self.players[i % len(self.players)].cards.append(card)

    def roll_die(self):
        return random.randint(1, 6)

    def move_player(self, player, direction, steps):
        x, y = player.position
        for _ in range(steps):
            if direction == "UP":
                x -= 1
            elif direction == "DOWN":
                x += 1
            elif direction == "LEFT":
                y -= 1
            elif direction == "RIGHT":
                y += 1
        player.position = (x, y)

    def check_room_entry(self, pos):
        for room, doors in DOORS.items():
            if pos in doors:
                return room
        return None

    def suggest(self, player, room):
        print(f"{player.name}, make a suggestion in the {room}:")
        char = input("  Character: ").strip()
        weapon = input("  Weapon: ").strip()
        print(f"You suggested: {char} with the {weapon} in the {room}")
        # Logic to move the suggested character and weapon would go here

    def will_move_off_board(self, position, direction, steps):
        x, y = position
        if direction == "UP":
            return x - steps < 0
        elif direction == "DOWN":
            return x + steps >= 10
        elif direction == "LEFT":
            return y - steps < 0
        elif direction == "RIGHT":
            return y + steps >= 10
        return True

    def play_turn(self, player):
        current_pos = player.position
        room_name = self.check_room_entry(current_pos)
        pos_display = f"{current_pos} ({room_name})" if room_name else str(current_pos)
        print(f"Current position: {pos_display}")

        input(f"{player.name}, press Enter to roll the die...")
        roll = self.roll_die()
        print(f"You rolled a {roll}.")

        while True:
            move = input("Enter your move (e.g., UP 2): ").strip().upper().split()
            if len(move) == 2 and move[0] in {"UP", "DOWN", "LEFT", "RIGHT"}:
                direction, steps = move[0], int(move[1])
                if self.will_move_off_board(player.position, direction, steps):
                    print("That move would take you off the board. Try again.")
                    continue
                self.move_player(player, direction, steps)
                break
            elif move[0].startswith("SECRET_PASSAGE_TO_"):
                dest_room = move[0].replace("SECRET_PASSAGE_TO_", "").title().replace("_", " ")
                current_room = self.check_room_entry(player.position)
                if current_room and SECRET_PASSAGES.get(current_room) == dest_room:
                    print(f"{player.name} uses a secret passage to the {dest_room}.")
                    player.position = DOORS[dest_room][0]
                    self.suggest(player, dest_room)
                else:
                    print("Invalid secret passage.")
                break
            else:
                print("Invalid move input.")

        new_room = self.check_room_entry(player.position)
        if new_room:
            print(f"You entered the {new_room}.")
            self.suggest(player, new_room)

    def run(self):
        while True:
            current_player = self.players[self.current_player_idx]
            self.play_turn(current_player)
            self.current_player_idx = (self.current_player_idx + 1) % self.num_players

if __name__ == "__main__":
    game = CluedoGame()
    game.run()
