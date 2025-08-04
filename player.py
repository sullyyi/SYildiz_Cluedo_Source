from configurations import CHARACTERS, WEAPONS, ROOM_NAMES

class Player:
    # Represents a player in the Cluedo game. A player has a name, current position on the board, and a hand of cards.
    # The `is_ai` flag indicates whether this player is controlled by the computer.
    # Each player also maintains a knowledge base for deduction purposes when controlled by the AI.

    def __init__(self, name, position, is_ai: bool = False):
        # Initialize a new player.
        self.name = name
        self.position = position
        self.cards: list[str] = []
        self.eliminated: bool = False
        self.is_ai: bool = is_ai

        # AI deduction state
        # Maps other player names to the set of cards known to be held by them
        self.known_cards: dict[str, set[str]] = {}
        # Maps other player names to the set of cards known to NOT be held by them
        self.not_have: dict[str, set[str]] = {}
        # Possible solution sets for character, weapon, and room; narrowed as the game progresses
        self.possible_solution = {
            "character": set(CHARACTERS),
            "weapon": set(WEAPONS),
            "room": set(ROOM_NAMES),
        }
        # Suggestion history for potential future logic or replay/debugging
        self.suggestion_history: list[tuple[str, str, str, str | None]] = []

    def receive_card(self, card: str):
        """Assign a card to this player and update AI deduction if applicable."""
        self.cards.append(card)
        if self.is_ai:
            # Eliminate owned cards from the possible solution
            for category in self.possible_solution:
                self.possible_solution[category].discard(card)

    def observe_suggestion(self, character: str, weapon: str, room: str, refuter_name: str | None, players_in_game: list[str]):
        """Update AI deduction based on suggestion outcome."""
        if not self.is_ai:
            return

        suggestion = (character, weapon, room)
        self.suggestion_history.append((*suggestion, refuter_name))

        if refuter_name is None:
            print(f"[AI LOGIC] No one refuted suggestion: {suggestion}")
            # Eliminate all 3 from all other players; include them in possible solution
            for category, card in zip(["character", "weapon", "room"], suggestion):
                self.possible_solution[category].intersection_update({card})
                for player in players_in_game:
                    if player != self.name:
                        self.not_have.setdefault(player, set()).add(card)
        else:
            print(f"[AI LOGIC] {refuter_name} refuted suggestion: {suggestion}")
            # Mark that everyone else doesn't have any of the three
            for player in players_in_game:
                if player != self.name and player != refuter_name:
                    self.not_have.setdefault(player, set()).update(suggestion)

    def update_knowledge_from_refutation(self, suggester: str, suggestion: tuple[str, str, str], refuter: str, card_shown: str | None):
        """Refinement from private card shown to AI."""
        if not self.is_ai or not card_shown:
            return

        self.known_cards.setdefault(refuter, set()).add(card_shown)
        print(f"[AI LOGIC] {refuter} must have '{card_shown}'")
        # Remove shown card from the possible solution
        for category in self.possible_solution:
            self.possible_solution[category].discard(card_shown)

    def should_accuse(self) -> bool:
        """Check if AI has narrowed down the solution and should accuse."""
        if not self.is_ai:
            return False
        return all(len(self.possible_solution[cat]) == 1 for cat in self.possible_solution)

    def make_accusation(self) -> tuple[str, str, str] | None:
        """Return the AI's accusation if it's sure, else None."""
        if self.should_accuse():
            char = next(iter(self.possible_solution["character"]))
            weap = next(iter(self.possible_solution["weapon"]))
            room = next(iter(self.possible_solution["room"]))
            print(f"[AI DECISION] Making accusation: {char}, {weap}, {room}")
            return (char, weap, room)
        return None

    def choose_suggestion(self) -> tuple[str, str, str] | None:
        """AI chooses a suggestion based on narrowed possibilities."""
        if not self.is_ai:
            return None

        char = next(iter(self.possible_solution["character"]))
        weap = next(iter(self.possible_solution["weapon"]))
        room = next(iter(self.possible_solution["room"]))

        print(f"[AI DECISION] Suggesting: {char}, {weap}, {room}")
        return (char, weap, room)
