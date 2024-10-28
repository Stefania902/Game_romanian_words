from tkinter import *
import pandas
import random
from scoreboard import Score, Popup

scoreboard=Score()
popup=Popup

    ##Constants
FONT_TEXT = ("Helvetica", 16, "normal")
FONT_LABEL = ("Helvetica", 24, "bold")
FONT_HEARTS = ("Helvetica", 30, "bold")
SIZE = 36
BKGD_1 = 'LavenderBlush2'
BKGD_2 = 'LavenderBlush3'

    ##Initiate game with default database - usor.csv 
databases = ["usor.csv", "mediu.csv", "dificil.csv"]
radio_btn_value = 0
dict = pandas.read_csv(databases[radio_btn_value], encoding='cp1252')

    ##A random word and shuffle it
pick_random_word = random.choice(dict['word'])
shuffled_word = []
shuffled_word = list(pick_random_word)
random.shuffle(shuffled_word)

    ##New random and shuffled word when button is pressed
def other_word():
    global pick_random_word
    global shuffled_word
    pick_random_word = random.choice(dict['word'])
    shuffled_word = []
    shuffled_word = list(pick_random_word)
    random.shuffle(shuffled_word)
    shuffled_label.config(text=shuffled_word)    
    return shuffled_word

    ##Fetches the word definition from database when button is pressed
def fetch_definition(saved_word):
    #get index of saved_word
    index_word = dict[dict['word'] == saved_word].index.values
    print(index_word)
    #index = dict.set_index('word', inplace=True)
    popup('DEFINITIA DIN DEX', dict.loc[index_word, 'definition'].item())

    ##End the game when it runs out of lives
def end_game():
    popup('Pa Pa!', 'S-a incheiat jocul!')
    scoreboard.score_check()
    window.destroy()
    
    ##Player types the answer and presses 'Enter' function
def on_press(event):
    global user_input
    user_input=answer.get()
    check_answer()

    ##Player gives up and presses the 'Renunti?' button
def solution():
    #The solution is displayed
    solution_label.config(text=pick_random_word)
    #Save the word
    saved_word=pick_random_word
    #Another random word
    other_word()
    #Add a new button to fetch definition
    definition_btn = Button(text='Cauta in dex', background=BKGD_2, font=FONT_TEXT, width=15, borderwidth=1, cursor='tcross', command=lambda :fetch_definition(saved_word))
    definition_btn.place(x=450, y=425)
    #Heart counter reduces one life if you give up
    if scoreboard.lives > 1:
        scoreboard.lives -= 1
        hearts_label["text"] = scoreboard.remaining_hearts()
    #End the game if player gives up and has one life left
    elif scoreboard.lives == 1:
        end_game()

is_on = 0

def toggle_btn():
    global is_on
    
    if is_on == 0:
        first_btn.config(image=toggle_on)
        on_label = Label(window, text=pick_random_word[0], font=("Helvetica", 18, "bold"), background='light grey')
        on_label.place(x=720, y=308)
        is_on = 1
        on_label.after(1000, on_label.destroy)
    else:
        first_btn.config(image=toggle_off)
        on_label = Label(window, text=pick_random_word[0], font=("Helvetica", 18, "bold"), background='light grey')
        on_label.place(x=753, y=308)
        is_on = 0
        on_label.after(1000, on_label.destroy)

    ##Check the answer given by the player
def check_answer():
    if user_input == pick_random_word:
        print('Corect!')
        #Clear the player input from entry
        answer.delete(0, len(user_input))
        #New random and shuffled word
        other_word()
        if scoreboard.lives == 5:
            #Increase only the score and update label
            scoreboard.increase_score()
            score_label.configure(text = f"Score: {scoreboard.score}")
        elif scoreboard.lives > 0 and scoreboard.lives < 5:
            #Increase score and no. of lives
            scoreboard.increase_score()
            score_label.configure(text = f"Score: {scoreboard.score}")
            scoreboard.lives += 1
            hearts_label["text"] = scoreboard.remaining_hearts()
    elif user_input != pick_random_word:
        print('Gresit!')
        #Clear the player input from entry
        answer.delete(0, len(user_input))
        if scoreboard.lives > 0 and scoreboard.lives <= 5:
            popup('Uf', 'Mai incearca!')
            #Decrease no. of lives
            scoreboard.lives -= 1
            hearts_label["text"] = scoreboard.remaining_hearts()
        else:
            end_game()

    ## Creating the window
