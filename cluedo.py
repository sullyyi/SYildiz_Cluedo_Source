import random

#room layout, see excel sheet for clarity and movement
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
#players can move from one room to another without using dice
SECRET_PASSAGES = {
    "Study": "Kitchen",
    "Kitchen": "Study",
    "Lounge": "Library",
    "Library": "Lounge",
}

CHARACTERS = ["Sherlock", "Watson", "Daniel", "Ivy", "James", "Lilith"]
WEAPONS = ["Trophy", "Iron", "Bust", "Fire Poker", "Meat Tenderizer", "Rat Poison"]
ROOM_NAMES = list(ROOMS.keys())

#players start at static positions
START_POSITIONS = {
    "Sherlock": (2, 1),
    "Watson": (2, 4),
    "Daniel": (2, 8),
    "Ivy": (7, 0),
    "James": (7, 4),
    "Lilith": (7, 8),
}

class Player:
    def __init__(self, name, position, is_ai = False):
        self.name = name
        self.position = position
        self.cards = []
        self.eliminated = False
        #ai class properties, knowledge base, history base for deductions
        self.is_ai = is_ai
        self.known_cards = {}
        self.not_have = {}
        self.possible_solution = {
            "character": set(CHARACTERS),
            "weapon": set(WEAPONS),
            "room": set(ROOM_NAMES),
        }
        self.suggestion_history = []

