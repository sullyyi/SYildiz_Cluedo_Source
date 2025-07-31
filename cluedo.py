#!/usr/bin/env python3
#2025
"""
Cluedo Game - Part 1 (Text-based)

This script contains the basic skeleton for a Cluedo game. It defines the core
data structures (characters, weapons, rooms), sets up the game board, and
provides a command-line interface for player interaction. Detailed game logic
(such as validating moves, handling suggestions and refutations) will need to
be implemented as you continue development.

To run the game:
    python cluedo.py
"""
import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass(frozen=True)
class Character:
    """Represents a Cluedo character."""
    name: str
    start_position: Tuple[int, int]

@dataclass(frozen=True)
class Weapon:
    """Represents a Cluedo weapon."""
    name: str

@dataclass(frozen=True)
class Room:
    """Represents a room in the mansion."""
    name: str
    position: Tuple[int, int]
    connections: List[str] = field(default_factory=list)
    secret_passage: Optional[str] = None

@dataclass
class Player:
    """Represents a player in the game."""
    character: Character
    position: Tuple[int, int]
    cards: List[str] = field(default_factory=list)

class Board:
    """Represents the Cluedo game board as a grid/graph."""
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.graph: Dict[str, List[str]] = {}
        self.setup_rooms()

    def setup_rooms(self):
        """Initializes rooms, connections and secret passages."""
        # Example room layout with positions and secret passages
        room_data = [
            ('Study', (0, 0), ['Hall'], 'Kitchen'),
            ('Hall', (0, 2), ['Study', 'Lounge'], None),
            ('Lounge', (0, 4), ['Hall'], 'Conservatory'),
            ('Library', (2, 0), ['Billiard Room'], None),
            ('Billiard Room', (2, 2), ['Library', 'Dining Room'], None),
            ('Dining Room', (2, 4), ['Billiard Room', 'Kitchen'], None),
            ('Conservatory', (4, 0), ['Ballroom'], 'Lounge'),
            ('Ballroom', (4, 2), ['Conservatory', 'Kitchen'], None),
            ('Kitchen', (4, 4), ['Ballroom'], 'Study'),
        ]
        for name, pos, adj, secret in room_data:
            self.rooms[name] = Room(name=name, position=pos,
                                    connections=adj, secret_passage=secret)
        # Build graph for adjacency
        for room_name, room in self.rooms.items():
            self.graph[room_name] = room.connections

    def move(self, start_room: str, end_room: str) -> bool:
        """Validate movement from start_room to end_room."""
        return end_room in self.graph.get(start_room, [])

class CluedoGame:
    """Main class for managing the game state and interactions."""
    def __init__(self):
        self.characters = self._init_characters()
        self.weapons = self._init_weapons()
        self.board = Board()
        self.solution = self._select_solution()
        self.players: List[Player] = []
        self.current_player_index = 0
        self._deal_cards()

    def _init_characters(self) -> List[Character]:
        """Initialize Cluedo characters with starting positions."""
        # Starting positions can be refined according to your board design
        return [
            Character('Miss Scarlett', (0, 1)),
            Character('Colonel Mustard', (1, 4)),
            Character('Mrs. White', (4, 3)),
            Character('Reverend Green', (3, 0)),
            Character('Mrs. Peacock', (1, 0)),
            Character('Professor Plum', (4, 1)),
        ]

    def _init_weapons(self) -> List[Weapon]:
        """Initialize Cluedo weapons."""
        return [
            Weapon('Candlestick'),
            Weapon('Dagger'),
            Weapon('Lead Pipe'),
            Weapon('Revolver'),
            Weapon('Rope'),
            Weapon('Wrench'),
        ]

    def _select_solution(self) -> Dict[str, str]:
        """Randomly select the murder solution."""
        character = random.choice(self.characters).name
        weapon = random.choice(self.weapons).name
        room = random.choice(list(self.board.rooms.keys()))
        return {'character': character, 'weapon': weapon, 'room': room}

    def _deal_cards(self):
        """Deal remaining cards to players (to be implemented)."""
        # Combine characters, weapons, and rooms excluding the solution cards
        pass  # Logic for dealing cards will go here

    def add_player(self, character_name: str):
        """Add a new player to the game."""
        character = next((c for c in self.characters if c.name == character_name), None)
        if character:
            self.players.append(Player(character=character, position=character.start_position))
        else:
            raise ValueError(f"Character '{character_name}' not found")

    def roll_dice(self) -> int:
        """Simulate rolling a six-sided die."""
        return random.randint(1, 6)

    def play_turn(self, player: Player):
        """Handle a single player's turn (dice roll, movement, suggestion)."""
        # This method should prompt for user input to move and make suggestions.
        pass

    def run(self):
        """Main game loop."""
        print("Welcome to Cluedo!\n")
        # Setup players based on user input
        for character in self.characters:
            use_character = input(f"Add player for {character.name}? (y/n): ").strip().lower()
            if use_character == 'y':
                self.add_player(character.name)
        print(f"{len(self.players)} players joined the game.\n")
        # Game loop
        while True:
            current_player = self.players[self.current_player_index]
            print(f"It's {current_player.character.name}'s turn.")
            # Example turn progression (to be expanded)
            roll = self.roll_dice()
            print(f"You rolled a {roll}. You are currently at position {current_player.position}.")
            # TODO: ask player for movement input and process it
            # TODO: if player enters a room, handle suggestion
            # End of turn: move to next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            # Break condition for demonstration
            if input("Continue playing? (y/n): ").strip().lower() != 'y':
                break

if __name__ == '__main__':
    game = CluedoGame()
    game.run()
