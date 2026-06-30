
def load_highscore():
    try:
        with open("highscore.txt", "r") as high_file:
            stored_val = high_file.read().strip()
            return int(stored_val) if stored_val else 0
    except (FileNotFoundError, ValueError):
        return 0
    
def save_highscore(new_score):
    current_high = load_highscore()
    if new_score > current_high:
        try:
            with open("highscore.txt", "w") as high_file:
                high_file.write(str(new_score))
        except IOError:
            print("Error: Could not save the high score.")

    