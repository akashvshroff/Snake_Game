import pygame
import time
from random import randint
from collections import namedtuple
from tkinter import *
from tkinter import ttk
import sqlite3
from math import floor

'''
tkinter = bg = '#336699'
tkinter = fg = '#f8f8ff'
tkinter entry fg = '#336699'
'''


class SnakePlayer:
    def __init__(self, master):
        # initialise the tkinter window, tabs and then start
        # set all the variables, name and score
        # sqlite connection
        # colours
        self.master = master
        self.master.geometry('450x450')
        self.tabs = ttk.Notebook(self.master)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text='START')
        self.tabs.add(self.tab2, text='LEADERBOARD')

        self.tabs.pack(expand=1, fill='both')

        # tab1
        self.start_frame = Frame(self.tab1, width=450, height=450, bg='#336699')
        self.start_frame.pack()
        self.title = Label(self.tab1, text='WELCOME TO SNAKE', font=(
            'System', 21, 'bold'), fg='#f8f8ff', bg='#336699')
        self.title.place(relx=0.15, rely=0.1)
        self.rules = 'Eat as many of the pink food as you can grow but beware, if you collide with the wall or yourself then you will die. Move using the arrow keys, the larger you get, the faster you move. Enter your name below and get started.'
        self.rules_display = Message(self.tab1, text=self.rules, fg='#f8f8ff', bg='#336699', width=450,
                                     font=('System', 14), justify=LEFT)
        self.rules_display.place(relx=0, rely=0.3)
        self.login_text = StringVar()
        self.login_text.set("Enter username.")
        self.login_entry = Entry(self.tab1, textvariable=self.login_text, width=34,
                                 font=('System', 12, 'bold'), justify=LEFT, bg='#f8f8ff')
        self.login_entry.place(relx=0.02, rely=0.62)
        self.login_btn = Button(self.tab1, fg='#f8f8ff', width=10, bg='#336699',
                                font=('System', 12, 'bold'), text='SUBMIT', command=self.get_username)
        self.login_btn.place(relx=0.74, rely=0.61)

        self.start_playing_btn = Button(self.tab1, fg='#f8f8ff', width=20, bg='#336699', state=DISABLED,
                                        font=('System', 12, 'bold'), text='START GAME', command=self.play_game)
        self.leaderboard_btn = Button(self.tab1, fg='#f8f8ff', width=20, bg='#336699',
                                      font=('System', 12, 'bold'), text='LEADERBOARD', command=lambda: self.change_tab(1))
        self.quit_program_btn = Button(self.tab1, fg='#f8f8ff', width=42,
                                       bg='#336699', text='QUIT PROGRAM', font=('System', 12, 'bold'), command=self.quit_prg)
        self.start_playing_btn.place(relx=0.015, rely=0.74)
        self.leaderboard_btn.place(relx=0.515, rely=0.74)
        self.quit_program_btn.place(relx=0.016, rely=0.86)

        # tab2
        self.leaderboard_frame = Frame(self.tab2, width=450, height=450, bg='#336699')
        self.leaderboard_frame.pack()

        self.score_label = Label(self.tab2, fg='#f8f8ff', text="SCORES",
                                 font=('System', 20, 'bold'), bg='#336699')
        self.score_label.place(relx=0.37, rely=0.03)

        self.score_text = Text(self.tab2, font=('System', 20, 'bold'),
                               height=8, width=25, bg='#f8f8ff', fg='#336699')  # change colour to lighter
        self.score_text.place(relx=0.055, rely=0.16)
        self.score_text.insert(INSERT, 'Click update scores.')
        self.score_text.configure(state='disabled')

        self.update_leaderboard_btn = Button(self.tab2, fg='#f8f8ff', width=19, height=1, font=(
            'System', 12, 'bold'), text=r'UPDATE SCORES', bg='#336699', command=self.show_leaderboard)
        self.play_more_btn = Button(self.tab2, fg='#f8f8ff', width=19, height=1, font=(
            'System', 12, 'bold'), text='PLAY AGAIN', bg='#336699', command=self.play_game)
        self.quit_prog_btn = Button(self.tab2, fg='#f8f8ff', width=39, height=1, font=(
            'System', 12, 'bold'), text='QUIT PROGRAM', bg='#336699', command=self.quit_prg)

        self.update_leaderboard_btn.place(relx=0.06, rely=0.79)
        self.play_more_btn.place(relx=0.51, rely=0.79)
        self.quit_prog_btn.place(relx=0.06, rely=0.89)

        # sql connections
        self.conn = sqlite3.connect(
            r'C:\Users\akush\Desktop\Programming\Projects\Snake\snake_scores.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Scores (username text, score int)')

        # regular variables
        Colour = namedtuple("Colour", ["r", "g", "b"])
        self.bg_colour = Colour(r=51, g=102, b=153)
        self.snake_colour = Colour(r=51, g=204, b=51)
        self.food_colour = Colour(r=255, g=102, b=153)
        self.text_colour = Colour(r=255, g=255, b=255)
        self.border_colour = Colour(r=242, g=242, b=242)
        self.death_screen_colour = Colour(r=64, g=64, b=62)
        self.death_text_colour = Colour(r=236, g=33, b=33)

        self.win_width = 600
        self.win_height = 600
        self.start_x, self.end_x = 40, 540
        self.start_y, self.end_y = 40, 540
        self.segment_size = 20

        self.key_map = {273: "Up",
                        274: "Down",
                        275: "Right",
                        276: "Left"}

        self.win_dimensions = self.win_height, self.win_width
        self.user_name = ''
        self.current_direction = None
        self.food_position = 0, 0
        self.delay = 0.1
        self.score = 0

        # pygame stuff

    def draw_grid(self):
        # draws the pygame grid
        for i in range(self.start_x, self.end_x+1, 20):
            for j in range(self.start_y, self.end_y+1, 20):
                pygame.draw.rect(self.screen, self.bg_colour, [
                                 i, j, self.segment_size, self.segment_size], 0)
                pygame.draw.rect(self.screen, self.border_colour, [
                                 i, j, self.segment_size, self.segment_size], 1)

    def draw_obj(self):
        # draws the food and the snake
        pygame.draw.rect(self.screen, self.food_colour, [
                         self.food_position, (self.segment_size, self.segment_size)])

        for x, y in self.snake_positions:
            pygame.draw.rect(self.screen, self.snake_colour, [
                             x, y, self.segment_size, self.segment_size])

    def set_new_food_positions(self, snake_positions):
        # randomizes and checks the food position
        while True:
            x_position = randint(2, 27) * self.segment_size
            y_position = randint(2, 27) * self.segment_size
            food_position = (x_position, y_position)
            if food_position in snake_positions:
                continue
            else:
                self.food_position = food_position
                break

    def move_snake(self):
        # moves the snake around and then deletes the last position
        time.sleep(self.delay)
        head_x, head_y = self.snake_positions[0]

        if self.current_direction == 'Left':
            new_head_pos = (head_x - self.segment_size, head_y)
        elif self.current_direction == 'Right':
            new_head_pos = (head_x + self.segment_size, head_y)
        elif self.current_direction == 'Down':
            new_head_pos = (head_x, head_y + self.segment_size)
        elif self.current_direction == 'Up':
            new_head_pos = (head_x, head_y - self.segment_size)
        self.snake_positions.insert(0, new_head_pos)
        del self.snake_positions[-1]

    def check_collisions(self, snake_positions):
        # checks the collisions with the wall and itself
        head_x, head_y = snake_positions[0]
        if head_x < self.start_x or head_x > self.end_x or head_y < self.start_y or head_y > self.end_y:
            return True
        if (head_x, head_y) in snake_positions[1:]:
            return True
        return False

    def check_food_collision(self):
        # checks if it collides with food of any sort
        if self.snake_positions[0] == self.food_position:
            self.snake_positions.append(self.snake_positions[-1])
            return True

    def on_key_press(self, event):
        # checks the current direction and the key press
        key = event.__dict__['key']
        new_direction = self.key_map.get(key)
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
        if new_direction in all_directions and {new_direction, self.current_direction} not in opposites:
            self.current_direction = new_direction

    def play_game(self):
        # initialises the pygame window and then sets up and then plays the game
        pygame.init()
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.win_dimensions)

        self.snake_positions = [(300, 280)]
        self.set_new_food_positions(self.snake_positions)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.on_key_press(event)
            self.screen.fill(self.bg_colour)
            self.draw_grid()
            self.draw_obj()
            font = pygame.font.Font(None, 26)
            score_text = font.render('SCORE: {:02}'.format(self.score), True, self.text_colour)
            user_text = font.render("NAME: {}".format(self.user_name), True, self.text_colour)
            self.screen.blit(user_text, (10, 10))
            self.screen.blit(score_text, (500, 10))

            pygame.display.update()

            if self.current_direction:
                self.move_snake()

            if self.check_collisions(self.snake_positions):
                # print("snake: {}".format(self.snake_positions))
                pygame.quit()
                self.update_leaderboard()
                self.pop_up()

            if self.check_food_collision():
                self.set_new_food_positions(self.snake_positions)
                self.score += 1
                if self.delay > 0:
                    self.delay -= 0.01
                else:
                    self.delay = 0

            self.clock.tick(30)

    def pop_up(self):
        sc, self.score = self.score, 0
        self.snake_positions = [(300, 280)]
        self.current_direction = None
        death_text = 'YOUR SCORE WAS {:02}.'.format(sc)
        self.death_win = Tk()
        self.death_win.geometry('450x400')
        death_frame = Frame(self.death_win, width=450, height=400, bg='#000000')
        death_frame.pack()
        death_label = Label(self.death_win, text='YOU DIED.', font=(
            'System', 35, 'bold'), bg='#000000', fg='#DC143C')
        death_label.place(relx=0.21, rely=0.25)
        death_info = Label(self.death_win, text=death_text, font=(
            'System', 25), bg='#000000', fg='#DC143C')
        death_info.place(relx=0.1, rely=0.52)
        ldbrd_btn = Button(self.death_win, text='LEADERBOARD', fg='#000000', bg='#DC143C',
                           width=20, font=('System', 12), command=self.quit_pop_up)
        replay_btn = Button(self.death_win, text='TRY AGAIN', fg='#000000', bg='#DC143C',
                            width=20, font=('System', 12), command=self.try_again)
        ldbrd_btn.place(relx=0.01, rely=0.8)
        replay_btn.place(relx=0.52, rely=0.8)
        self.death_win.mainloop()

    def try_again(self):
        self.death_win.destroy()
        try:
            self.play_game()
        except:
            pass

    def quit_pop_up(self):
        self.death_win.destroy()
        self.change_tab(1)

    def get_username(self):
        # gets the user_name
        self.user_name = self.login_text.get()
        self.start_playing_btn['state'] = NORMAL
        self.login_text.set('All the best, {}.'.format(self.user_name))

    def update_leaderboard(self):
        # updates the leaderboard after every turn
        # re-initialises score
        self.cur.execute('INSERT INTO Scores (username, score) VALUES (?,?)',
                         (self.user_name, self.score))
        self.conn.commit()

    def ordinal(self, n): return "%d%s" % (
        n, "tsnrhtdd"[(floor(n/10) % 10 != 1)*(n % 10 < 4)*n % 10::4])

    def show_leaderboard(self):
        # gets the data from the sql database and then shows it
        self.score_text.configure(state='normal')
        self.cur.execute("SELECT * FROM Scores ORDER BY score DESC")
        score_data = self.cur.fetchall()
        score_info = ''
        if score_data:
            for i, (name, sc) in enumerate(score_data):
                if i >= 5:
                    break
                score_info += '{}. {} : {}\n'.format(self.ordinal(i+1), name, sc)
        else:
            score_info = 'There are no scores to display yet.'
        self.score_text.delete('1.0', END)
        self.score_text.insert(INSERT, score_info)
        self.score_text.configure(state='disabled')

    def quit_prg(self):
        # allows you to quit the program
        sys.exit()

    def change_tab(self, n):
        # allows you to go the leaderboard and/or quit
        self.tabs.select(n)


def main():
    root = Tk()
    obj = SnakePlayer(root)
    root.mainloop()


if __name__ == '__main__':
    main()
