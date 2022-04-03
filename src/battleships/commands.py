from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CallbackQueryHandler
from .board_class import Board, SettingsBS, start_init, restart_init, check_if_can_place_ship, manually_place_ship
from .board_class import check_if_can_shoot, finish_the_game
import random

from ..language import *
from .localization import *
from ..start import local_lang

settings_bs = SettingsBS()
player1board = Board()
player2board = Board()


# """message handler for battleships"""
def message_handler_bs(update: Update, context: CallbackContext):
    global settings_bs, player1board, player2board
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    if update.message.text == f"⚓️ {dict['Battleships vs CPU']}" \
            or update.message.text == f"⚓️ {dict['Return to settings']}":
        settings_bs, player1board, player2board = restart_init(settings_bs, player1board, player2board)
        my_txt = f"{dict['Lets play']}!"
        keyboard = [[f"⚓️ {dict['Set ships']}"], ["🔙"]]
        field_placeholder = f"⚓️ {dict['️Battleships']} 🕹"
        reply_markup = ReplyKeyboardMarkup(keyboard, input_field_placeholder=field_placeholder,
                                           resize_keyboard=True)
        update.message.reply_text(my_txt, reply_markup=reply_markup)
        update.message.reply_text(f"{dict['Change desired settings']}:", reply_markup=generate_settings_keyboard())
    elif (settings_bs.player_p1_ships() == "Auto" and update.message.text == f"⚓️ {dict['Set ships']}") \
            or (update.message.text == f"⚓️ {dict['Set ships again']}" and settings_bs.player_p1_ships() == "Done") \
            or update.message.text == f"⚓️ {dict['Complete setup']}" and settings_bs.get_game_stage() == "start":
        settings_bs, player1board, player2board = start_init(settings_bs, player1board, player2board)
        keyboard = [[f"⚓️ {dict['Set ships again']}"], [f"⚓️ {dict['Return to settings']}"],
                    [f"💣 {dict['Start the game']}"],
                    ["🔙"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, input_field_placeholder=f"⚓️ {dict['Start']} 🕹",
                                           resize_keyboard=True)
        update.message.reply_text(f"🎮 {dict['Are you ready']}?", reply_markup=reply_markup)
        sea = create_sea_message(player1board.get_board(), player1board.get_list_of_ships())
        update.message.reply_text(sea, reply_markup=generate_sea_set_keyboard())
    elif update.message.text == f"⚓️ {dict['Set ships']}":
        keyboard = [[f"⚓️ {dict['Complete setup']}"], ["🔙"]]
        if len(player1board.get_list_of_ships()) == 10:
            keyboard = [[f"⚓️ {dict['Set ships again']}"], [f"⚓️ {dict['Return to settings']}"],
                        [f"💣 {dict['Start the game']}"],
                        ["🔙"]]
            settings_bs, player1board, player2board = start_init(settings_bs, player1board, player2board)
        reply_markup = ReplyKeyboardMarkup(keyboard, input_field_placeholder=f"⚓️ {dict['Set ships']}🕹",
                                           resize_keyboard=True)
        update.message.reply_text(f"🎮 {dict['Are you ready']}?", reply_markup=reply_markup)
        sea_plus = ""
        ship_to_set = player1board.get_ship_length_to_set() * '⏹'
        if ship_to_set == '⏹⏹⏹⏹':
            sea_plus = f"{dict['Set']} {ship_to_set}-{dict['cell ship']}: "
        sea = create_sea_message(player1board.get_board(), player1board.get_list_of_ships())
        update.message.reply_text(sea + sea_plus, reply_markup=generate_sea_set_keyboard())


# """generate keyboard with sea board depending on current player turn"""
def generate_sea_set_keyboard():
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    if settings_bs.player_p1_ships() != "Done":
        x = ["", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️"]
        y = ["", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️"]
        z = ["", "☑️", "☑️"]
        mhx = ["", "set:x1", "set:x2", "set:x3", "set:x4", "set:x5", "set:x6", "set:x7", "set:x8", "set:x9", "set:x10"]
        mhy = ["", "set:y1", "set:y2", "set:y3", "set:y4", "set:y5", "set:y6", "set:y7", "set:y8", "set:y9", "set:y10"]
        mhz = ["", "set:z1", "set:z2"]
        x_axes, y_axes, z_axes = settings_bs.get_x_y_z()
        x[x_axes], mhx[x_axes] = "✅", "empty"
        y[y_axes], mhy[y_axes] = "✅", "empty"
        z[z_axes], mhz[z_axes] = "✅", "empty"
        done_button_text = f"{dict['Select coordinates to set a ship']}:"
        done_button_value = "empty"
        if x_axes != 0 and y_axes != 0 and z_axes != 0:
            done_button_text = f"{dict['Set this ship']} ✅"
            done_button_value = "set:Done"
        if player1board.get_ship_length_to_set() == 1:
            kb_horizontal_text = "✅"
            kb_horizontal_value = "empty"
            kb_vertical_text = "✅"
            kb_vertical_value = "empty"
            settings_bs.set_z(random.randint(1, 2))
        else:
            kb_horizontal_text = f"{dict['Horizontal']}{z[2]}"
            kb_horizontal_value = f"{mhz[2]}"
            kb_vertical_text = f"{dict['Vertical']}{z[1]}"
            kb_vertical_value = f"{mhz[1]}"
        keyboard = [
            [InlineKeyboardButton(done_button_text, callback_data=done_button_value)],
            [InlineKeyboardButton(kb_horizontal_text, callback_data=kb_horizontal_value),
             InlineKeyboardButton(kb_vertical_text, callback_data=kb_vertical_value)],
            [InlineKeyboardButton(f"y1{y[1]}", callback_data=mhy[1]),
             InlineKeyboardButton(f"y2{y[2]}", callback_data=mhy[2]),
             InlineKeyboardButton(f"y3{y[3]}", callback_data=mhy[3]),
             InlineKeyboardButton(f"y4{y[4]}", callback_data=mhy[4]),
             InlineKeyboardButton(f"y5{y[5]}", callback_data=mhy[5])],
            [InlineKeyboardButton(f"y6{y[6]}", callback_data=mhy[6]),
             InlineKeyboardButton(f"y7{y[7]}", callback_data=mhy[7]),
             InlineKeyboardButton(f"y8{y[8]}", callback_data=mhy[8]),
             InlineKeyboardButton(f"y9{y[9]}", callback_data=mhy[9]),
             InlineKeyboardButton(f"y10{y[10]}", callback_data=mhy[10])],
            [InlineKeyboardButton(f"x1{x[1]}", callback_data=mhx[1]),
             InlineKeyboardButton(f"x2{x[2]}", callback_data=mhx[2]),
             InlineKeyboardButton(f"x3{x[3]}", callback_data=mhx[3]),
             InlineKeyboardButton(f"x4{x[4]}", callback_data=mhx[4]),
             InlineKeyboardButton(f"x5{x[5]}", callback_data=mhx[5])],
            [InlineKeyboardButton(f"x6{x[6]}", callback_data=mhx[6]),
             InlineKeyboardButton(f"x7{x[7]}", callback_data=mhx[7]),
             InlineKeyboardButton(f"x8{x[8]}", callback_data=mhx[8]),
             InlineKeyboardButton(f"x9{x[9]}", callback_data=mhx[9]),
             InlineKeyboardButton(f"x10{x[10]}", callback_data=mhx[10])]
        ]
    elif settings_bs.get_game_stage() == "set ships" and player1board.get_ships_left() == 10:
        keyboard = [[InlineKeyboardButton(f"{dict['Set ships and start the game']}⬇️", callback_data="empty")]]
        settings_bs.set_game_stage("start")
    else:
        ships = player1board.get_ships_left()
        done_button_text = f"{dict['Ships on board']}: {ships}"
        done_button_value = "empty"
        keyboard = [[InlineKeyboardButton(done_button_text, callback_data=done_button_value)]]
    markup = InlineKeyboardMarkup(keyboard)
    return markup


# """shooting keyboard
def generate_sea_guess_keyboard():
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    player = settings_bs.get_turn()
    players = settings_bs.get_players()
    if player == players["Player1"]:
        player_board = player2board
    else:
        player_board = player1board
    if player_board.get_ships_left() == 0:
        keyboard = [[InlineKeyboardButton(f"{dict['You win, no ships left']}!", callback_data="empty")]]
        finish_the_game(settings_bs, player1board, player2board)
    elif player == players["Player2"]:
        keyboard = [[InlineKeyboardButton(f"{dict['Pass turn to CPU']}!", callback_data="empty")]]
    else:
        x = ["", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️"]
        y = ["", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️"]
        mhx = ["", "shot:x1", "shot:x2", "shot:x3", "shot:x4", "shot:x5", "shot:x6", "shot:x7", "shot:x8", "shot:x9",
               "shot:x10"]
        mhy = ["", "shot:y1", "shot:y2", "shot:y3", "shot:y4", "shot:y5", "shot:y6", "shot:y7", "shot:y8", "shot:y9",
               "shot:y10"]
        x_axes, y_axes = settings_bs.get_x(), settings_bs.get_y()
        x[x_axes], mhx[x_axes] = "✅", "empty"
        y[y_axes], mhy[y_axes] = "✅", "empty"
        done_button_text = f"{dict['Select coordinates to shoot']}:"
        done_button_value = "empty"
        if x_axes != 0 and y_axes != 0:
            done_button_text = "Shoot!"
            done_button_value = "shot:Done"
        keyboard = [
            [InlineKeyboardButton(f"y1{y[1]}", callback_data=mhy[1]),
             InlineKeyboardButton(f"y2{y[2]}", callback_data=mhy[2]),
             InlineKeyboardButton(f"y3{y[3]}", callback_data=mhy[3]),
             InlineKeyboardButton(f"y4{y[4]}", callback_data=mhy[4]),
             InlineKeyboardButton(f"y5{y[5]}", callback_data=mhy[5])],
            [InlineKeyboardButton(f"y6{y[6]}", callback_data=mhy[6]),
             InlineKeyboardButton(f"y7{y[7]}", callback_data=mhy[7]),
             InlineKeyboardButton(f"y8{y[8]}", callback_data=mhy[8]),
             InlineKeyboardButton(f"y9{y[9]}", callback_data=mhy[9]),
             InlineKeyboardButton(f"y10{y[10]}", callback_data=mhy[10])],
            [InlineKeyboardButton(done_button_text, callback_data=done_button_value)],
            [InlineKeyboardButton(f"x1{x[1]}", callback_data=mhx[1]),
             InlineKeyboardButton(f"x2{x[2]}", callback_data=mhx[2]),
             InlineKeyboardButton(f"x3{x[3]}", callback_data=mhx[3]),
             InlineKeyboardButton(f"x4{x[4]}", callback_data=mhx[4]),
             InlineKeyboardButton(f"x5{x[5]}", callback_data=mhx[5])],
            [InlineKeyboardButton(f"x6{x[6]}", callback_data=mhx[6]),
             InlineKeyboardButton(f"x7{x[7]}", callback_data=mhx[7]),
             InlineKeyboardButton(f"x8{x[8]}", callback_data=mhx[8]),
             InlineKeyboardButton(f"x9{x[9]}", callback_data=mhx[9]),
             InlineKeyboardButton(f"x10{x[10]}", callback_data=mhx[10])],
        ]
    markup = InlineKeyboardMarkup(keyboard)
    return markup


# """Create sea map depending on current player turn"""
def create_sea_message(board, list_of_ships):
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    sea = f"➡️Y | 🌀 = {dict['Miss']} | ⏹ = {dict['Ship']}\n⬇️X | ✴️ = {dict['Hit']}    | ❌ = {dict['Sunk']} \n⏺1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟\n"
    for row in range(1, 11):
        if row == 10:
            square = "🔟"
        else:
            square = str(row) + "️⃣"
        sea += square
        for col in range(1, 11):
            if board[row][col] == "Empty":
                square = "🟦"
            elif board[row][col] == "Miss":
                square = "🌀"
            elif board[row][col] == "Out":
                square = "🌀"
            elif board[row][col] == "Ship":
                square = "⏹"
                for ship in list_of_ships:
                    if ship[0] == row and ship[1] == col:
                        if ship[2] == 2:
                            square = "◀️"
                        else:
                            square = "🔼️"
            elif board[row][col] == "Hit":
                square = "✴️"
            elif board[row][col] == "Sunk":
                square = "❌"
            if col == 10:
                square += "\n"
            sea += square
    return sea


# """Create sea map of the enemy without ships"""
def create_guess_sea_message(board):
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    if settings_bs.get_game_stage() == "shoot":
        sea = f"➡️Y | 🌀 = {dict['Miss']} | ⏹ = {dict['Ship']}\n⬇️X | ✴️ = {dict['Hit']}    | ❌ = {dict['Sunk']} \n⏺1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟\n"
    else:
        sea = f"➡️Y | ⏹ = {dict['Ship']}\n⬇️X |\n⏺1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟\n"
    # player = settings_bs.get_turn()
    # players = settings_bs.get_players()
    # if player == players["Player1"]:
    #     board = player2board.get_board()
    # else:
    #     board = player1board.get_board()
    for row in range(1, 11):
        if row == 10:
            square = "🔟"
        else:
            square = str(row) + "️⃣"
        sea += square
        for col in range(1, 11):
            if board[row][col] == "Empty" or board[row][col] == "Ship":
                square = "🟦"
            elif board[row][col] == "Miss" or board[row][col] == "Out":
                square = "🌀"
            elif board[row][col] == "Hit":
                square = "✴️"
            elif board[row][col] == "Sunk":
                square = "❌"
            if col == 10:
                square += "\n"
            sea += square
    return sea


# """settings keyboard message """
def generate_settings_keyboard():
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    set_ships_message = f"{dict['Set your ships']}:"
    ea, md, hd, p1, p2, sha, shm = "☑️", "☑️", "☑️", "☑️", "☑️", "☑️", "☑️"
    phea, phmd, phhd, php1, php2, phsha, phshm = "bat:EA", "bat:MD", "bat:HD", "bat:P1", "bat:P2", "bat:SHA", "bat:SHM"
    if settings_bs.get_difficulty() is not None:
        dif = settings_bs.get_difficulty()
        if dif == 1:
            ea = "✅"
            phea = "Empty"
        elif dif == 2:
            md = "✅"
            phmd = "Empty"
        elif dif == 3:
            hd = "✅"
            phhd = "Empty"
    if settings_bs.get_turn() is not None:
        turn = settings_bs.get_turn()
        players = settings_bs.get_players()
        if turn == players["Player1"]:
            p1 = "✅"
            php1 = "Empty"
        elif turn == players["Player2"]:
            p2 = "✅"
            php2 = "Empty"
    if settings_bs.player_p1_ships() == "Manual":
        shm = "✅"
        phshm = "Empty"
    elif settings_bs.player_p1_ships() == "Auto":
        sha = "✅"
        phsha = "Empty"
    if settings_bs.player_p1_ships() == "Done":
        set_ships_message = f"{dict['Set your ships: Done']} ✅"
    keyboard = [
        [
            InlineKeyboardButton(f"{dict['Set difficulty']}:", callback_data='empty')
        ],
        [
            InlineKeyboardButton(f"{dict['Easy']}{ea}", callback_data=F'{phea}'),
            InlineKeyboardButton(f"{dict['Medium']}{md}", callback_data=F'{phmd}'),
            InlineKeyboardButton(f"{dict['Hard']}{hd}", callback_data=F'{phhd}')
        ],
        [
            InlineKeyboardButton(f"{dict['Set turns']}:", callback_data='empty')
        ],
        [
            InlineKeyboardButton(f"{dict['You first']}{p1}", callback_data=F'{php1}'),
            InlineKeyboardButton(f"{dict['You second']}{p2}", callback_data=F'{php2}'),
        ],
        [
            InlineKeyboardButton(set_ships_message, callback_data='empty')
        ],
        [
            InlineKeyboardButton(f"{dict['Manually']}{shm}", callback_data=F'{phshm}'),
            InlineKeyboardButton(f"{dict['Automatically']}{sha}", callback_data=F'{phsha}')
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    return markup


# """Settings setup"""
def bs_settings_edit(update: Update, context: CallbackContext):
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    query = update.callback_query
    option = query.data.replace("bat:", "")
    """difficulty:
    "Easy" = 1
    "Medium" = 2
    "Hard" = 3
    """
    if option == "EA":
        settings_bs.set_difficulty(1)
    elif option == "MD":
        settings_bs.set_difficulty(2)
    elif option == "HD":
        settings_bs.set_difficulty(3)
    elif option == "P1" or option == "P2":
        settings_bs.next_turn()
    elif option == "SHM":
        settings_bs.set_ships_p1_manual()
    elif option == "SHA":
        settings_bs.set_ships_p1_auto()
    query.answer()
    query.edit_message_text(f"{dict['Change desired settings']}:", reply_markup=generate_settings_keyboard())


# """set user ships on board"""
def pre_game_update(update: Update, context: CallbackContext):
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    global player1board
    sea_plus = ""
    sea_end = ""
    query = update.callback_query
    option = query.data.replace("set:", "")
    if option[0] == "x":
        settings_bs.set_x(int(option.replace("x", "")))
    elif option[0] == "z":
        settings_bs.set_z(int(option.replace("z", "")))
    elif option[0] == "y":
        settings_bs.set_y(int(option.replace("y", "")))
    elif option == "Done":
        if check_if_can_place_ship(settings_bs, player1board) is True:
            player1board = manually_place_ship(settings_bs, player1board)
        else:
            sea_plus += f"{dict['Ships cannot touch each other or overlap the borders']}.\n"
        settings_bs.set_x(0)
        settings_bs.set_y(0)
        settings_bs.set_z(0)
    elif option == "Continue":
        settings_bs.set_game_stage("start")
        send_start_the_game_message(update, context)
    if player1board.get_ship_length_to_set() > 0:
        ship_to_set = player1board.get_ship_length_to_set() * '⏹'
        sea_plus += f"{dict['Set']} {ship_to_set}-{dict['cell ship']}: "
    sea = create_sea_message(player1board.get_board(), player1board.get_list_of_ships())
    query.answer()
    query.edit_message_text(sea_end + sea + sea_plus, reply_markup=generate_sea_set_keyboard())


# """user shooting"""
def shot_edit_update(update: Update, context: CallbackContext):
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    global player1board, player2board
    player = settings_bs.get_turn()
    players = settings_bs.get_players()
    if player == players["Player1"]:
        player_board = player2board
        # if settings_bs.difficulty == "Easy":
        player2board.set_out_around_sunk()
    else:
        player_board = player1board
    sea_plus = ""
    result = ""
    query = update.callback_query
    option = query.data.replace("shot:", "")
    if option[0] == "x":
        settings_bs.set_x(int(option.replace("x", "")))
    elif option[0] == "y":
        settings_bs.set_y(int(option.replace("y", "")))
    elif option == "Done":
        x_axes, y_axes, z_axes = settings_bs.get_x_y_z()
        if check_if_can_shoot(player_board, x_axes, y_axes) is True:
            result = player_board.shot_register(x_axes, y_axes)
            if result == "Hit":
                sea_plus += f"{dict['You Hit']}!\n"
            elif result == "Miss":
                sea_plus += f"{dict['You Miss']}!\n"
                settings_bs.next_turn()
            elif result == "Sunk":
                sea_plus += f"{dict['Good shot']}!\n"
                if len(player_board.get_list_of_ships()) > 0:
                    sea_plus += f"{dict['You have']} {player_board.get_ships_left()} {dict['ships left to sink']}.\n"
                elif len(player_board.get_ships_left()) == 0:
                    sea_plus += f"{dict['You have sunk all ships']}!\n"
                    settings_bs.next_turn()
        else:
            sea_plus += f"{dict['You cannot shoot there']}.\n"
        settings_bs.set_x(0)
        settings_bs.set_y(0)
    sea = create_guess_sea_message(player2board.get_board())
    query.answer()
    query.edit_message_text(sea + sea_plus, reply_markup=generate_sea_guess_keyboard())


# """message handler for shooting"""
def message_handler_bs_game(update: Update, context: CallbackContext):
    """dict select"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru

    global settings_bs, player1board, player2board
    settings_bs.set_game_stage("shoot")
    player = settings_bs.get_turn()
    players = settings_bs.get_players()
    if player1board.get_ships_left() == 0 or player2board.get_ships_left() == 0:
        winner, ships_left, shots_winner_shot, shots_loser_shot, turns_skipped, winner_shots_missed, loser_shots_missed = finish_the_game(
            settings_bs, player1board, player2board)
        win_message = f"{winner} {dict['won the game! With ships left']}: {ships_left} {dict['and']} {winner_shots_missed} {dict['shots missed of total']} {shots_winner_shot}. {dict['Loser missed']} {loser_shots_missed} {dict['of total']} {shots_loser_shot} {dict['shots.Game over after']} {turns_skipped} {dict['turns']}.\n"
        # context.bot.send_message(chat_id=update.effective_chat.id, text=win_message)
        keyboard = [["🔙"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, input_field_placeholder=f"💣 {dict['GAME OVER']} 🕹",
                                           resize_keyboard=False)
        update.message.reply_text(win_message, reply_markup=reply_markup)
    elif settings_bs.get_game_stage() == "shoot":
        if update.message.text == f"💣 {dict['Start the game']}":
            keyboard = [[f"💣 {dict['Next turn']}"], [" ", " ", " ", "🔙"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, input_field_placeholder=f"💣 {dict['Time to shoot']} 🕹",
                                               resize_keyboard=True)
            dict_dif = ["Easy", "Medium", "Hard"]
            i = settings_bs.get_difficulty() - 1
            start_game_message = f"{dict['You will fight on']} {dict[dict_dif[i]]} {dict['difficulty against CPU']}.\n {settings_bs.get_turn()} {dict['shoot first']}!"
            update.message.reply_text(start_game_message, reply_markup=reply_markup)
        elif update.message.text == f"💣 {dict['Print my sea']}":
            sea = create_sea_message(player1board.get_board(), player1board.get_list_of_ships())
            update.message.reply_text(sea, reply_markup=generate_sea_set_keyboard())
        elif update.message.text == f"💣 {dict['Print enemys sea']}":
            sea = create_guess_sea_message(player2board.get_board())
            update.message.reply_text(sea, reply_markup=generate_sea_guess_keyboard())
        elif update.message.text == f"💣 {dict['Next turn']}":
            if settings_bs.get_turn() == players["Player1"]:
                sea = create_guess_sea_message(player2board.get_board())
                update.message.reply_text(sea, reply_markup=generate_sea_guess_keyboard())
        if player == players["Player2"] and player == "Cpu":
            sea_plus = ""
            x, y = player1board.cpu_guess(settings_bs.get_difficulty())
            result = player1board.shot_register(x, y)
            sea = create_sea_message(player1board.get_board(), player1board.get_list_of_ships())
            if result == "Miss":
                # context.bot.send_message(chat_id=update.effective_chat.id,text=f"CPU shoot x{x}, y{y} and missed!\nYours turn!")
                sea_plus = f"{dict['CPU shoot']} x{x}, y{y} {dict['and misses! Your turn']}!"
                settings_bs.next_turn()
                # update.message.reply_text(sea+sea_plus, reply_markup=generate_sea_keyboard())
            elif result == "Hit":
                sea_plus = f"{dict['CPU shoot']} x{x}, y{y} {dict['and hit']}!"
            elif result == "Sunk":
                sea_plus = f"{dict['CPU sunk your ship']}!"
            update.message.reply_text(sea + sea_plus, reply_markup=generate_sea_set_keyboard())


# """"""
def init(dispatcher) -> None:
    dispatcher.add_handler(CallbackQueryHandler(pre_game_update, pattern=r'set\:(.+)'))
    dispatcher.add_handler(CallbackQueryHandler(bs_settings_edit, pattern=r'bat\:(.+)'))
    dispatcher.add_handler(CallbackQueryHandler(shot_edit_update, pattern=r'shot\:(.+)'))
    dispatcher.add_handler(MessageHandler(filters=Filters.regex(r'^💣'), callback=message_handler_bs_game))
    dispatcher.add_handler(MessageHandler(filters=Filters.regex(r'^⚓️'), callback=message_handler_bs))
