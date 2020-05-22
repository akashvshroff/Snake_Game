import pygame
import time
from random import randint
from collections import namedtuple
from tkinter import *
from tkinter import ttk
import sqlite3
from math import floor


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
            'System', 18, 'bold'), fg='#f8f8ff', bg='#336699')
        self.title.place(relx=0.15, rely=0.05)
        self.rules = 'Eat as much of the pink food as you can to grow but beware, if you eat yourself, you will die. On easy mode, if you collide with the wall, then you will stop moving. On hard, if you try to leave the bounds, you will die. For both, there will also be poison that is deep black. DO NOT EAT IT. Move using the arrow keys, the larger you get, the faster you move. Enter your name below, choose your difficulty and get started.'
        self.rules_display = Message(self.tab1, text=self.rules, fg='#f8f8ff', bg='#336699', width=450,
                                     font=('System', 12), justify=LEFT)
        self.rules_display.place(relx=0, rely=0.15)
        self.login_text = StringVar()
        self.login_text.set("Enter username.")
        self.login_entry = Entry(self.tab1, textvariable=self.login_text, width=34,
                                 font=('System', 12, 'bold'), justify=LEFT, bg='#f8f8ff')
        self.login_entry.place(relx=0.02, rely=0.58)
        self.login_btn = Button(self.tab1, fg='#f8f8ff', width=10, bg='#336699',
                                font=('System', 12, 'bold'), text='SUBMIT', command=self.get_username)
        self.login_btn.place(relx=0.74, rely=0.57)

        self.easy_btn = Button(self.tab1, fg='#f8f8ff', width=20, bg='#336699',
                               font=('System', 12, 'bold'), text='EASY MODE', state=DISABLED, command=lambda: self.get_level(0))
        self.hard_btn = Button(self.tab1, fg='#f8f8ff', width=20, bg='#336699',
                               font=('System', 12, 'bold'), text='HARD MODE', state=DISABLED, command=lambda: self.get_level(1))
        self.easy_btn.place(relx=0.015, rely=0.68)
        self.hard_btn.place(relx=0.515, rely=0.68)

        self.start_playing_btn = Button(self.tab1, fg='#f8f8ff', width=20, bg='#336699', state=DISABLED,
                                        font=('System', 12, 'bold'), text='START GAME', command=self.play_game)
        self.leaderboard_btn = Button(self.tab1, fg='#f8f8ff', width=20, bg='#336699',
                                      font=('System', 12, 'bold'), state=DISABLED, text='LEADERBOARD', command=lambda: self.change_tab(1))
        self.quit_program_btn = Button(self.tab1, fg='#f8f8ff', width=42,
                                       bg='#336699', text='QUIT THE PROGRAM', font=('System', 12, 'bold'), command=self.quit_prg)
        self.start_playing_btn.place(relx=0.015, rely=0.78)
        self.leaderboard_btn.place(relx=0.515, rely=0.78)
        self.quit_program_btn.place(relx=0.017, rely=0.89)

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
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS Scores (username text, score int, diff_id int)')
        # 1 for easy, 2 for tough
        self.cur.execute('CREATE TABLE IF NOT EXISTS Diff (name text, id primary key)')
        self.cur.execute('INSERT OR IGNORE INTO Diff (name, id) VALUES (?,?)', ('easy', 1),)
        self.cur.execute('INSERT OR IGNORE INTO Diff (name, id) VALUES (?,?)', ('hard', 2),)

        # regular variables
        Colour = namedtuple("Colour", ["r", "g", "b"])
        self.bg_colour = Colour(r=51, g=102, b=153)
        self.snake_colour = Colour(r=51, g=204, b=51)
        self.food_colour = Colour(r=255, g=102, b=153)
        self.text_colour = Colour(r=255, g=255, b=255)
        self.border_colour = Colour(r=242, g=242, b=242)
        self.poison_colour = Colour(r=28, g=28, b=28)
        self.death_screen_colour = Colour(r=64, g=64, b=62)
        self.death_text_colour = Colour(r=236, g=33, b=33)

        # pygame stuff
        self.win_width = 400
        self.win_height = 400
        self.start_x, self.end_x = 40, 340
        self.start_y, self.end_y = 40, 340
        self.segment_size = 20

        self.key_map = {273: "Up",
                        274: "Down",
                        275: "Right",
                        276: "Left"}

        self.win_dimensions = self.win_height, self.win_width
        self.user_name = ''
        self.current_direction = None
        self.food_position = 0, 0
        self.poison_position = []
        self.eye_position_1 = (204, 188)
        self.eye_position_2 = (212, 188)
        self.delay = 0.2
        self.delay_reduction = 0
        self.score = 0
        self.easy_game = None
        self.diff = ''
        self.diff_id = 0

    def draw_grid(self):
        # draws the pygame grid
        for i in range(self.start_x, self.end_x+1, 20):
            for j in range(self.start_y, self.end_y+1, 20):
                pygame.draw.rect(self.screen, self.bg_colour, [
                                 i, j, self.segment_size, self.segment_size], 0)
                pygame.draw.rect(self.screen, self.border_colour, [
                                 i, j, self.segment_size, self.segment_size], 1)

    def set_eye_position(self):
        head_x, head_y = self.snake_positions[0]
        if self.current_direction == 'Right' or self.current_direction == 'Left':
            self.eye_position_1, self.eye_position_2 = (
                head_x + 8, head_y + 12), (head_x + 8, head_y + 4)
        elif self.current_direction == 'Up' or self.current_direction == 'Down':
            self.eye_position_1, self.eye_position_2 = (
                head_x + 4, head_y + 8), (head_x + 12, head_y + 8)

    def draw_obj(self):
        # draws the food and the snake
        self.set_eye_position()
        pygame.draw.rect(self.screen, self.food_colour, [
                         self.food_position, (self.segment_size, self.segment_size)])
        if self.poison_position:
            for x, y in self.poison_position:
                pygame.draw.rect(self.screen, self.poison_colour, [
                    x, y, self.segment_size, self.segment_size])
        for x, y in self.snake_positions:
            pygame.draw.rect(self.screen, self.snake_colour, [
                             x, y, self.segment_size, self.segment_size])
        pygame.draw.rect(self.screen, self.poison_colour, [self.eye_position_1, (4, 4)])
        pygame.draw.rect(self.screen, self.poison_colour, [self.eye_position_2, (4, 4)])

    def set_new_food_positions(self):
        # randomizes and checks the food position
        while True:
            x_position = randint(2, 17) * self.segment_size
            y_position = randint(2, 17) * self.segment_size
            food_position = (x_position, y_position)
            if food_position in self.snake_positions:
                continue
            else:
                self.food_position = food_position
                break

    def set_poison_position(self):
        # randomizes and checks the food position
        while True:
            x_position = randint(2, 17) * self.segment_size
            y_position = randint(2, 17) * self.segment_size
            poison_position = (x_position, y_position)
            if poison_position in self.snake_positions or poison_position == self.food_position:
                continue
            else:
                self.poison_position.append(poison_position)
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
        if self.easy_game:  # easy game
            tail_x, tail_y = snake_positions[-1]
            if head_x < self.start_x:
                self.snake_positions.pop(0)
                self.snake_positions.append((tail_x + 20, tail_y))
                self.current_direction = None
                return False
            elif head_x > self.end_x:
                self.snake_positions.pop(0)
                self.snake_positions.append((tail_x - 20, tail_y))
                self.current_direction = None
                return False
            elif head_y < self.start_y:
                self.snake_positions.pop(0)
                self.snake_positions.append((tail_x, tail_y + 20))
                self.current_direction = None
                return False
            elif head_y > self.end_y:
                self.snake_positions.pop(0)
                self.snake_positions.append((tail_x, tail_y - 20))
                self.current_direction = None
                return False
        else:
            if head_x < self.start_x or head_x > self.end_x or head_y < self.start_y or head_y > self.end_y:
                return True

        if (head_x, head_y) in snake_positions[1:]:
            return True
        if (head_x, head_y) == self.poison_position:
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

        self.snake_positions = [(200, 180)]
        self.set_new_food_positions()
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
            self.screen.blit(score_text, (300, 10))

            pygame.display.update()

            if self.current_direction:
                self.move_snake()

            if self.check_collisions(self.snake_positions):
                # print("snake: {}".format(self.snake_positions))
                pygame.quit()
                self.update_leaderboard()
                self.pop_up()

            if self.check_food_collision():
                self.set_new_food_positions()
                if not self.easy_game:  # for hard game there is a poison block that changes every time you eat.
                    if self.score > 5 and self.score % 6 == 0:
                        self.set_poison_position()
                else:
                    if self.score > 7 and self.score % 8 == 0:
                        self.set_poison_position()
                self.score += 1
                if self.delay > 0.01:
                    self.delay -= self.delay_reduction
                else:
                    self.delay = 0.01

            self.clock.tick(30)

    def pop_up(self):
        sc, self.score, self.delay = self.score, 0, 0.2
        self.snake_positions = [(200, 180)]
        self.poison_position = []
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
        self.easy_btn['state'] = NORMAL
        self.hard_btn['state'] = NORMAL
        self.login_text.set('All the best, {}. Choose a level.'.format(self.user_name))

    def get_level(self, n):
        if n == 0:
            self.easy_game = True
            self.diff = 'easy'
            self.delay_reduction = 0.006
            self.diff_id = 1
        else:
            self.easy_game = False
            self.diff = 'hard'
            self.delay_reduction = 0.003
            self.diff_id = 2
        self.login_text.set('All the best, {}. Level: {}.'.format(
            self.user_name, self.diff.upper()))
        self.start_playing_btn['state'] = NORMAL
        self.leaderboard_btn['state'] = NORMAL

    def update_leaderboard(self):
        # updates the leaderboard after every turn
        # re-initialises score
        'get the diff id and then do it'
        self.cur.execute('INSERT INTO Scores (username, score, diff_id) VALUES (?,?,?)',
                         (self.user_name, self.score, self.diff_id))
        self.conn.commit()

    def ordinal(self, n): return "%d%s" % (
        n, "tsnrhtdd"[(floor(n/10) % 10 != 1)*(n % 10 < 4)*n % 10::4])

    def show_leaderboard(self):
        # gets the data from the sql database and then shows it
        self.score_text.configure(state='normal')
        self.cur.execute(
            "SELECT username,score FROM Scores WHERE diff_id = ? ORDER BY score DESC", (self.diff_id,))
        score_data = self.cur.fetchall()
        score_info = ''
        score_info += 'MODE: {}\n\n'.format(self.diff.upper())
        if score_data:
            for i, (name, sc) in enumerate(score_data):
                if i >= 5:
                    break
                score_info += '{} PLACE. {} : {}\n'.format(self.ordinal(i+1), name, sc)
        else:
            score_info = 'There are no scores to display yet.'
        self.score_text.delete('1.0', END)
        self.score_text.insert(INSERT, score_info)
        self.score_text.configure(state='disabled')

    def quit_prg(self):
        # allows you to quit the program
        pygame.quit()
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
