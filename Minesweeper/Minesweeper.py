# Model View Controller pattern of A3 GUI Pokemon Game

import tkinter as tk
import random
import math
import os

from time import time
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog

# CONSTANTS
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
EXPOSED = "0"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
REVEALED = "0123456789"
TASK_ONE = 1
TASK_TWO = 2

class BoardModel(object):
    """
    Represents board game involved in game
    """
    def __init__(self, grid_size, num_pokemon):
        """
        It stores and manages internal game state. It is a model class

        Parameters:
            grid_size (int): the size of the grid used
            num_pokemon (int): number of hidden pokemon involved
        """
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._game = UNEXPOSED * grid_size*grid_size
        self._pokemon_locations = self.generate_pokemons(grid_size, num_pokemon)
        
    def get_pokemon_locations(self):
        """
        (list<int>) Returns indices of pokemon locations in game string
        """
        return self._pokemon_locations

    def get_num_attempted_catches(self):
        """
        (int) Returns number of pokeballs currently placed on board
        """
        pokeballs_num = 0
        for element in self.get_game():
            if element == FLAG:
                pokeballs_num+=1
        return pokeballs_num

    def get_num_pokemon(self):
        """
        (int) Returns number of pokemons hidden in game
        """
        return self._num_pokemon

    def get_game(self):
        """
        (str) Returns the status of game string that represents each tile on game
        board
        """
        return self._game

    def check_loss(self):
        """
        (bool) Returns True if and only if game is lost, else will be False
        """
        pokemon_hidden_loc = self.get_pokemon_locations()
        pokemon_pos = []
        
        for pokemon_index in pokemon_hidden_loc:
            pokemon_pos.append(self.index_to_position(pokemon_index))

        for index, element in enumerate(self._game):
            pos = self.index_to_position(index)

            if pos in pokemon_pos and element in REVEALED:
                return True
        return False

    def check_win(self):
        """
        (bool) Checks if player has won game by looking into all cell status of game string

        """
        non_pokemon_cell = len(self._game) - len(self._pokemon_locations)
        cond1 = 0
        cond2 = 0
        for cell in self._game:
            if cell.isdigit():
                cond1 += 1
        for pokemon in self._pokemon_locations:
            if self._game[pokemon] == FLAG:
                cond2 += 1
        if cond1 == non_pokemon_cell and cond2 == len(self._pokemon_locations):
            return True
        else:
            return False
        
    def index_to_position(self, index):
        """
        (tuple<int, int>) Returns (row, col) coordinate corresponding to supplied index

        Paramters:
            index (int): index corresponding to game string
        """
        row = index // self._grid_size
        col = index % self._grid_size
        coordinate = (row, col)
        return coordinate

    def position_to_index(self, position):
        """
        (int) Returns index corresponding to coordinate inputted

        Paramters:
            positio (tuple): tuple corresponding to position of tile on game board
        """
        index = position[1] + position[0]*self._grid_size
        return index

    def replace_character_at_index(self, index, character):
        """
        Replaces game string with specified character placed at the specified index
        anad returns it

        Parameters:
            game (str): A string of all relevant game character 
            index (int): The index position in game string that will be updated
            character (str): The character that will be used to update a specific game string
        """
        game = list(self._game)
        game[index] = character
        self._game = "".join(game)

    def flag_cell(self, index):
        """
        Toggles the flag at the specified index in game string and updates it

        Parameters:
            game (string): A string of all relevant game character 
            index (int): The index position in game string that will be updated 
        """
        game = list(self._game)
        if game[index] == UNEXPOSED:
            game[index] = FLAG
        elif game[index] == FLAG:
            game[index] = UNEXPOSED
        self._game = "".join(game) 

    def generate_pokemons(self, grid_size, number_of_pokemons):
        """
        (tuple<int>) Pokemons will be generated and given a random index within the
        game. 

        Parameters:
            grid_size (int): The grid size of the game.
            number_of_pokemons (int): The number of pokemons that the game will
            have.
        """
        cell_count = grid_size ** 2
        pokemon_locations = ()

        for _ in range(number_of_pokemons):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count-1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count-1)

            pokemon_locations += (index,)
        return pokemon_locations
            
    def index_in_direction(self, index, grid_size, direction):
        """
        (int) Takes index to a cell in the game string and returns a new index
        corresponding to an adjacent cell in the specified direction and will
        return None if it goes out of game board boundaries

        Parameters:
            index (int): The index position in game string that is relevant for specified direction
            grid_size (int): Grid size of the game
            direction (str): Direction of intended movement
        """
        directions_dict = {
        UP : -1,
        DOWN: 1,
        LEFT: -1,
        RIGHT: 1,
        UP+'-'+LEFT: [-1,-1],
        UP+'-'+RIGHT: [1,-1],
        DOWN+'-'+LEFT: [-1,1],
        DOWN+'-'+RIGHT: [1,1]
        }

        topL_corner = 0
        topR_corner = grid_size-1
        botL_corner = grid_size*(grid_size-1)
        botR_corner = grid_size*grid_size
        
        top_boundary = [i for i in range(topL_corner ,topR_corner+1)]
        bot_boundary = [i for i in range(botL_corner , botR_corner+1)]
        left_boundary = [i for i in range(topL_corner, botL_corner+1, grid_size)]
        right_boundary = [i for i in range(topR_corner, botR_corner, grid_size)]

        # Code at the bottom ensures indexes on the edges of the grid would not be updated when it is directed towards the boundaries of the grid
        # and will return None instead. All indexes on the edges of grid are covered in the code below
        if direction in [RIGHT, LEFT]:
            if (index in left_boundary and direction == LEFT) or (index in right_boundary and direction == RIGHT):
                return None
            index = index + directions_dict[direction]
            
        elif direction in [UP, DOWN]:
            if (index in top_boundary and direction == UP) or (index in bot_boundary and direction == DOWN):
                return None
            index = index + grid_size*directions_dict[direction]
            
        elif direction in directions_dict:
            if direction in [UP+'-'+LEFT, DOWN+'-'+LEFT]:
                if (index in (top_boundary + left_boundary) and direction == UP+'-'+LEFT) or (index in (left_boundary + bot_boundary) and direction == DOWN+'-'+LEFT):
                    return None
                
            elif direction in [UP+'-'+RIGHT, DOWN+'-'+RIGHT]:
                if (index in (top_boundary + right_boundary) and direction == UP+'-'+RIGHT) or (index in (right_boundary + bot_boundary) and direction == DOWN+'-'+RIGHT):
                    return None
            index = index + directions_dict[direction][0] + grid_size*directions_dict[direction][1]
            
        else:
            return None
        return index

    def neighbour_directions(self, index, grid_size):
        """
        (list<int>) Returns a list of indexes that have a neighbouring cell
        (excluding the boundaries).

        Parameters:
            index (int): The index position in game string 
            grid_size (int): Grid size of the game
        """
        neighbour_indexes = []
        for direct in DIRECTIONS:
            if self.index_in_direction(index, grid_size, direct) != None:
                neighbour_indexes.append(self.index_in_direction(index, grid_size, direct))
        return neighbour_indexes

    def number_at_cell(self, game, pokemon_locations, grid_size, index):
        """
        (int) Would check the number of pokemon in neighbouring cells and output an
        integer of that particular cell

        Parameters:
            game (str): Used to check if there are already any exposed cell in game string
            grid_size (int): Grid size of the game
            index (int): This would be the relevant cell that will be checked to see number of pokemon around it
            pokemon_locations (tuple <int,...>): Random pokemon locations which is given as index number corresponding to position in game string
        """
        pokemon_num = 0
        revealed = "012345678"
        revealed_cell = []
        neighbours = self.neighbour_directions(index, grid_size)

        # bottom code appends revealed cell (cells that are not "~") to an empty list
        for cell in neighbours:
            if game[cell] in revealed:
                revealed_cell.append(cell)

        # since neighbour_directions would include a revealed cell as a "neighbour",
        # it is unnecessary and since there will be 10x10 cells, this removal of
        # cells that are not relevant would speed code up
        for cell in revealed_cell:
            if cell in neighbours:
                neighbours.remove(cell)

        for cell in neighbours:
            if cell in pokemon_locations:
                pokemon_num+=1   
        return pokemon_num

    def big_fun_search(self, game , grid_size, pokemon_locations, index):
        """
        (list<int>) Searching adjacent cells to see if there are any Pokemon"s
        present. Find all cells which should be revealed when a cell is selected.
        For cells which have a zero value (i.e. no neighbouring pokemons) all the
        cell"s neighbours are revealed. If one of the neighbouring cells is also
        zero then all of that cell"s neighbours are also revealed. This repeats
        until no zero value neighbours exist.
        For cells which have a non-zero value (i.e. cells with neightbour pokemons)
        , only the cell itself is revealed.

        Parameters:
            game (str): Game string.
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell
        """
        queue = [index]
        discovered = [index]
        visible = []

        if game[index] == FLAG:
                return queue

        number = self.number_at_cell(game, pokemon_locations, grid_size, index)
        if number != 0:
                return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, grid_size):
                if neighbour in discovered or neighbour is None:
                    continue

                discovered.append(neighbour)
                if game[neighbour] != FLAG:
                    number = self.number_at_cell(game, pokemon_locations, grid_size, neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def restart_game_string(self):
        """
        (int) This will restart all elements in game string but maintain hidden
        pokemon locations
        """
        self._game = UNEXPOSED * self._grid_size*self._grid_size

    def get_num_pokeball_left(self):
        """
        Acquires the number of pokeballs left for players
        """
        pokeballs_num = self.get_num_pokemon()
        for element in self.get_game():
            if element == FLAG:
                pokeballs_num-=1
        return pokeballs_num

    def set_game_settings_open(self, pokemon_num, pokemon_loc, game_string, grid_size):
        """
        This will ensure the following settings would follow settings of file loaded:
        number of pokemons in game, pokemon location and game string

        Parameters:
            pokemon_num (int): Previous game data's of number of pokemons
            pokemon_loc (tuple): Previous game data's of location of pokemons
            game_string (str): Previous game data's of game string
        """
        self._game = game_string
        self._num_pokemon = pokemon_num
        self._pokemon_locations = pokemon_loc
        self._grid_size = grid_size

class StatusBar(tk.Frame):
    """
    Represents status of game currently played
    """
    def __init__(self, master, NewGame, RestartGame):
        """
        Represents the current status of game and provides menu for user to click
        new game and restart game

        Parameters:
            master (object): tkinter.Tk class used to represent 'master' window
            NewGame (class method): This will cause game to be renewed with pokemon
            locations changing
            RestartGame (class method): This will restart game with pokemon
            locations not changing
        """
        super().__init__(master)
        # id cycle is used to keep track of the after cycle when timer is run
        self._id_cycle = None

        # the following ensures timer will turn off and tracks it 
        self._timer_off = False
        self._prev_elapsed_time = 0
        self._start_time = None
        self._elapsed_time = None
        self._master = master
        self._attempted_catches = 0
        self._pokeball_left = 0
        self.configure(height="100", bg="white")
        self.pack(fill='x', side=tk.BOTTOM, expand=True)

        load = Image.open("images/full_pokeball.gif")
        render = ImageTk.PhotoImage(load)
        self._frame1 = tk.Frame(self)
        self._frame1.configure(bg="white")
        self._frame1.pack(side=tk.LEFT, expand=True)
        self._pokeball = tk.Label(self._frame1, image=render, bg='white')
        self._pokeball.image = render
        self._pokeball.pack(pady=10, side=tk.LEFT)

        self._frame2 = tk.Frame(self)
        self._frame2.configure(bg="white")
        self._frame2.pack(side=tk.LEFT, expand=True)
    
        self._attempted_catches_text = tk.Label(self._frame2, text= str(self._attempted_catches)+" attempted catches")
        self._attempted_catches_text.configure(bg="white", anchor='w')
        self._attempted_catches_text.pack(pady=2, side=tk.TOP, fill=tk.BOTH)

        self._pokeball_left = tk.Label(self._frame2, text= str(self._pokeball_left)+" pokeballs left")
        self._pokeball_left.configure(bg="white", anchor='w')
        self._pokeball_left.pack(pady=2, side=tk.TOP, fill=tk.BOTH)

        load = Image.open("images/clock.gif")
        render = ImageTk.PhotoImage(load)
        self._frame3 = tk.Frame(self)
        self._frame3.configure(bg="white")
        self._frame3.pack(side=tk.LEFT, expand=True)
        self.time_img = tk.Label(self._frame3, image=render, bg='white')
        self.time_img.image = render
        self.time_img.pack(pady=10, side=tk.LEFT)

        self._frame4 = tk.Frame(self)
        self._frame4.configure(bg="white")
        self._frame4.pack(side=tk.LEFT, expand=True)
        self._time_text_title = tk.Label(self._frame4, text="Time elapsed")
        self._time_text_title.configure(bg="white")
        self._time_text_title.pack(pady=2, side=tk.TOP)
        self._timer_text = tk.Label(self._frame4, text="00:00")
        self._timer_text.configure(bg="white")
        self._timer_text.pack(pady=2, side=tk.TOP)

        self._button_frame = tk.Frame(self)
        self._button_frame.configure(bg="white")
        new_game_button = tk.Button(self._button_frame,
                                    text="New Game", command=NewGame)
        new_game_button.pack(side=tk.TOP)
        new_game_button.configure(bg="white")
        
        restart_button = tk.Button(self._button_frame,
                                   text="Restart Game", command=RestartGame)
        restart_button.pack(side=tk.TOP)
        restart_button.configure(bg="white")
        self._button_frame.pack(side=tk.LEFT, expand=True)
        
    def update_pokeball_stats(self, attempt, pokeball_left):
        """
        Represents pokeballs used by users to catch pokemon during game and will
        be visually shown in status bar

        Parameters:
            attempt (int): number of attempted pokeball thrown to catch pokemon
            pokeball_left (int): number of pokeball left (equivalent to number
            of pokemon in game that are hidden)
        """
        self._attempted_catches_text.configure(text=str(attempt)+" attempted catches")
        self._pokeball_left.configure(text=str(pokeball_left)+" pokeballs left")

    def update_clock(self):
        """
        This counts time diff when game starts and updadtes by cailling itself
        """
        # this line only gets rid of previous after id that was created
        # when code is first run - id_cycle does not exist yet
        if self._id_cycle:
            self.after_cancel(self._id_cycle)
            
        later_time = time()
        self._elapsed_time = later_time - self._start_time + self._prev_elapsed_time
        minutes, seconds = divmod(self._elapsed_time, 60)
        
        timeformat = "{:02d}m {:02d}s".format(int(minutes), int(seconds))
        self._timer_text.configure(bg="white", text=timeformat)
        self._id_cycle = self.after(1000, self.update_clock)

        if self._timer_off:
            self._timer_off = False
            self.after_cancel(self._id_cycle)

    def off_timer(self):
        """
        Turns off timer so no remaining data
        """
        self._timer_off = True
        
    def update_start_time(self):
        """
        When game is restarted, start time need to be updated to current time
        """
        self._start_time = time()

    def get_elapsed_time(self):
        """
        (float) When saving, elapsed time is required for record
        """
        return self._elapsed_time

    def set_elapsed_time(self,new_elapsed_time):
        """
        When loading, previous game's elapsed time needs to be taken into account
        """
        self._prev_elapsed_time = new_elapsed_time
        
class PokemonGame(object):
    """
    Represents the entire game process
    """
    def __init__(self, master, grid_size=10, num_pokemon=3, task=TASK_TWO):
        """
        Interaction between game model and view. It is a controller class

        Parameters:
            grid_size (int): the size of the grid used
            num_pokemon (int): number of hidden pokemon involved
            master (object): tkinter.Tk class used to represent 'master' window
            task (int): indication of different PokemonGame versions used
        """
        self._grid_size = grid_size
        self._master = master
        self._board_view = None
        self._num_pokemon = num_pokemon

        if not 1 < self._grid_size < 11:
            tk.messagebox.showerror(title="Grid_size invalid value",
                                                message="Grid_size must have a value of anything between or inclusive of 2 to 10")
            exit()
        if not -1 < self._num_pokemon < self._grid_size**2:
            tk.messagebox.showerror(title="Pokemon num invalid value",
                                                message="Pokemon number must have a value of anything between or inclusive of 0 to grid_size^2")
            exit()
        self._model = BoardModel(grid_size, num_pokemon)
        self._pokeball_left = self._model.get_num_pokeball_left()
        self._task = task

        self._master.geometry("{}x{}".format(700, 700))
        self._master.title("Pokemon: Got 2 Find Them All!")
        self._master.configure(bg="white")
        top_label = tk.Label(self._master, text="Pokemon: Got 2 Find Them All!", bg="#E06666", fg="white")
        top_label.config(font=("Courier New", 20, 'bold'))
        top_label.pack(fill='x', pady=(0,1))

        if self._task == TASK_TWO:
            # the variables below are used to reorganise the high score board
            # involves reshuffling and deleton of scores that were lower compared
            # to the new incoming scores in high_score_save_file method
            self._high_score_data = {}
            self._temp_score_data = {}
            self._high_score_exist = None

            # variables below are stored and shared among methods below
            self._congrats_box = None
            self._status_bar = None
            self._restart = None
            self._winner_name = None
            self._board_width_loaded = None
            self._store_prev_settings = {"Game_string": None, "Pokemon_locations": None,
                              "Grid_size": None, "Elapsed_time": None, "Board_width":None}
            self._data_to_save = None
            self._data_format = []
            # create menu bar
            menubar = tk.Menu(self._master)
            self._master.config(menu=menubar)

            # ensures high score file exists
            self.high_score_file()

            # within menu bar create file menu
            filemenu = tk.Menu(menubar, tearoff=False)
            menubar.add_cascade(label="File", menu=filemenu)

            # within fill menu - fill processing options available
            filemenu.add_command(label="Save game", command=self.save_game)
            filemenu.add_command(label="Load game", command=self.open_file)
            filemenu.add_command(label="Restart game", command=self.restart_game)
            filemenu.add_command(label="New game", command=self.new_game)
            filemenu.add_command(label="Quit", command=self.quit_game)
            filemenu.add_command(label="High Score", command=self.draw_high_score_window)
            self._timer_on = True
            
            self._status_bar = StatusBar(self._master, self.new_game, self.restart_game)
            self._master.after(0, self._status_bar.update_start_time())
        self.draw()
        
    def high_score_save_file(self,time,name):
        """
        Saves high score data of player who won game while beating other players
        to be the top 3 or top 1 if file doesn't exist

        Parameters:
            time (str): Time spent by player before completing game
            name (str): Name of player
        """
        filename = "Highscore_data_A3.txt"
        # this is a  temp dictionary with names as keys and values with
        # seconds integers
        temp_dict_scores = {}
        # this is a temp dictionary with names as keys and values with
        # 1m 20s string
        temp_dict_real_time = {}
        reformat_time_str = time.replace('m','').replace('s','').rstrip().split(' ')
        new_score = int(reformat_time_str[0])*60 + int(reformat_time_str[1])

        if name == "":
            tk.messagebox.showerror(title="Input Name please", message="Please input a name")
            self.congrats_box(time)
            self._master.wait_window(self._congrats_box)
            name_of_winner = self._winner_name.get()
            if name_of_winner == "":
                tk.messagebox.showerror(title="Nameless", message="Without a name - no record will be saved")
                return None
                
        if self._temp_score_data == {}:
            temp_dict_scores[name] = new_score
            temp_dict_real_time[name] = time 
        elif name in self._temp_score_data and new_score < self._temp_score_data[name]:
            temp_dict_scores[name] = new_score
            temp_dict_real_time[name] = time
        elif name in self._temp_score_data:
            pass
        else:
            count = 0
            for (player_name, before_scores), (_, before_time) in zip(self._temp_score_data.items(), self._high_score_data.items()):
                if len(self._temp_score_data) < 3:
                    if name not in temp_dict_scores:
                        temp_dict_scores[name] = new_score
                        temp_dict_real_time[name] = time
                    temp_dict_scores[player_name] = before_scores
                    temp_dict_real_time[player_name] = before_time
                else:
                    # if self._temp_score_data has 3 entries of high scores already
                    # it starts to get rid of old high scores and only keep the top 3
                    if count >= 3:
                        continue
                    elif new_score < before_scores and count < 2:
                        temp_dict_scores[name] = new_score
                        temp_dict_scores[player_name] = before_scores
                        temp_dict_real_time[name] = time
                        temp_dict_real_time[player_name] = before_time
                        count+=2
                    elif new_score == before_scores and count < 2:
                        temp_dict_scores[player_name] = before_scores
                        temp_dict_scores[name] = new_score
                        temp_dict_real_time[player_name] = before_time
                        temp_dict_real_time[name] = time
                        count+=2
                    elif count < 3:
                        temp_dict_scores[player_name] = before_scores
                        temp_dict_real_time[player_name] = before_time
                        count+=1

        self._high_score_data = {}
        self._temp_score_data = {}
        # below will only have 3 keys and values which indicates top 3 players
        for key in sorted(temp_dict_scores, key=temp_dict_scores.get, reverse=False):
            self._temp_score_data[key] = temp_dict_scores[key]
            self._high_score_data[key] = temp_dict_real_time[key]
                
        if self._temp_score_data:
            with open(filename, 'w') as file:
                for player_name, time in self._high_score_data.items():
                    file.write("%s: %s\n" % (player_name, time))
            
    def high_score_file(self):
        """
        Creates or updates data on high score of users
        """
        filename = "Highscore_data_A3.txt"
        # this is a dictionary with names as keys and values with seconds integers
        self._temp_score_data = {}
        store_score_data = {}
        # this is a dictionary with names as keys and values with 1m 20s string
        self._high_score_data = {}
        
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                file_data = file.readlines()

                for index, line in enumerate (file_data):
                    temp_minute = []
                    reformat_line = line.split(':')
                    # will be used to be displayed on top level window
                    total_time_str = reformat_line[1].rstrip()
                    # will be easier to sort highscores like this 
                    total_time_num = reformat_line[1].replace('m','').replace('s','').rstrip().split()

                    # converts string numbers to integers
                    for element in total_time_num:
                        temp_minute.append(int(element))

                    self._temp_score_data[reformat_line[0]] = temp_minute[0]*60 + temp_minute[1]
                    store_score_data[reformat_line[0]] = total_time_str

            # sort values from shortest time to longest
            for key in sorted(self._temp_score_data, key=self._temp_score_data.get, reverse=False):
                self._high_score_data[key] = store_score_data[key]
                
        else:
            # create file if file doesn't exist
            open(filename, 'w')

    def exit_high_score(self):
        """
        Exits high score top level window
        """
        self._high_score_exist.destroy()
    
    def draw_high_score_window(self):
        """
        Represents scores between top 3 players using most current data
        """
        # if window exists already - just destroy and redraw with latest data
        if self._high_score_exist:
            self._high_score_exist.destroy()
            self._high_score_exist = None
            
        top = tk.Toplevel(self._master)
        self._high_score_exist = top
        top.title("Top 3")
        top_label = tk.Label(top, text="High Scores", bg="#E06666", fg="white")
        top_label.config(font=("Courier New", 20, 'bold'))
        top_label.pack(fill='x', pady=5)
        if self._high_score_data != {}:
            for name, scores in self._high_score_data.items():
                score_label = tk.Label(top, text=name+': '+scores)
                score_label.pack(fill='x',side=tk.TOP, pady=2)

        done_button = tk.Button(top,
                                   text="Done", command=self.exit_high_score)
        done_button.pack(pady=5)
        
    def set_timer_off(self):
        """
        Timer will stop updating when game ends
        """
        self._timer_on = False
        self._status_bar.off_timer()

    def redraw(self):
        """
        Redraws game window
        """
        self._board_view.destroy()
        self.draw()

    def save_game(self):
        """
        Saves game. Just for additional information - the following will be saved
        text file:
        - current state of game string
        - grid size of game
        - locations of pokemon (intuitively gives number of pokemon in game)
        - number of pokeballs left
        - elapsed time (how long user have been playing so far)
        - board width of game board 
        """
        self._data_to_save = [
            "Game_string-" + str(self._model.get_game()), 
            "Grid_size-" + str(self._grid_size),
            "Pokemon_locations-" + str(self._model.get_pokemon_locations()),
            "Elapsed_time-" + str(self._status_bar.get_elapsed_time()),
            "Board_width-" + str(self._board_view.get_board_width())
            ]
        
        filename = filedialog.asksaveasfilename(
            initialfile="Untitled.txt", defaultextension=".txt",
            filetypes=[("Text Documents","*.txt")])
        if filename:
            file = open(filename, 'w', encoding="utf-8")
            for game_data in self._data_to_save:
                file.write(game_data + "\n")
            file.close()

    def open_file(self):
        """
        This loads a saved game file and restarts game to previous game setting
        """
        # used to check previous file's format and ensure all data must be present
        # for loading of file to be successfull
        self._store_prev_settings = {"Game_string": None, "Pokemon_locations": None,
                          "Grid_size": None, "Elapsed_time": None, "Board_width": None}

        # ensures only text file can be opened 
        filename = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])

        # user clicked cancel
        if not filename:
            return None
        try:
            file = open(filename, 'r', encoding="utf-8")
        except OSError:
            tk.messagebox.showerror(title="Error when loading file", message="File selected could not be loaded")
            return None
        
        file_data = file.readlines()

        # since file can be loaded properly and it exist, check validity and format
        # of file before letting it through to be processed by classes of game
        for data in file_data:
            format_data = data.rstrip("\n").split("-")
            
            if format_data[0] == "Grid_size" or format_data[0] == "Elapsed_time" or format_data[0] == "Board_width":
                if format_data[0] != "Elapsed_time":
                    try:
                        value = int(format_data[1])

                        if not 2 <= value <= 10 and format_data[0] == "Grid_size":
                            tk.messagebox.showerror(title="Grid_size invalid value",
                                                message="Grid_size must have a value of anything between or inclusive of 2 to 10")
                            file.close()
                            return None
                    except ValueError:
                        tk.messagebox.showerror(title="Grid_size value format",
                                                message="Grid_size and Board_width must only have integer digits as its' value")
                        file.close()
                        return None
                else:
                    try:
                        value = float(format_data[1])
                    except ValueError:
                        tk.messagebox.showerror(title="Elapsed_time value format",
                                                message="Elapsed_time must only have float digits as its' value")
                        file.close()
                        return None
                self._store_prev_settings[format_data[0]] = value
                
            elif format_data[0] == "Game_string":
                acceptable_char = FLAG + REVEALED + POKEMON + UNEXPOSED 
                for char in format_data[1]:
                    if char in acceptable_char:
                        pass
                    else:
                        tk.messagebox.showerror(title="Game_string value format",
                                                message="Game_string value string must only have either " +
                                                POKEMON + " or " + FLAG + " or " + UNEXPOSED + " or " + REVEALED)
                        file.close()
                        return None
                self._store_prev_settings[format_data[0]] = format_data[1]

            elif format_data[0] == "Pokemon_locations":
                acceptable_char = "(), " + REVEALED

                if format_data[1] == '' or format_data[1] == ' ':
                    tk.messagebox.showerror(title="Pokemon_locations value",
                                                message="Pokemon_locations value cannot be empty")
                    file.close()
                    return None
                
                for char in format_data[1]:
                    if char in acceptable_char:
                        pass
                    else:
                        tk.messagebox.showerror(title="Pokemon_locations value format",
                                                message="Pokemon_locations value string must have a tuple-like format. Eg '(1 ,2 , 30)'")
                        file.close()
                        return None
                self._store_prev_settings[format_data[0]] = tuple(format_data[1].replace("(","").replace(")","").split(","))
                turn_to_int = []
                for num in self._store_prev_settings[format_data[0]]:
                    turn_to_int.append(int(num))
                self._store_prev_settings[format_data[0]] = tuple(turn_to_int)
            else:
                tk.messagebox.showerror(title="Format of text file",
                                        message="text file is not in correct format it should have Grid_size, Pokeballs_left, Elapsed_time, Game_string and Pokemon_locations")
                file.close()
                return None
            
        file.close()
        for key in self._store_prev_settings:
            if self._store_prev_settings[key] is None:
                tk.messagebox.showerror(title="Missing values",message=key + " is missing " + ". Ensure formatting is correct")
                return None

        # since format is correct - need to ensure values inputted are logical
        # to ensure game runs smoothly
        if len(self._store_prev_settings["Game_string"]) != self._store_prev_settings["Grid_size"]**2:
            tk.messagebox.showerror(title="Game_string and Grid_size error", message="Game_string should have Grid_size^2 number of elements")
            return None

        messagebox.showinfo(title="Game loaded successfully",message="Game loaded! Click Ok to continue!")
        self.restart_with_load()
        
    def new_game(self):
        """
        Starts new game
        """
        self._model = BoardModel(self._grid_size, self._num_pokemon)
        # this is only for when an old game is loaded - to make sure it cease to
        # exist in new game
        self._status_bar.set_elapsed_time(0)
        self._restart = True
        self.redraw()

    def restart_game(self):
        """
        Restarts game
        """
        # not calling BoardModel class ensures random hidden generated pokemons
        # would not change
        self._model.restart_game_string()

        # this is only for when an old game is loaded - to make sure it cease to
        # exist in restart game
        self._status_bar.set_elapsed_time(0)
        self._restart = True
        self.redraw()

    def restart_with_load(self):
        """
        Ensures - game is 'restarted' with loaded game settings from before
        """
        self.restart_game()
        # variables defined for self reference and connection to methods involved
        grid_size = self._store_prev_settings["Grid_size"]
        pokemon_num = len(self._store_prev_settings["Pokemon_locations"])
        pokemon_loc = self._store_prev_settings["Pokemon_locations"]
        game_string = self._store_prev_settings["Game_string"]
        prev_elapsed_time_loaded = self._store_prev_settings["Elapsed_time"]
        self._board_width_loaded = self._store_prev_settings["Board_width"]

        #updates board_model with pokemon_num, pokemon_loc, game_string
        self._model.set_game_settings_open(pokemon_num, pokemon_loc, game_string, grid_size)
        self._num_pokemon = pokemon_num
        self._grid_size = self._store_prev_settings["Grid_size"]
        self._pokeball_left = self._model.get_num_pokeball_left()
        self._status_bar.set_elapsed_time(prev_elapsed_time_loaded)
        self.redraw()

    def quit_game(self):
        """
        Quit game
        """
        message_box = tk.messagebox.askyesno(title="Quit Game",message="Are you sure you would like to quit?")

        if message_box:
            self._master.destroy()
            exit()
    
    def draw(self):
        """
        Draws game to master window wwith most recent data
        """
        if self._task == TASK_ONE:
            # cells will not have images
            self._board_view = BoardView(self._master, self._grid_size)
            label_ids = self._board_view.draw_board(self._model.get_game())
        elif self._task == TASK_TWO:
            # cells will have images
            self._board_view = ImageBoardView(self._master, self._grid_size)

            if self._board_width_loaded:
                self._board_view.set_board_width(self._board_width_loaded)
                self._board_view_loaded = None
            
            label_ids = self._board_view.draw_board(self._model.get_game())

        # users will know which cell their mouse is currently on    
        self.bind_clicks_motion(label_ids)
        self._board_view.pack(side=tk.TOP)

        if self._task == TASK_TWO:
            # updates attempted catches and pokeballs left
            attempted_catches = self._model.get_num_attempted_catches()
            self._status_bar.update_pokeball_stats(attempted_catches,
                                                   self._model.get_num_pokeball_left())
            if self._restart:
                self._restart = False
                self._pokeball_left = self._model.get_num_pokeball_left()
                self._status_bar.update_pokeball_stats(attempted_catches,
                                                   self._model.get_num_pokeball_left())
                self._status_bar.update_start_time()
                self._timer_on = True
            
            if self._timer_on:
                self._master.after(0, self._status_bar.update_clock())
            else:
                self.set_timer_off()                
                
    def bind_clicks_motion(self, label_ids):
        """
        Bind clicks and motion on a label to the left and right click handlers.

        Parameters:
            label (tk.Widget): Label which clicks should bound to.
        """
        # bind left click and motion to allow user to find out where their cursor
        # is currently on
        for row_of_ids in label_ids:
            for label in row_of_ids:
                self._board_view.tag_bind(label, "<Button-1>",
                                          self._handle_left_click)
                self._board_view.tag_bind(label, "<Motion>",
                                          self._board_view.motion_detect)
                    
        # bind right click
        # right click can be either Button-2 or Button-3 depending on operating system
        for i in range(2,4):
            for row_of_ids in label_ids:
                for label in row_of_ids:
                    self._board_view.tag_bind(label, f"<Button-{i}>",
                                              self._handle_right_click)

    def _handle_left_click(self, clicked):
        """
        Handles tiles that are left clicked on the game board

        Parameters:
            clicked (tk.Event): This is an event object of the pixels of where the click
            occur
        """
        position = self._board_view.pixel_to_position((clicked.x, clicked.y))
        index = self._model.position_to_index(position)        
        character = self._model.number_at_cell(self._model.get_game(),
                                               self._model.get_pokemon_locations(),
                                               self._grid_size, index)
        # if clicked cell is flagged - do nothing
        if self._model.get_game()[index] == FLAG:
            pass
        # if clicked cell is revealed - do nothing
        elif self._model.get_game()[index] in REVEALED:
            pass
        else:
            self._model.replace_character_at_index(index, str(character))

            # chosen cell had a pokemon hidden!
            if self._model.check_loss():
                # user chose a cell with pokemon that wasn't flagged
                # expose all hidden pokemons
                for poke_index in self._model.get_pokemon_locations():
                    self._model.replace_character_at_index(poke_index, POKEMON)
                self.game_win_or_lost(False)
                

            # if chosen cell has no pokemon hidden - then run this block
            # this is done so whenever game restarts - clicked cell wouldn't get
            # through this block of code
            else:
                cell_need_visible = self._model.big_fun_search(self._model.get_game(),
                                                               self._grid_size,
                                                               self._model.get_pokemon_locations(),
                                                               index)
                
                for cell_index in cell_need_visible:
                    if self._model.get_game()[cell_index] == FLAG:
                        pass
                    else:
                        character = self._model.number_at_cell(self._model.get_game(),
                                                               self._model.get_pokemon_locations(),
                                                               self._grid_size, cell_index)
                        self._model.replace_character_at_index(cell_index, str(character))
                self.redraw()
                # once game string is fully updated after a click - we update board GUI

        # we then check if user has won
        if self._model.check_win():
            for poke_index in self._model.get_pokemon_locations():
                self._model.replace_character_at_index(poke_index, POKEMON)
            self.game_win_or_lost(True)

    def _handle_right_click(self, clicked):
        """
        Handles tiles that are right clicked on the game board

        Parameters:
            clicked (tk.Event): This is an event object of the pixels of where the click
            occur
        """
        # this is to keep track of number of pokeball left for TASK 2
        # if pokeball_left = 0, then user can't flag anymore cells then
        position = self._board_view.pixel_to_position((clicked.x, clicked.y))
        index = self._model.position_to_index(position)

        if self._model.get_game()[index] == FLAG:
            self._pokeball_left += 1
        if self._pokeball_left > 0 or self._task == TASK_ONE:
            if self._model.get_game()[index] == UNEXPOSED:
                self._pokeball_left -= 1
                
            self._model.flag_cell(index)

            if self._model.check_win():
                # win or lose - hidden pokemons will be exposed 
                for poke_index in self._model.get_pokemon_locations():
                        self._model.replace_character_at_index(poke_index, POKEMON)
                self.game_win_or_lost(True)
            self.redraw()
            

    def game_win_or_lost(self, status):
        """
        User clicked a cell with pokemon in it - causing game to terminate or
        restart depending on user's choice

        Parameter:
            status (bool): False if user lost game and True if user won
        """
        if self._task == TASK_TWO:
            self.set_timer_off()
        self.redraw()
        if status:
            if self._task == TASK_TWO:
                time_spent_by_player = self._status_bar.get_elapsed_time()
                minutes, seconds = divmod(time_spent_by_player, 60)
                seconds_only = int(minutes)*60 + int(seconds)
                player_time = "{:02d}m {:02d}s".format(int(minutes), int(seconds))

                if self._temp_score_data and len(self._temp_score_data) == 3:
                    for player_name, timing in self._temp_score_data.items():
                        if seconds_only < timing:
                            self.congrats_box(player_time)
                            self._master.wait_window(self._congrats_box)
                            name_of_winner = self._winner_name.get()
                            self.high_score_save_file(player_time, name_of_winner)
                            break
                else:
                    self.congrats_box(player_time)
                    self._master.wait_window(self._congrats_box)
                    name_of_winner = self._winner_name.get()
                    self.high_score_save_file(player_time, name_of_winner)
                
            message_box = tk.messagebox.askyesno(title="Game Over",message="You won! Would you like to play again?")
        else:
            message_box = tk.messagebox.askyesno(title="Game Over",message="You lose! Would you like to play again?")

        if message_box:
            self._model = BoardModel(self._grid_size, self._num_pokemon)
            self._restart = True
            self.redraw()
        else:
            self._master.destroy()
            exit()

    def congrats_box(self, time):
        """
        (str) Produces a second window and asks user to input name

        Parameters:
            time (str): time spent by player before completing game
        """
        self._congrats_box = tk.Toplevel(self._master)
        self._winner_name = tk.StringVar(value="")
        self._congrats_box.title("You are Top 3")
        message = tk.Label(self._congrats_box, text="You won in %s. Enter your name!" % time)
        message.pack(side=tk.TOP, fill='x')
        name_of_user = tk.Entry(self._congrats_box, textvariable=self._winner_name)
        name_of_user.pack()
        name_of_user.focus_force()
        exit_box = tk.Button(self._congrats_box, text="Enter", command=self._congrats_box.destroy)
        exit_box.pack(side=tk.TOP)
        