class CluedoGame:
    def __init__(self):
        self.num_players = self.ask_player_count()
        print(f"{self.num_players -1} human(s), and 1 AI will be playing! Good luck!")
        self.current_player_idx = 0
        self.solution = self.select_solution()
        self.players = self.create_players()
        self.deal_cards()
    
    def create_players(self):
        players = []
        for i in range(self.num_players):
            name = CHARACTERS[i]
            position = START_POSITIONS[name]
            is_ai = (i == self.num_players - 1) #only one ai right now
            players.append(Player(name, position, is_ai = is_ai))
        return players

    def ask_player_count(self):
        while True:
            try:
                num = int(input("How many players (2–6)? "))
                if 2 <= num <= 6:
                    return num
                else:
                    print("Please enter a number between 2 and 6.")
            except ValueError: #in case a number out of range is chosen
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

    def check_room_entry(self, pos): #check if a player entered the room, return the new location
        for room, tiles in ROOMS.items():
            if pos in tiles:
                return room
        return None

    def will_move_off_board(self, position, direction, steps): # to check if a player is moving off the board, dont allow it
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
        char = input("  Character: ").strip() #choose a player
        weapon = input("  Weapon: ").strip() #choose a weapon
        room = input("  Room: ").strip() #chooses the room youre in

        print(f"\nYou accused: {char} with the {weapon} in the {room}")

        if (char, weapon, room) == self.solution:
            print(f"\n {player.name} made a correct accusation and wins the game!")
            exit()
        else:
            print(f"\n Wrong accusation. {player.name} is eliminated from making further turns.")
            player.eliminated = True

    def play_turn(self, player):
        if player.eliminated: #SKIP the player turn if they are eliminated, round robin to the next player
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

            if not move: #fixes incorrect commands
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
                    print("Steps must be a number!")
                    continue

                if self.will_move_off_board(player.position, direction, steps): #check for off range
                    print("That move would take you off the board. Try again in range.")
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
            #ai turn
            if current_player.is_ai:
                self.ai_play_turn(current_player)
            else:
                self.play_turn(current_player)
            #handling end turn and time for ai turns for readability
            if current_player.is_ai:
                input("Press Enter to continue AI turn...")
            else:                
                input("Press Enter to end your turn...")
            self.current_player_idx = (self.current_player_idx + 1) % self.num_players
    
    #ai play turn and movement
    def ai_play_turn(self, player):
        print(f"{player.name} (AI PLAYER) is thinking about what to do...")
        input("Press ENTER to continue the AI turn...") #pause for human logic
        #check the room its in currently
        room = self.check_room_entry(player.position)
        if room:
            self.ai_suggest(player, room)
            input("AI wants to consider an accusation...")
            self.ai_accuse_if_confident(player)
            return
    #moving towards a room
        print(f"{player.name} (AI PLAYER) is not in a room, and has chosen a room to move towards...")
        input("AI is about to move... Press ENTER to continue") #pause for human logic
        suggested_rooms = {entry[2] for entry in player.suggestion_history} #to ensure the ai doesnt visit rooms it already suggested, no repitition unless its forced
        unvisited_rooms = list(player.possible_solution["room"] - suggested_rooms)
        if not unvisited_rooms:
            unvisited_rooms = list(player.possible_solution["room"]) #in case all rooms are visited
        target_room = random.choice(unvisited_rooms)
        target_tiles = ROOMS[target_room]
    #ai picks a tile from the room a2s a target to begin closest guidance
        target_x, target_y = random.choice(target_tiles)
        current_x, current_y = player.position
    #ai moves one step from difference in grid positions
        if abs(target_x - current_x) > abs(target_y - current_y):
            direction = "RIGHT" if target_x > current_x else "LEFT"
        else:
            direction = "DOWN" if target_y > current_y else "UP"

        if self.will_move_off_board(player.position, direction, 1):
            print(f"{player.name} (AI PLAYER) cannot move {direction}, skipping turn!")
            return
        self.move_player(player, direction, 1)
        new_pos = player.position
        new_room = self.check_room_entry(new_pos)

        print(f"{player.name} (AI PLAYER) has moved {direction} to {new_pos}")
        input("Press ENTER to continue the AI PLAYER movement")

        if new_room:
            print(f"{player.name} (AI PLAYER) has entered the {new_room}.")
            self.ai_suggest(player, new_room)
            input("Press ENTER to continue the AI turn...")
            self.ai_accuse_if_confident(player)
        else:
            print(f"{player.name} (AI PLAYER) is still roaming the halls...")

    #ai confidence with accusations
    def ai_accuse_if_confident(self, player):
        char_set = player.possible_solution["character"]
        weapon_set = player.possible_solution["weapon"]
        room_set = player.possible_solution["room"]

        if len(char_set) == 1 and len(weapon_set) == 1 and len(room_set) == 1:
            char = next(iter(char_set))
            weapon = next(iter(weapon_set))
            room = next(iter(room_set))

            print(f"\n{player.name} (AI PLAYER) is making an accusation!: {char} with the {weapon} in the {room}")
        
            if (char, weapon, room) == self.solution:
                print(f"\n{player.name}( AI PLAYER) has guessed the correct accusation and wins!!!")
                exit()
            else:        
                print(f"\n{player.name} (AI PLAYER) was wrong, and is ELIMINATED!")
                player.eliminated = True

    #ai suggestion capability
    def ai_suggest(self, player, room):
        print(f"{player.name} (AI PLAYER) is making a suggestion in the {room}...")
        #choosing an item and character from the difference of possibilities
        char = random.choice(list(player.possible_solution["character"] - set(player.cards)))
        weapon = random.choice(list(player.possible_solution["weapon"] - set(player.cards)))
        print(f"{player.name} suggests: {char} with the {weapon} in the {room}")
        #move the suggested character into the room
        for p in self.players:
            if p.name.lower() == char.lower() and p != player:
                p.position = next(iter(ROOMS[room]))
                print(f"{p.name} has been moved into {room} because of the suggestion.")
                break
        
        suggestion_set = {char, weapon, room}
        refuted = False
        current_index = self.players.index(player)

        for i in range(1, len(self.players)):
            next_player = self.players[(current_index + i) % len(self.players)]
            matching_cards = [card for card in next_player.cards if card in suggestion_set]
            if matching_cards:
                shown_card = random.choice(matching_cards)
                print(f"{next_player.name} refutes this suggestion by showing a card.")
                refuted = True

                #to update the ai known information base
                if next_player.name not in player.known_cards:
                    player.known_cards[next_player.name] = set()
                player.known_cards[next_player.name].add(shown_card)

                #to remove the shown cards from the future probable solutions
                for category in player.possible_solution:
                    player.possible_solution[category].discard(shown_card)
                
                #to log the information
                player.suggestion_history.append((char, weapon, room, next_player.name))
                break
            else:
                #if the refute is false, they dont have any of the 3
                if next_player.name not in player.not_have:
                    player.not_have[next_player.name] = set()
                player.not_have[next_player.name].update(suggestion_set)


        if not refuted:
            print("No player can refute this suggestion.")
            player.suggestion_history.append((char, weapon, room, None))

if __name__ == "__main__":
    game = CluedoGame()
    game.run()
