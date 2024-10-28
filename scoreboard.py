from os import path
from tkinter import*

HEART_SYMBOL = "💛"
FONT = ("Helvetica", 22, "normal")
FONT_BTN = ("Helvetica", 18, "normal")
SCORE_FILE = "score.txt"


class Score:
    def __init__(self):
        self.lives = 5
        self.score = 0
        if path.exists(SCORE_FILE):
            with open(SCORE_FILE, mode='r') as score_file: 
                score_string = score_file.read()
                print(len(score_string))
                if len(score_string) > 0:
                    self.high_score = int(score_string)
                else:
                    self.high_score = 0
        else:
            open(file=SCORE_FILE, mode="x")
            self.high_score = 0

    def remaining_hearts(self):
        hearts = ""
        for _ in range(self.lives):
            hearts += HEART_SYMBOL
        return hearts
    
    def increase_score(self):
        self.score += 1
    
    def score_check(self):
        if self.score > self.high_score:
            with open(SCORE_FILE, mode='w') as score_file:
                score_file.write(f'{self.score}')

class Popup(Tk):
    def __init__(self, title, text):
        super().__init__()
        self.title(title)
        self.config(padx=10, pady=10)
        self.generate_text(text)
        self.generate_button()
        self.configure(background='LavenderBlush2')
        self.bind_all("<Any-KeyPress>", self.keypress_handler)
        self.protocol("WM_DELETE_WINDOW", self.exit_window)
        self.focus_force()
    
    def generate_button(self):
        self.button = Button(self, text="OK", font=FONT_BTN, command=self.exit_window)
        self.button.configure(width=10, borderwidth=1, background='LavenderBlush3', cursor='tcross')
        self.button.grid(column=1, row=1)
    
    def generate_text(self, text):
        self.max_width = 10
        self.label = Label(self, text=text, font=FONT, background='lavender blush', wraplength=500)
        self.label.grid(column=0, row=0)
        
    def keypress_handler(self, event):
        if event.keysym == "Return" or event.keysym == "Escape":
            self.exit_window()
    
    def exit_window(self):
        self.destroy()