class BoardView(tk.Canvas):
    """
    Visual reprensetation of the game
    """
    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        """
        Updates visual of game whenever an interaction occurs if needed and
        constructs board view with game string.
        It is a view class

        Parameters:
            grid_size (int): the size of the grid used
            num_pokemon (int): number of hidden pokemon involved
            master (object): tkinter.Tk class used to represent 'master' window
            board_width (int): width of window size
        """
        super().__init__(master)
        self._board_width = board_width
        self._grid_size = grid_size

        self._board_layout = None
        self._board_ids = None
        self._previous_id_highlight = None
        # to get rid of excess spacings of the canvas which can cause error
        # from motion binded
        self.config(height=self._board_width-5, width=self._board_width-5)

    def set_board_width(self, board_width):
        """
        Sets board width - only used when new game is loaded

        Parameters:
            board_width (int): Number use to sized width and height of board
        """
        self._board_width = board_width
        self.config(height=board_width-5, width=board_width-5)

    def get_board_width(self):
        """
        (int) Gets board width of game board - which essentially is height as well
        """
        return self._board_width

    def motion_detect(self, motion):
        """
        Handles the change in borders of rectangle when there is motion on specific
        canvas

        Parameters:
            motion (tk.Event): This is an event object of pixels where motion occured
        """
        if self._previous_id_highlight:
            self.itemconfig(self._previous_id_highlight, width=1)
            
        y, x = self.pixel_to_position((motion.x, motion.y))
        self._previous_id_highlight = self._board_ids[y][x]
        self.itemconfig(self._previous_id_highlight, width=5)

    def draw_board(self, game_string):
        """
        (list<list<Tile>>)Draws entire board making up of Label to reflect game
        state and returns label_ids

        Parameters:
            board (str): game string that will be passed and used to produce board
            view
        """
        self._board_layout = self.reformat_game_string(game_string, self._grid_size)
        
        labels = []
        size = self._board_width / self._grid_size

        for y, row in enumerate(self._board_layout):
            board_row = []
            for x, game_element in enumerate(row):
                if game_element == POKEMON:
                    placement = self.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="yellow")
                elif game_element == FLAG:
                    placement = self.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="red")
                elif game_element == UNEXPOSED:
                    placement = self.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="dark green")
                elif game_element in REVEALED:
                    placement = self.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="light green")
                    
                board_row.append(placement)
            labels.append(board_row)
            
        self._board_ids = labels

        for y, row in enumerate(self._board_layout):
            for x, game_element in enumerate(row):
                if game_element in REVEALED:
                    x_pixel, y_pixel = self.position_to_pixel((y,x))
                    self.create_text(x_pixel, y_pixel, text=game_element)
        return labels

    def get_bbox(self, pixel):
        """
        (tuple<int, int, int, int>) Gives bounding box for given cell centered pixel coordinate

        Parameters:
            pixel (tuple): this will be pixel coordinates clicked on canvas
        """
        coord_x, coord_y = pixel

        for row_of_id in self._board_ids:
            for rectangle_id in row_of_id:
                X1, Y1, X2, Y2 = self.bbox(rectangle_id)
                if X1 <= coord_x <= X2 and Y1 <= coord_y <= Y2:
                    return X1, Y1, X2, Y2
                
    def position_to_pixel(self, position):
        """
        (tuple<int, int>) Returns center pixel for the cell at position (from game string)

        Parameters:
            position (tuple): this is position corresponding to game string 
        """
        row, col = position
        id_of_cell = self._board_ids[row][col]
        X1, Y1, X2, Y2 = self.bbox(id_of_cell)
        return (int((X1+X2)/2), int((Y1+Y2)/2))

    def pixel_to_position(self, pixel):
        """
        (tuple<int, int>) Returns position of cell (which also corresponds to
        index in game string) corresponding to pixels inputted

        Parameters:
            pixel (tuple<int, int>): pixel that corresponds to the vicinity a certain cell on
            windows 
        """
        coord_x, coord_y = pixel

        for y, row_of_id in enumerate(self._board_ids):
            for x, tile in enumerate(row_of_id):
                X1, Y1, X2, Y2 = self .bbox(tile)
                if X1 <= coord_x <= X2 and Y1 <= coord_y <= Y2:
                    return (y, x)

    def reformat_game_string(self, game_string, grid_size):
        """
        (list<list<str>>) Creates a list that has lists of columns of multiple
        game string

        Parameters:
            game_stirng (str): represents current status of game
        """
        reformated_game_string = []
        count = [i*grid_size for i in range(1, grid_size+1)]
        index = 0
        i = 0
        
        while i < grid_size:
            row = []
            for col in range(index, count[i]):
                row.append(game_string[col])
            reformated_game_string.append(row)
            index+=grid_size
            i+=1
        return reformated_game_string

