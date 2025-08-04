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

#players can move from one room to another
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