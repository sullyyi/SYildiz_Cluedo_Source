#tracker to assist human players
import os

def generate_tracker_log(player):
    lines = []
    lines.append("INFO TRACKER")
    lines.append("Your suggestion history:")
    for char, weap, room, refuter in player.suggestion_history:
        result = f"Refuted by {refuter}" if refuter else "No player refuted"
        lines.append(f"  • {char}, {weap}, {room} → {result}")
    
    not_solution = set()
    suspicious = []

    for char, weap, room, refuter in player.suggestion_history:
        if refuter:
            not_solution.update([char, weap, room])
        else:
            suspicious.append((char, weap, room))

    lines.append("\n Confirmed NOT in solution:")
    lines.append(f"  {', '.join(not_solution) if not_solution else 'None yet'}")

    lines.append("\n Suspicious (no player could refute):")
    for triplet in suspicious:
        lines.append(f"  • {triplet[0]}, {triplet[1]}, {triplet[2]}")

    return lines

def display_and_save_tracker(player):
    lines = generate_tracker_log(player)
    filename = "tracker_log.txt"
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"\n[TRACKER] Written to {filename}\n")

    # Auto-open the file
    os.system(f"open {filename}") 
