import random


# """settings:difficulty 1-3, number and length of ships,current turn,list of two players"""
class SettingsBS:
    def __init__(self):
        # """difficulty : "Easy" = 1,"Medium" = 2,"Hard" = 3"""
        self.difficulty = 1
        # """number of ships to set,[0] = ship_4,[1] = ship_3,[2] = ship_2,[3] = ship_1"""
        self.ships_to_set = [1, 2, 3, 4]
        """
        players default:
        "Player"
        "Cpu"
        """
        self.players = {"Player1": "Player", "Player2": "Cpu"}
        self.turn = self.players["Player1"]
        """
        set ships:
        "Manual"
        "Auto"
        "Done"
        """
        # """ships are set or not"""
        self.ships_p1 = "Auto"
        self.ships_p2 = "Auto"
        # """get axis from user"""
        self.axis = [0, 0, 0]
        self.skip_turn_on = False
        self.skip_turn_counter = 0
        self.game_stage = "set ships"
        """
        game stages:
        "set ships"
        "start"
        "shoot"
        """

    def set_skip_turn(self):
        self.skip_turn_on = True

    def reset_skip_turn(self):
        self.skip_turn_on = False
        self.skip_turn_counter = 0

    def get_game_stage(self):
        return self.game_stage

    def set_game_stage(self, stage):
        self.game_stage = stage

    def get_if_skip_turn(self):
        return self.skip_turn_on

    def get_x_y_z(self):
        return self.axis

    def set_x(self, x):
        self.axis[0] = x

    def set_y(self, y):
        self.axis[1] = y

    def get_x(self):
        return self.axis[0]

    def get_y(self):
        return self.axis[1]

    def set_z(self, z):
        self.axis[2] = z

    def get_difficulty(self):
        return self.difficulty

    # """set difficulty of cpu"""
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    # """return list of ships to set"""
    def get_ships_to_set(self):
        return self.ships_to_set

    # """get two names"""
    def set_players(self, player1, player2):
        self.players["Player1"], self.players["Player2"] = player1, player2

    # """return current player"""
    def get_turn(self):
        return self.turn

    def get_players(self):
        return self.players

    # """switch players"""
    def next_turn(self):
        if self.turn == self.players["Player1"]:
            self.turn = self.players["Player2"]
        else:
            self.turn = self.players["Player1"]
        self.skip_turn_counter += 1

    def player_p1_ships(self):
        return self.ships_p1

    def player_p2_ships(self):
        return self.ships_p2

    def set_ships_p1_manual(self):
        self.ships_p1 = "Manual"

    def set_ships_p1_auto(self):
        self.ships_p1 = "Auto"

    def set_ships_p2_auto(self):
        self.ships_p2 = "Auto"

    def finish_place_p1_ships(self):
        self.ships_p1 = "Done"

    def finish_place_p2_ships(self):
        self.ships_p2 = "Done"

    def finish_game(self):
        self.game_stage = "end"

    def get_turns_skipped(self):
        return self.skip_turn_counter


