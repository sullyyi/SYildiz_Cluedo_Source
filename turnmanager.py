import random
from movement import move_player, check_room_entry, will_move_off_board
from configurations import SECRET_PASSAGES, ROOMS
from player import Player
from tracker import display_and_save_tracker

class TurnManager:
    def __init__(self, game):
        self.game = game  # gives access to players, solution, etc.

    def play_turn(self, player):
        if player.eliminated:
            print(f"{player.name} has been eliminated and cannot take a turn.")
            return

        print(f"\n--- {player.name}'s Turn ---")
        current_pos = player.position
        room_name = check_room_entry(current_pos)
        pos_display = f"{current_pos} ({room_name})" if room_name else str(current_pos)
        print(f"Current position: {pos_display}")

        input(f"{player.name}, press Enter to roll the die...")
        roll = self.game.roll_die()
        print(f"You rolled a {roll}.")

        while True:
            move = input("Enter your move (e.g., UP 2), 'CARDS' to view your hand, 'TRACK' to see info, 'ACCUSE' to make an accusation: ").strip().upper().split()

            if not move:
                print("Please enter a command.")
                continue

            if move[0] == "CARDS":
                print(f"\nYour cards: {player.cards}\n")
                continue

            if move[0] == "TRACK":
                display_and_save_tracker(player)
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

                if will_move_off_board(player.position, direction, steps):
                    print("That move will take you off the board. Try again in range.")
                    continue

                move_player(player, direction, steps)
                new_pos = player.position
                room = check_room_entry(new_pos)
                pos_display = f"{new_pos} ({room})" if room else str(new_pos)
                print(f"You have moved to {pos_display}")
                break

            elif move[0].startswith("SECRET_PASSAGE_TO_"):
                dest_room = move[0].replace("SECRET_PASSAGE_TO_", "").title().replace("_", " ")
                current_room = check_room_entry(player.position)
                if current_room and SECRET_PASSAGES.get(current_room) == dest_room:
                    print(f"{player.name} uses a secret passage to the {dest_room}.")
                    player.position = next(iter(ROOMS[dest_room]))
                    self.suggest(player, dest_room)
                else:
                    print("Invalid secret passage.")
                break
            else:
                print("Invalid move input.")

        new_room = check_room_entry(player.position)
        if new_room:
            print(f"You entered the {new_room}.")
            self.suggest(player, new_room)

    def ai_play_turn(self, player):
        print(f"\n--- {player.name} (AI PLAYER) Turn ---")
        if player.eliminated:
            print(f"{player.name} is eliminated and skips their turn.")
            return

        input("Press ENTER to begin AI turn...")

        current_room = check_room_entry(player.position)
        if current_room:
            print(f"{player.name} is currently in the {current_room}.")
            self.ai_suggest(player, current_room)
            input("Press ENTER to continue...")
            self.ai_accuse_if_confident(player)
            return

        print(f"{player.name} is in the hallway and deciding where to go...")

        possible_rooms = list(player.possible_solution["room"])
        visited_rooms = {entry[2] for entry in player.suggestion_history}
        unvisited_rooms = list(set(possible_rooms) - visited_rooms)

        target_rooms = unvisited_rooms if unvisited_rooms else possible_rooms
        target_room = random.choice(target_rooms)
        target_tiles = ROOMS[target_room]

        target_x, target_y = random.choice(target_tiles)
        current_x, current_y = player.position
        dx, dy = target_x - current_x, target_y - current_y

        if abs(dx) > abs(dy):
            direction = "RIGHT" if dx > 0 else "LEFT"
        else:
            direction = "DOWN" if dy > 0 else "UP"

        if will_move_off_board(player.position, direction, 1):
            print(f"{player.name} can't move {direction} this turn.")
            return

        move_player(player, direction, 1)
        new_pos = player.position
        print(f"{player.name} moved {direction} to {new_pos}")

        new_room = check_room_entry(new_pos)
        if new_room:
            print(f"{player.name} has entered the {new_room}.")
            self.ai_suggest(player, new_room)
            self.ai_accuse_if_confident(player)
        else:
            print(f"{player.name} is still in the hallway.")

    def ai_suggest(self, player, room):
        print(f"{player.name} (AI PLAYER) is making a suggestion in the {room}...")

        suggestion = player.choose_suggestion()
        if not suggestion:
            print("[AI ERROR] Could not generate suggestion.")
            return

        char, weapon, room = suggestion
        print(f"{player.name} suggests: {char} with the {weapon} in the {room}")

        for p in self.game.players:
            if p.name.lower() == char.lower() and p != player:
                p.position = next(iter(ROOMS[room]))
                print(f"{p.name} has been moved to the {room} as part of the suggestion.")
                break

        suggestion_set = {char, weapon, room}
        refuted = False
        refuter_name = None
        card_shown = None
        current_index = self.game.players.index(player)

        for i in range(1, len(self.game.players)):
            next_player = self.game.players[(current_index + i) % len(self.game.players)]
            matching_cards = [card for card in next_player.cards if card in suggestion_set]

            if matching_cards:
                card_shown = random.choice(matching_cards)
                print(f"{next_player.name} refutes this suggestion by showing a card.")
                refuted = True
                refuter_name = next_player.name
                break

        player.observe_suggestion(char, weapon, room, refuter_name, [p.name for p in self.game.players])
        if refuted:
            player.update_knowledge_from_refutation(player.name, suggestion, refuter_name, card_shown)
        else:
            print("No player could refute this suggestion.")


    def ai_accuse_if_confident(self, player):
        accusation = player.make_accusation()
        if accusation is None:
            print(f"{player.name} (AI PLAYER) is not confident enough to accuse yet.")
            return

        char, weapon, room = accusation
        print(f"\n{player.name} (AI PLAYER) is making an accusation: {char} with the {weapon} in the {room}")

        if (char, weapon, room) == self.game.solution:
            print(f"\n{player.name} (AI PLAYER) guessed correctly and wins the game!!!")
            exit()
        else:
            print(f"\n{player.name} (AI PLAYER) was wrong and is now ELIMINATED!")
            player.eliminated = True
            
    def suggest(self, player, room):
        print(f"{player.name}, make a suggestion in the {room}:")
        char = input("  Character: ").strip()
        weapon = input("  Weapon: ").strip()

        print(f"You suggested: {char} with the {weapon} in the {room}")

        for p in self.game.players:
            if p.name.lower() == char.lower() and p != player:
                p.position = next(iter(ROOMS[room]))
                print(f"{p.name} has been moved to the {room} as part of the suggestion.")
                break

        refuted = False
        current_index = self.game.players.index(player)
        for i in range(1, len(self.game.players)):
            next_player = self.game.players[(current_index + i) % len(self.game.players)]
            matching_cards = [card for card in next_player.cards if card in {char, weapon, room}]
            if matching_cards:
                shown_card = random.choice(matching_cards)
                print(f"{next_player.name} refuted your suggestion by showing you the card: {shown_card}")
                refuted = True
                break

        if not refuted:
            print("No one could refute your suggestion.")
        #log for tracking
        player.suggestion_history.append((char, weapon, room, next_player.name if refuted else None))


    def accuse(self, player):
        print(f"{player.name}, make an accusation!")
        char = input("  Character: ").strip()
        weapon = input("  Weapon: ").strip()
        room = input("  Room: ").strip()

        print(f"\nYou accused: {char} with the {weapon} in the {room}")

        if (char, weapon, room) == self.game.solution:
            print(f"\n{player.name} made a correct accusation and wins the game!")
            exit()
        else:
            print(f"\nWrong accusation. {player.name} is eliminated from making further turns.")
            player.eliminated = True

    def run(self):
        while True:
            current_player = self.game.players[self.game.current_player_idx]
            if current_player.is_ai:
                self.ai_play_turn(current_player)
                input("Press Enter to continue AI turn...")
            else:
                self.play_turn(current_player)
                input("Press Enter to end your turn...")
            self.game.current_player_idx = (self.game.current_player_idx + 1) % self.game.num_players
