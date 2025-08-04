from configurations import ROOMS, SECRET_PASSAGES 
from player import Player

def move_player(player, direction, steps):
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

def check_room_entry(pos): #check if a player entered the room, return the new location
    for room, tiles in ROOMS.items():
        if pos in tiles:
            return room
    return None

def will_move_off_board(position, direction, steps): #to check if a player is moving off the board, dont allow it
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