class Board:
    # ships_to_set = [1, 2, 3, 4]

    def __init__(self, board=None):
        """
        [0]:x
        [1]:y
        [2]:z
        [3]:length
        [4]:health
        """
        self.list_of_ships = []
        """
            board have values:
            "Empty" - nothing in this position
            "Miss" - registered miss
            "Ship" - ship
            "Hit"
            "Sunk"
        """
        self.board = [
            [
                "Border", "Border", "Border", "Border", "Border", "Border",
                "Border", "Border", "Border", "Border", "Border", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Border", "Border", "Border", "Border", "Border",
                "Border", "Border", "Border", "Border", "Border", "Border"
            ]
        ]
        self.ships_left = 10  # number of healthy ships left
        self.shots_fired = 0  # number of shots fired
        self.shots_missed = 0  # number of shots missed

    def get_shots_fired(self):
        return self.shots_fired

    def set_shots_fired(self):
        self.shots_fired += 1

    def get_shots_missed(self):
        return self.shots_missed

    def set_shots_missed(self):
        self.shots_missed += 1

    def get_board(self):
        return self.board

    # """save ships at placing"""
    def save_ship_to_list(self, x, y, z, length):
        """
        int:param x: horizontal
        int:param y: vertical
        int:param z: hor. or ver. operator
        int:param length: ships
        int:param health: ships health = ships length
        """
        health = length
        self.list_of_ships.append([x, y, z, length, health])

    # """check if the ship is sunk"""
    def if_sunk(self):
        if self.list_of_ships[4] == 0:
            return True

    # """return location value"""
    def get_xy_position(self, x, y):
        return self.board[x][y]

    # """modify x y position"""
    def set_xy_position(self, x, y, value):
        self.board[x][y] = value

    # """return key of hit ship"""
    def get_hit_ship(self, x, y):
        for hit_ship, ship in enumerate(self.list_of_ships):
            if ship[2] == 2:  # check for horizontal
                if ship[1] <= y < (ship[1] + ship[3]) and x == ship[0]:
                    return hit_ship
            elif ship[2] == 1:  # check for vertical
                if ship[0] <= x < (ship[0] + ship[3]) and y == ship[1]:
                    return hit_ship
        # return -1 # debug

    # """register shot x,y and minus hp if hit"""
    def shot_register(self, x, y):
        result = ""
        self.set_shots_fired()
        if self.get_xy_position(x, y) == "Empty":
            self.set_xy_position(x, y, "Miss")  # guess is miss
            result = "Miss"
            self.set_shots_missed()
        elif self.get_xy_position(x, y) == "Ship":
            hit = self.get_hit_ship(x, y)
            list_s = self.get_list_of_ships()
            ship = list_s[hit]
            if ship[4] <= ship[3]:  # ship health   # length_of_ship =  ship[3]
                self.set_xy_position(x, y, "Hit")  # hit
                result = "Hit"
                self.list_of_ships[hit][4] -= 1  # minus 1 hp
            if self.list_of_ships[hit][4] == 0:  # if no hp left
                self.minus_ship()
                result = "Sunk"
                for i in range(0, ship[3]):  # i = length of ship10
                    if ship[2] == 2:  # check for vertical ship
                        self.set_xy_position(ship[0], ship[1] + i, "Sunk")  # mark as sunk on board
                    elif ship[2] == 1:  # check for horizontal ship
                        self.set_xy_position(ship[0] + i, ship[1], "Sunk")  # mark as sunk on board
        return result

    def set_out_around_sunk(self):
        for row in range(1, 11):
            for col in range(1, 11):
                if self.get_xy_position(row, col) == "Sunk":
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 2):
                            if self.get_xy_position(i, j) == "Empty":
                                self.set_xy_position(i, j, "Out")

    def get_list_of_ships(self):
        return self.list_of_ships

    # """get number of ships left"""
    def get_ships_left(self):
        return self.ships_left

    # """mark one sunk ship"""
    def minus_ship(self):
        self.ships_left -= 1

    def cpu_guess(self, difficulty):
        x, y = -1, -1
        self.set_out_around_sunk()
        if difficulty == 3:
            x, y = self.cpu_guess_hard()
            if x != -1 and y != -1:
                return x, y
        for row in range(1, 11):  # choose target to shoot
            if x != -1 and y != -1:
                break
            else:
                for col in range(1, 11):  # search all the board
                    random_x = random.randrange(-1, 2, 2)  # add unpredictability
                    random_y = random.randrange(-1, 2, 2)
                    if self.board[row][col] == "Hit":
                        if self.board[row + random_x][col] in ["Empty", "Ship"]:
                            x = row + random_x
                            y = col
                            break
                        elif self.board[row][col + random_y] in ["Empty", "Ship"]:
                            x = row
                            y = col + random_y
                            break
                        elif self.board[row + (random_x * (-1))][col] in ["Empty", "Ship"]:
                            x = row + (random_x * (-1))
                            y = col
                            break
                        elif self.board[row][col + (random_y * (-1))] in ["Empty", "Ship"]:
                            x = row
                            y = col + (random_y * (-1))
                            break
        while x == -1 or y == -1:  # if the coordinates where not set yet
            x = random.randrange(1, 11)
            y = random.randrange(1, 11)
            if self.board[x][y] in ["Sunk", "Miss", "Hit", "Out", "Border"]:
                x = -1
                y = -1
        return x, y

    def restart_board(self):
        self.list_of_ships.clear()
        self.board.clear()
        self.board = [
            [
                "Border", "Border", "Border", "Border", "Border", "Border",
                "Border", "Border", "Border", "Border", "Border", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Empty", "Empty", "Empty", "Empty", "Empty",
                "Empty", "Empty", "Empty", "Empty", "Empty", "Border"
            ],
            [
                "Border", "Border", "Border", "Border", "Border", "Border",
                "Border", "Border", "Border", "Border", "Border", "Border"
            ]
        ]
        self.ships_left = sum([1, 2, 3, 4])

    def get_ship_length_to_set(self):
        if len(self.get_list_of_ships()) == 0:
            ship_to_set = 4
        elif len(self.get_list_of_ships()) == 1 or len(self.get_list_of_ships()) == 2:
            ship_to_set = 3
        elif 3 <= len(self.get_list_of_ships()) <= 5:
            ship_to_set = 2
        elif 6 <= len(self.get_list_of_ships()) <= 9:
            ship_to_set = 1
        else:
            ship_to_set = 0
        return ship_to_set

    def cpu_guess_hard(self):
        for x in range(1, 11):  # choose target to shoot
            for y in range(1, 11):  # search all the board
                if self.get_xy_position(x, y) == "Hit":  # find hits
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if self.get_xy_position(x + i, y + j) == "Empty":
                                self.set_xy_position(x + i, y + j, "Out")
                    random_l = [1, 2, 3, 4]
                    random.shuffle(random_l)
                    for j in random_l:
                        if j == 1:
                            for i in range(1, 3):
                                if x + i < 11:
                                    if self.get_xy_position(x + i, y) == "Hit":
                                        if self.get_xy_position(x + i + 1, y) in ["Ship", "Empty"]:
                                            return x + i + 1, y
                        if j == 2:
                            for i in range(1, 3):
                                if x - i > 0:
                                    if self.get_xy_position(x + (i * -1), y) == "Hit":
                                        if self.get_xy_position(x + ((i + 1) * -1), y) in ["Ship", "Empty"]:
                                            return x + ((i + 1) * -1), y
                        if j == 3:
                            for i in range(1, 3):
                                if y + i < 11:
                                    if self.get_xy_position(x, y + i) == "Hit":
                                        if self.get_xy_position(x, y + i + 1) in ["Ship", "Empty"]:
                                            return x, y + i + 1
                        if j == 4:
                            for i in range(1, 3):
                                if y - i > 0:
                                    if self.get_xy_position(x, y + (i * -1)) == "Hit":
                                        if self.get_xy_position(x, y + ((i + 1) * -1)) in ["Ship", "Empty"]:
                                            return x, y + ((i + 1) * -1)
                    random.shuffle(random_l)
                    for i in random_l:
                        if i == 1:
                            if self.get_xy_position(x + 1, y) in ["Ship", "Empty"]:
                                return (x + 1), y
                        if i == 2:
                            if self.get_xy_position(x - 1, y) in ["Ship", "Empty"]:
                                return (x - 1), y
                        if i == 3:
                            if self.get_xy_position(x, y + 1) in ["Ship", "Empty"]:
                                return x, (y + 1)
                        if i == 4:
                            if self.get_xy_position(x, y - 1) in ["Ship", "Empty"]:
                                return x, (y - 1)
        return -1, -1


