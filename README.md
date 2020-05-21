# Outline:

- An emulation of the all the time classic snake game using PyGame, Tkinter and SQL. PyGame provided the operational basis for the game itself while Tkinter was used to create a GUI to interact with the game and finally SQL was used to house the scores in order to allow for a leaderboard. A detailed description lies below.

# Purpose:

- I had wanted to teach myself PyGame for quite some time but I couldn't find any project that was engaging and challenging at the same time until I finally realised, I could build the classic snake game I had spent most of my childhood whiling away time on. The build would help expose me to the broader more general features of PyGame like how to create a gameloop and PyGame's rect and text features while also allowing me to dig deeper while handling some more logical challenges of the game like detecting collisions, the idea of a growing snake and an increasingly difficult game as the snake grew. I could also brush up on my Tkinter, as I used it's simplicity in my program to add some usability via a leaderboard and start menu. Finally I used SQL to run the metaphorical 'back-end' of the project and used it to store user data and the leaderboard.

# Description:

- The program itself at its base is rather simple and cleanly written (or atleast that is what I attempted) bearing in mind OOP.
- The constructor of the class handles the set-up of the Tkinter window and tabs while the play_game function houses the PyGame initialisation and the game loop as shown below.

    ```python
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
                    if self.delay > 0.01:
                        self.delay -= 0.005
                    else:
                        self.delay = 0.01

                self.clock.tick(30)
    ```

- I chose to restrict all the pygame set up and loop to this sole function as it meant I could give the users to play again and that users would not be met with multiple windows on start up.
- Most of the other functions are descriptively named and are adorned with comments in order to aid readability.
- One interesting thing to note is the use of a namedTuple to initialise various rgb values used throughout the code and I have the Techlado blog to thank for that and a number of nuances in this build as I used their material for reference throughout my scripting.