window = Tk()
window.title("CREZI CA STII?")
window.minsize(width=900, height=500)
image_bg = PhotoImage(file='Background.png')
background_label = Label(window, image=image_bg)
window.protocol("WM_DELETE_WINDOW", end_game)

    ##Create radius buttons for level choose: incepator, mediu and dificil
def radio_used():
    global radio_btn_value, dict
    radio_btn_value = radio_state.get()
    print(radio_btn_value)
    dict = pandas.read_csv(databases[radio_btn_value])
    other_word()
radio_state = IntVar()
radiobutton1 = Radiobutton(text="Usor", value=0, variable=radio_state, command=radio_used)
radiobutton2 = Radiobutton(text="Mediu", value=1, variable=radio_state, command=radio_used)
radiobutton3 = Radiobutton(text="Dificil", value=2, variable=radio_state, command=radio_used)
radiobutton1.place(x=30, y=40)
radiobutton2.place(x=100, y=40)
radiobutton3.place(x=180, y=40)

    ##Creating window controls
#Shuffles area: description, label and button
shuffled_description = Label(text='Ghiceste cuvantul din chenarul de mai jos:', background=BKGD_1, font=FONT_TEXT)
shuffled_label = Label(text=shuffled_word, font=FONT_LABEL, width=20)
other_word_btn = Button(text='Cuvant nou', background=BKGD_2, font=FONT_TEXT, width=10, borderwidth=1, cursor='tcross', command=other_word)

#Typing the word area: description and entry tab
answer_description = Label(text="Sti deja? Tasteaza-l si apasa 'Enter'", background=BKGD_1, font=FONT_TEXT)
answer = Entry(width=20, font='Calibri 20 normal')
answer.focus()
#User types the answer and presses 'Enter'
answer.bind('<Return>', on_press)

#Hint and correct word area: label and button
first_letter = Label(text='Prima litera ca indiciu ---->', font=FONT_TEXT)
toggle_on=PhotoImage(file='on.png')
toggle_off=PhotoImage(file='off.png')
first_btn = Button (window, image=toggle_off, cursor='tcross', command=toggle_btn)
solution_label = Label(text='Cuvantul cautat', font=FONT_LABEL, height=1, width = 15)
solution_btn = Button(text='Renunti?', background=BKGD_2, font=FONT_TEXT, width=10, borderwidth=1, cursor='tcross', command=solution)

#Hearts and scores: description and label
hearts_description = Label(text='Numarul de incercari 💛', background=BKGD_1, font=FONT_TEXT)
hearts_label = Label(text=scoreboard.remaining_hearts(), font=FONT_HEARTS, background=BKGD_1)
score_label = Label(text=f"Scor: {scoreboard.score}", background=BKGD_1, font=FONT_TEXT)
high_score_label = Label(text=f"Scor maxim: {scoreboard.high_score}", background=BKGD_1, font=FONT_TEXT)

##Place the elements
background_label.place(x=0, y=0)

#Hearts and scores
hearts_description.place(x=30, y=82)
hearts_label.place(x=30, y=107)
score_label.place(x=30, y=180)
high_score_label.place(x=30, y=220)

##Shuffle area
shuffled_description.place(x=300, y=48)
shuffled_label.place(x=302, y=78)
other_word_btn.place(x=700, y=77)

##Answer area
answer_description.place(x=302, y=143)
answer.place(x=302, y=173)

##Solution area
first_letter.place(x=420, y=310)
first_btn.place(x=700, y=300)
solution_label.place(x=398, y=366)
solution_btn.place(x=700, y=365)

window.mainloop()