# """choose a ship to place on board"""
def input_auto_ships(player_board):
    ships_to_set = [1, 2, 3, 4]
    ships_count = sum(ships_to_set)
    ship_to_set = int
    while ships_count != 0:
        if ships_to_set[0] != 0:  # 4 squares ship
            ship_to_set = 4
            ships_to_set[0] -= 1
        elif ships_to_set[1] != 0:  # 3 squares ship
            ship_to_set = 3
            ships_to_set[1] -= 1
        elif ships_to_set[2] != 0:  # 2 squares ship
            ship_to_set = 2
            ships_to_set[2] -= 1
        elif ships_to_set[3] != 0:  # 1 square ship
            ship_to_set = 1
            ships_to_set[3] -= 1
        ships_count = sum(ships_to_set)
        player_board, x, y, z = auto_place_ship(player_board, ship_to_set)
        player_board.save_ship_to_list(x, y, z, ship_to_set)
        # | 0=x | 1=y | 2=z | 3=ship length & hits |
    return player_board


def restart_init(settings_bs, player1board, player2board):
    if len(player2board.get_list_of_ships()) != 0:
        del player2board
        player2board = Board()
        settings_bs.set_ships_p2_auto()
    if len(player1board.get_list_of_ships()) != 0:
        del player1board
        player1board = Board()
        settings_bs.set_ships_p1_auto()
    return settings_bs, player1board, player2board


def start_init(settings_bs, player1board, player2board):
    if settings_bs.player_p2_ships() == "Done":
        del player2board
        player2board = Board()
        settings_bs.set_ships_p2_auto()
    if settings_bs.player_p1_ships() == "Done" and settings_bs.get_game_stage() == "set ships":
        del player1board
        player1board = Board()
        settings_bs.set_ships_p1_auto()
    if settings_bs.player_p2_ships() == "Auto":
        player2board = input_auto_ships(player2board)  # input cpu ships automatically
        settings_bs.finish_place_p2_ships()
    if settings_bs.player_p1_ships() == "Auto":
        player1board = input_auto_ships(player1board)
        settings_bs.finish_place_p1_ships()
    if len(player1board.get_list_of_ships()) == 11:
        settings_bs.finish_place_p1_ships()
    if len(player2board.get_list_of_ships()) == 11:
        settings_bs.finish_place_p2_ships()
    settings_bs.set_x(0)
    settings_bs.set_y(0)
    settings_bs.set_z(0)
    if settings_bs.player_p1_ships == "Done" and settings_bs.player_p2_ships == "Done":
        settings_bs.set_game_stage("shoot")
    return settings_bs, player1board, player2board