class ImageBoardView(BoardView):
    """
    Provides images to the board game instead of normal boxes
    """
    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        """
        Updates visual of game whenever an interaction occurs if needed and
        constructs board view with game string. Additionally, it replacces
        rectangles with images for each cell 
        It is a view class

        Parameters:
            grid_size (int): the size of the grid used
            num_pokemon (int): number of hidden pokemon involved
            master (object): tkinter.Tk class used to represent 'master' window
            board_width (int): width of window size
        """
        super().__init__(master, grid_size, board_width, *args, **kwargs)
        self._board_imgs = 0
        self._id_image_update = None
        self._y_prev = None
        self._x_prev = None

    def draw_board(self, game_string):
        """
        (list<list<Tile>>)Draws entire board making up of Label to reflect game
        state and returns label_ids

        Parameters:
            board (str): game string that will be passed and used to produce board
            view
        """
        self._board_layout = self.reformat_game_string(game_string, self._grid_size)
        label_img_placed = []
        label_img_id = []
        size = math.ceil(self._board_width / self._grid_size)

        img_dict_of_pokemon = {
            POKEMON: ["images/pokemon_sprites/charizard.gif", "images/pokemon_sprites/cyndaquil.gif",
                      "images/pokemon_sprites/pikachu.gif", "images/pokemon_sprites/psyduck.gif",
                      "images/pokemon_sprites/togepi.gif", "images/pokemon_sprites/umbreon.gif"],
            FLAG: ["images/pokeball.gif"],
            UNEXPOSED: ["images/unrevealed.gif"],
            REVEALED: ["images/zero_adjacent.gif", "images/one_adjacent.gif",
                       "images/two_adjacent.gif", "images/three_adjacent.gif",
                       "images/four_adjacent.gif", "images/five_adjacent.gif",
                       "images/six_adjacent.gif", "images/seven_adjacent.gif",
                       "images/eight_adjacent.gif"]
            }
        
        for y, row in enumerate(self._board_layout):
            board_row_img_id = []
            board_row_img_placed = []
            for x, game_element in enumerate(row):
                if game_element in REVEALED:
                    img_temp = Image.open(img_dict_of_pokemon[REVEALED][int(game_element)])
                elif game_element == UNEXPOSED:
                    img_temp = Image.open(img_dict_of_pokemon[game_element][0])
                elif game_element == FLAG:
                    img_temp = Image.open(img_dict_of_pokemon[game_element][0])
                else:
                    random_poke = random.randint(0, 5)
                    img_temp = Image.open(img_dict_of_pokemon[game_element][random_poke])

                img_temp = img_temp.resize((int(size),int(size)))
                image = ImageTk.PhotoImage(img_temp)
                placement_img = self.create_image(x*size+size/2, y*size+size/2, image=image)
                
                board_row_img_id.append(placement_img)
                board_row_img_placed.append(image)
                
            label_img_placed.append(board_row_img_placed)
            label_img_id.append(board_row_img_id)
            self.image = label_img_placed
            
        self._board_ids = label_img_id
        return label_img_id

    def motion_detect(self, motion):
        """
        Handles the change in images on board when there is motion on specific
        canvas

        Parameters:
            motion (tk.Event): This is an event object of pixels where motion occured
        """
        UNEXPOSED_img = "images/unrevealed.gif"
        UNEXPOSED_MOVE_img = "images/unrevealed_moved.gif"
        
        size = math.ceil(self._board_width / self._grid_size)
        y, x = self.pixel_to_position((motion.x, motion.y))
        game_element = self._board_layout[y][x]

        img_temp_move = Image.open(UNEXPOSED_MOVE_img)
        img_temp_move = img_temp_move.resize((int(size),int(size)))
        image_move = ImageTk.PhotoImage(img_temp_move)

        img_temp_no_move = Image.open(UNEXPOSED_img)
        img_temp_no_move = img_temp_no_move.resize((int(size),int(size)))
        image_no_move = ImageTk.PhotoImage(img_temp_no_move)

        if game_element == UNEXPOSED:
            if self._id_image_update is None:
                self._id_image_update = self._board_ids[y][x]
                self._y_prev = y
                self._x_prev = x
                self.image[y][x] = image_move
                self.itemconfig(self._id_image_update, image=image_move)
            elif self._id_image_update is not None:
                self.image[self._y_prev][self._x_prev] = image_no_move
                self.itemconfig(self._id_image_update, image=image_no_move)
                self._id_image_update = self._board_ids[y][x]
                self._y_prev = y
                self._x_prev = x
                self.image[y][x] = image_move
                self.itemconfig(self._id_image_update, image=image_move)            

    def get_board_ids(self):
        """
        Get board_ids to be used to bind clicks while images drawn on rectangles
        """
        return self._board_ids
            
def main():
    """
    Initiate game!
    """
    root = tk.Tk()
    PokemonGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()




