from tkinter import Tk, Button, Label, messagebox
from PIL import Image, ImageTk, ImageSequence
import os
import random
from itertools import cycle

class GameClass(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("850x600")
        self.config(bg="grey")
        self.title("Memory Game")
        self.number = 0
        self.number_list = []
        self.bottom_image_label = None
        self.bottom_image_path = None  # Initialize bottom image path
        self.rounds = 5  # Total number of rounds
        self.current_round = 1  # Initialize current round
        self.correct_choices = 0
        self.total_attempts = 0
        self.game_started = False  # Flag to track if game has started

        self.scoreboard_label = Label(self, text="Scoreboard", font=("Arial", 16), bg="grey", fg="white")
        self.scoreboard_label.place(x=800, y=20)
        self.score_label = Label(self, text=f"Correct Choices: {self.correct_choices}/{self.rounds}", font=("Arial", 12), bg="grey", fg="white")
        self.score_label.place(x=800, y=50)

        self.correct_gif_frames = self.load_gif_frames("C:\\Users\\monik\\Downloads\\hurrah.gif")
        self.wrong_gif_frames = self.load_gif_frames("C:\\Users\\monik\\Downloads\\oops.gif")

        self.start_button = Button(self, text="Start Game", command=self.start_game, borderwidth=2, bg="white", fg="black", font=("Arial", 16))
        self.start_button.place(x=350, y=250)

    def start_game(self):
        self.game_started = True
        self.start_button.destroy()  # Remove the start button once game has started
        self.label()  # Create game labels and buttons
        self.start_show()  # Start showing images

    def load_gif_frames(self, gif_path):
        gif_image = Image.open(gif_path)
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]
        return cycle(gif_frames)

    def label(self):
        if self.game_started:  # Only show scoreboard during the game
            self.scoreboard_label = Label(self, text="Scoreboard", font=("Arial", 16), bg="grey", fg="white")
            self.scoreboard_label.place(x=800, y=20)
            self.score_label = Label(self, text=f"Correct Choices: {self.correct_choices}/{self.rounds}", font=("Arial", 12), bg="grey", fg="white")
            self.score_label.place(x=800, y=50)

            self.position_labels = []
            positions = [(280, 20), (450, 20), (630, 20), (280, 150), (450, 150), (630, 150), (280, 280), (450, 280), (630, 280)]
            for i in range(9):
                position_label = Label(self, text=str(i+1), font=("Arial", 12), fg="black")
                position_label.place(x=positions[i][0]-20, y=positions[i][1]+50)
                self.position_labels.append(position_label)

        self.show_button = Button(self, text="Show", command=self.start_show, borderwidth=2, bg="white", fg="black", font=("Arial", 16), height=5, width=17)
        self.show_button.place(x=40, y=150)

        self.buttons = []
        positions = [(280, 20), (450, 20), (630, 20), (280, 150), (450, 150), (630, 150), (280, 280), (450, 280), (630, 280)]
        for i in range(9):
            button = Button(self, image="", command=lambda btn=i+1: self.check(btn), borderwidth=2, bg="sky blue",height=125, width=125)
            button.place(x=positions[i][0], y=positions[i][1])
            self.buttons.append(button)

    def start_show(self):
        if not self.game_started:
            messagebox.showinfo("Start Game", "Please start the game first!")
            return
        
        if self.current_round > self.rounds or self.total_attempts >= 5:  # Check if all rounds are completed or max attempts reached
            messagebox.showinfo("Game Over", "All rounds completed or maximum attempts reached. Game Over!")
            self.reset_game()  # Reset the game
            return
        
        if self.number % 2 == 0:  # Show mode
            self.number_list = os.listdir('C:\\Users\\monik\\Downloads\\Images')
            self.photo_images = []
            for i, image_path in enumerate(self.number_list[:9]):
                image = Image.open(os.path.join('C:\\Users\\monik\\Downloads\\Images', image_path))
                image = image.resize((125, 125), Image.ANTIALIAS)
                photo_image = ImageTk.PhotoImage(image)
                self.photo_images.append(photo_image)
                self.buttons[i].config(image=photo_image)
            self.show_button.config(text="Hide", bg="white", fg="black", font=("Arial", 16))
        
        else:  # Hide mode
            self.display_blank_blocks()
            self.show_button.config(text="Show", bg="white", fg="black", font=("Arial", 16))
            self.display_bottom_image()
        self.number += 1

    def on_button_click(self,event):
        button=event.widget
        index=self.buttons.index(button)+1
        self.check(index)

    def display_bottom_image(self):
        random_image_path = random.choice(self.number_list)
        self.bottom_image_path = random_image_path  # Set the bottom image path
        image = Image.open(os.path.join('C:\\Users\\monik\\Downloads\\Images', random_image_path))
        image = image.resize((125, 125), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)
        if self.bottom_image_label:
            self.bottom_image_label.destroy()
        self.bottom_image_label = Label(self, image=photo_image, bg="white")  # Set bottom image block color to white
        self.bottom_image_label.image = photo_image  # Keep reference to avoid garbage collection
        self.bottom_image_label.place(x=280, y=450)

    def display_blank_blocks(self):
        blank_image = Image.new("RGBA", (125, 125), (135, 206, 250))  # Create a blank image with sky blue color
        blank_photo = ImageTk.PhotoImage(blank_image)
        for button in self.buttons:
            button.config(image=blank_photo, text="")
            button.bind("<Button-1>",self.on_button_click) # Display blank blocks with sky blue color

    def check(self, btn_number):
        image_path = self.number_list[btn_number - 1]  # Get the path of the clicked image
        
        if self.number % 2 == 0:  # Hide mode
            if image_path == self.bottom_image_path:  # Check if clicked image matches the bottom image
                messagebox.showinfo("Correct Choice", "You've made the correct choice!")
                self.show_animation(self.correct_gif_frames)
                self.correct_choices += 1  # Increment correct choice count
                self.update_scoreboard()  # Update scoreboard after correct choice
                self.next_round()  # Move to the next round
            else:
                messagebox.showinfo("Wrong Choice", "Wrong Choice!")
                self.show_animation(self.wrong_gif_frames)

        self.after(500, self.start_show)  # Automatically switch to show mode after 2 seconds
        self.total_attempts += 1  # Increment total attempts after each round

    def show_animation(self, gif_frames):
        gif_frame = next(gif_frames)  # Get the next frame from the GIF cycle
        animation_label = Label(self, image=gif_frame, bg="white")
        animation_label.image = gif_frame  # Keep reference to avoid garbage collection
        animation_label.place(x=800, y=80)  # Adjust the position below the scoreboard
        self.after(600, animation_label.destroy)  # Remove the animation after 0.6 seconds

    def update_scoreboard(self):
        if self.game_started:  # Check if the game has started to update the scoreboard
            self.score_label.config(text=f"Correct Choices: {self.correct_choices}/{self.rounds}")  # Update scoreboard

    def next_round(self):
        self.current_round += 1
        self.update_scoreboard()


    def reset_game(self):
        self.number = 0
        self.current_round = 1
        self.correct_choices = 0
        self.total_attempts = 0
        self.game_started = False  # Reset game started flag
        self.score_label.config(text="")  # Clear scoreboard
        self.remove_game_elements()  # Remove game elements
        self.remove_position_numbers() 
        self.remove_scoreboard()
        self.start_button = Button(self, text="Start Game", command=self.start_game, borderwidth=2, bg="white", fg="black", font=("Arial", 16))
        self.start_button.place(x=350, y=250)  # Display start button again

    def remove_position_numbers(self):
        for label in self.position_labels:
          if label.winfo_exists():  
           label.place_forget()

    def remove_scoreboard(self):
     if hasattr(self, 'scoreboard_label'):
        self.scoreboard_label.destroy()
     if hasattr(self, 'score_label'):
        self.score_label.destroy()

    def remove_game_elements(self):
        if hasattr(self, 'show_button'):
            self.show_button.destroy()
        if hasattr(self, 'bottom_image_label'):
            self.bottom_image_label.destroy()
        for button in self.buttons:
            button.destroy()


if __name__ == "__main__":
    game = GameClass()
    game.mainloop()
 
