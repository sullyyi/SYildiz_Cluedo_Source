import random

# Room layout
ROOMS = {
    "Study":        [(0,0), (1,0), (0,1), (1,1)],
    "Hall":         [(4,0), (5,0), (4,1), (5,1)],
    "Lounge":       [(8,0), (9,0), (8,1), (9,1)],
    "Library":      [(0,4), (1,4), (0,5), (1,5)],
    "Gaming Room":  [(4,4), (5,4), (4,5), (5,5)],
    "Dining Room":  [(8,4), (9,4), (8,5), (9,5)],
    "Theater":      [(0,8), (1,8), (0,9), (1,9)],
    "Fireplace":    [(4,8), (5,8), (4,9), (5,9)],
    "Kitchen":      [(8,8), (9,8), (8,9), (9,9)]
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
        self.eliminated = False

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
                num = int(input("How many players (2–6)? "))
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
                y -= 1
            elif direction == "DOWN":
                y += 1
            elif direction == "LEFT":
                x -= 1
            elif direction == "RIGHT":
                x += 1
        player.position = (x, y)

    def check_room_entry(self, pos):
        for room, tiles in ROOMS.items():
            if pos in tiles:
                return room
        return None

    def will_move_off_board(self, position, direction, steps):
        x, y = position
        if direction == "UP":
            return y - steps < 0
        elif direction == "DOWN":
            return y + steps >= 10
        elif direction == "LEFT":
            return x - steps < 0
        elif direction == "RIGHT":
            return x + steps >= 10
        return True

    def suggest(self, player, room):
        print(f"{player.name}, make a suggestion in the {room}:")
        char = input("  Character: ").strip()
        weapon = input("  Weapon: ").strip()

        print(f"You suggested: {char} with the {weapon} in the {room}")

        for p in self.players:
            if p.name.lower() == char.lower() and p != player:
                p.position = next(iter(ROOMS[room]))
                print(f"{p.name} has been moved to the {room} as part of the suggestion.")
                break

        refuted = False
        current_index = self.players.index(player)
        for i in range(1, len(self.players)):
            next_player = self.players[(current_index + i) % len(self.players)]
            matching_cards = [card for card in next_player.cards if card in {char, weapon, room}]
            if matching_cards:
                shown_card = random.choice(matching_cards)
                print(f"{next_player.name} refuted your suggestion by showing you the card: {shown_card}")
                refuted = True
                break

        if not refuted:
            print("No one could refute your suggestion.")

    def accuse(self, player):
        print(f"{player.name}, make an accusation!")
        char = input("  Character: ").strip()
        weapon = input("  Weapon: ").strip()
        room = input("  Room: ").strip()

        print(f"\nYou accused: {char} with the {weapon} in the {room}")

        if (char, weapon, room) == self.solution:
            print(f"\n {player.name} made a correct accusation and wins the game! 🎉")
            exit()
        else:
            print(f"\n Wrong accusation. {player.name} is eliminated from making further turns.")
            player.eliminated = True

    def play_turn(self, player):
        if player.eliminated:
            print(f"{player.name} has been eliminated and cannot take a turn.")
            return

        print(f"\n--- {player.name}'s Turn ---")
        current_pos = player.position
        room_name = self.check_room_entry(current_pos)
        pos_display = f"{current_pos} ({room_name})" if room_name else str(current_pos)
        print(f"Current position: {pos_display}")

        input(f"{player.name}, press Enter to roll the die...")
        roll = self.roll_die()
        print(f"You rolled a {roll}.")

        while True:
            move = input("Enter your move (e.g., UP 2), or type 'CARDS' to view your hand: ").strip().upper().split()

            if not move:
                print("Please enter a command.")
                continue

            if move[0] == "CARDS":
                print(f"\nYour cards: {player.cards}\n")
                continue

            if move[0] == "ACCUSE":
                self.accuse(player)
                return

            if len(move) == 2 and move[0] in {"UP", "DOWN", "LEFT", "RIGHT"}:
                try:
                    direction, steps = move[0], int(move[1])
                except ValueError:
                    print("Steps must be a number.")
                    continue

                if self.will_move_off_board(player.position, direction, steps):
                    print("That move would take you off the board. Try again.")
                    continue

                self.move_player(player, direction, steps)
                new_pos = player.position
                room = self.check_room_entry(new_pos)
                pos_display = f"{new_pos} ({room})" if room else str(new_pos)
                print(f"You have moved to {pos_display}")
                break

            elif move[0].startswith("SECRET_PASSAGE_TO_"):
                dest_room = move[0].replace("SECRET_PASSAGE_TO_", "").title().replace("_", " ")
                current_room = self.check_room_entry(player.position)
                if current_room and SECRET_PASSAGES.get(current_room) == dest_room:
                    print(f"{player.name} uses a secret passage to the {dest_room}.")
                    player.position = next(iter(ROOMS[dest_room]))
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
            input("Press Enter to end your turn...")
            self.current_player_idx = (self.current_player_idx + 1) % self.num_players

if __name__ == "__main__":
    game = CluedoGame()
    game.run()
