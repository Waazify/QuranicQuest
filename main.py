import tkinter as tk
from levels import level_packs  # Import level_packs from the levels module

root = tk.Tk()
root.title("Quranic Quest")
root.configure(bg="black")  # Set the background color to black

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to match the screen size
root.geometry(f"{screen_width}x{screen_height}")

welcome_label = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
story_text = tk.Label(root, text="Explore the wisdom of the Quran!", font=("Helvetica", 16), fg="white", bg="black")
score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14), fg="white", bg="black")

choice_buttons = []
current_level = None
current_level_pack = None
player_score = 0  # Initialize player score

# Menu to select level pack
menu = tk.Menu(root)
root.config(menu=menu)

level_packs_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Choose Level Pack", menu=level_packs_menu)

def update_story(new_text):
    story_text.config(text=new_text)
    # Hide choice buttons if the level pack is completed
    if current_level + 1 == len(current_level_pack):
        hide_choices()

def update_choices(choices):
    for button in choice_buttons:
        button.destroy()

    for i, choice_text in enumerate(choices, start=1):
        button = tk.Button(root, text=choice_text, command=lambda i=i: make_choice(i), font=("Helvetica", 14), fg="white", bg="black")
        choice_buttons.append(button)
        button.pack(pady=5)

def hide_choices():
    for button in choice_buttons:
        button.pack_forget()

def load_level_pack(pack_name):
    global current_level_pack
    if pack_name in level_packs:
        current_level_pack = level_packs[pack_name]
        load_level(0)  # Start with the first level in the pack
    else:
        print(f"Level pack '{pack_name}' not found.")

def load_level(level_index):
    global current_level_pack
    if 0 <= level_index < len(current_level_pack):
        global current_level
        current_level = level_index
        level_data = current_level_pack[level_index]
        update_story(level_data["story"])
        update_choices(level_data["choices"])
    else:
        print(f"Level index '{level_index}' out of range.")

def make_choice(choice_number):
    if current_level is not None:
        level_data = current_level_pack[current_level]
        user_answer = chr(ord('a') + choice_number - 1)

        correct_answer = level_data.get("correct_answer", None)

        if correct_answer is not None and user_answer.lower() == correct_answer:
            update_story(f"Correct! Well done. Your score: {update_score(1)}")
        elif correct_answer is None:
            update_story(f"Correct! Well done. Your score: {update_score(1)}")
        else:
            update_story(f"Wrong! The correct answer is: {correct_answer.upper()}. Your score: {update_score(0)}")

        # Move to the next level or show congratulations if all levels are completed
        if current_level + 1 < len(current_level_pack):
            load_level(current_level + 1)
        else:
            show_congratulations()

def update_score(increment):
    global player_score
    player_score += increment
    score_label.config(text=f"Score: {player_score}", fg="white", bg="black")  # Update score on the screen
    return player_score

def show_congratulations():
    update_story("Congratulations! You've completed the level pack!")
    # You can add more actions or go back to the level pack selection menu

def select_level_pack(pack_name):
    load_level_pack(pack_name)

# Add level packs to the menu dynamically
for pack_name in level_packs:
    level_packs_menu.add_command(label=pack_name, command=lambda pack_name=pack_name: select_level_pack(pack_name))

# Welcome message label
welcome_message = "Welcome to Quranic Quest!"
welcome_label.config(text=welcome_message)
welcome_label.pack(pady=10)

story_text.pack(pady=20)
score_label.pack()

root.mainloop()
