import random
from player import Player
from turnmanager import TurnManager
from configurations import * 
from movement import move_player, check_room_entry, will_move_off_board


class CluedoGame:
    def __init__(self):
        self.num_players = self.ask_player_count()
        print(f"{self.num_players -1} human(s), and 1 AI will be playing! Good luck!")
        self.current_player_idx = 0
        self.solution = self.select_solution()
        self.players = self.create_players()
        self.deal_cards()
        self.debug_print_ai_hand() #for presentation purposes
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
    def debug_print_ai_hand(self): #to help during presentation
        for player in self.players:
            if player.is_ai:
                print(f"[FOR PRESENTATION] {player.name} (AI PLAYER) was dealt: {player.cards}")

if __name__ == "__main__":
    #hand control to the turn manager.  The turn manager handles the game loop, prompting each player (human or AI)
    game = CluedoGame()
    TurnManager(game).run()