# """place a ship on board"""
def auto_place_ship(player_board, ship_to_set):
    z = x = y = int
    while ship_to_set != 0:
        x = random.randrange(1, 11)  # FIRST COORDINATE 1,2,3,4,5,6,7,8,9,10
        y = random.randrange(1, 11)  # SECOND COORDINATE 1,2,3,4,5,6,7,8,9,10
        z = random.randrange(1, 3)  # ORIENTATION AX 1,2
        flag = 0
        if z == 1:  # VERTICAL ORIENTATION
            if x + ship_to_set - 1 <= 10:
                for row in range(-1, ship_to_set + 1):
                    if player_board.get_xy_position(row + x, y) == "Ship" \
                            or player_board.get_xy_position(row + x, y - 1) == "Ship" \
                            or player_board.get_xy_position(row + x, y + 1) == "Ship":
                        flag = 0
                        break
                    else:
                        flag = 1
            if flag == 1:
                for row in range(ship_to_set):
                    player_board.set_xy_position(row + x, y, "Ship")
                ship_to_set = 0  # successful deploy
        if z == 2:  # HORIZONTAL ORIENTATION
            if y + ship_to_set - 1 <= 10:
                for col in range(-1, ship_to_set + 1):
                    if player_board.get_xy_position(x, y + col) == "Ship" \
                            or player_board.get_xy_position(x - 1, y + col) == "Ship" \
                            or player_board.get_xy_position(x + 1, y + col) == "Ship":
                        flag = 0
                        break
                    else:
                        flag = 1
            if flag == 1:
                for col in range(ship_to_set):
                    player_board.set_xy_position(x, y + col, "Ship")
                ship_to_set = 0  # successful deploy
    return player_board, x, y, z


def manually_place_ship(settings_bs, player_board):
    x, y, z = settings_bs.get_x_y_z()
    ship_to_set = player_board.get_ship_length_to_set()
    if z == 1:  # VERTICAL ORIENTATION
        for row in range(ship_to_set):
            player_board.set_xy_position(row + x, y, "Ship")  # successful deploy
    if z == 2:  # HORIZONTAL ORIENTATION
        for col in range(ship_to_set):
            player_board.set_xy_position(x, y + col, "Ship")  # successful deploy
    player_board.save_ship_to_list(x, y, z, ship_to_set)
    if player_board.get_ship_length_to_set() == 0:
        settings_bs.finish_place_p1_ships()
    return player_board


def check_if_can_place_ship(settings_bs, player_board):
    flag = 0
    x, y, z = settings_bs.get_x_y_z()
    ship_to_set = player_board.get_ship_length_to_set()
    if z == 1:  # VERTICAL ORIENTATION
        if x + ship_to_set - 1 <= 10:
            for row in range(-1, ship_to_set + 1):
                if player_board.get_xy_position(row + x, y) == "Ship" \
                        or player_board.get_xy_position(row + x, y - 1) == "Ship" \
                        or player_board.get_xy_position(row + x, y + 1) == "Ship":
                    flag = 0
                    break
                else:
                    flag = 1
    elif z == 2:  # HORIZONTAL ORIENTATION
        if y + ship_to_set - 1 <= 10:
            for col in range(-1, ship_to_set + 1):
                if player_board.get_xy_position(x, y + col) == "Ship" \
                        or player_board.get_xy_position(x - 1, y + col) == "Ship" \
                        or player_board.get_xy_position(x + 1, y + col) == "Ship":
                    flag = 0
                    break
                else:
                    flag = 1
    if flag == 1:
        return True
    else:
        return False


def check_if_can_shoot(player_board, x, y):
    if player_board.get_xy_position(x, y) not in ("Miss", "Hit", "Sunk"):
        return True
    else:
        return False


def finish_the_game(settings, player1board, player2board):
    settings.finish_game()
    if player1board.get_ships_left() == 0:
        ships_left = player2board.get_ships_left()
        winner = settings.get_players()["Player2"]
        shots_winner_shot = player2board.get_shots_fired()
        shots_loser_shot = player1board.get_shots_fired()
        winner_shots_missed = player2board.get_shots_missed()
        loser_shots_missed = player1board.get_shots_missed()
    else:
        winner = settings.get_players()["Player1"]
        ships_left = player1board.get_ships_left()
        shots_winner_shot = player1board.get_shots_fired()
        shots_loser_shot = player2board.get_shots_fired()
        winner_shots_missed = player1board.get_shots_missed()
        loser_shots_missed = player2board.get_shots_missed()
    turns_skipped = settings.get_turns_skipped()
    return winner, ships_left, shots_winner_shot, shots_loser_shot, turns_skipped, winner_shots_missed, loser_shots_missed
