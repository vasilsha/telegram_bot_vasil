from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CallbackQueryHandler

from .pass_generator import pass_gen, SettingsPG

from ..language import *
from .localization import *
from ..start import local_lang


settings_pg = SettingsPG(10, True, True, True, False, False, False)
allowed_settings = {
    "L8": 1,
    "L16": 2,
    "L24": 3,
    "LLT": 4,
    "LLF": 5,
    "ULT": 6,
    "ULF": 7,
    "DGT": 8,
    "DGF": 9,
    "LNLT": 10,
    "LNLF": 11,
    "UNLT": 12,
    "UNLF": 13,
    "SCT": 14,
    "SCF": 15
}


def generate_keyboard():
    global settings_pg
    """Propose message"""
    if settings_pg.get_low_c_latin():
        tof_ll = "✅"
        ll = "T"
    else:
        tof_ll = "❌"
        ll = "F"
    if settings_pg.get_up_c_latin():
        tof_ul = "✅"
        ul = "T"
    else:
        tof_ul = "❌"
        ul = "F"
    if settings_pg.get_digit():
        tof_dg = "✅"
        dg = "T"
    else:
        tof_dg = "❌"
        dg = "F"
    if settings_pg.get_low_c_no_latin():
        tof_lnl = "✅"
        lnl = "T"
    else:
        tof_lnl = "❌"
        lnl = "F"
    if settings_pg.get_up_c_no_latin():
        tof_unl = "✅"
        unl = "T"
    else:
        tof_unl = "❌"
        unl = "F"
    if settings_pg.get_special_char():
        tof_sc = "✅"
        sc = "T"
    else:
        tof_sc = "❌"
        sc = "F"
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru
    keyboard = [
        [
            InlineKeyboardButton(f"8 {dict['symbols']}", callback_data='gen:L8'),
            InlineKeyboardButton(f"16 {dict['symbols']}", callback_data='gen:L16'),
            InlineKeyboardButton(f"24 {dict['symbols']}", callback_data='gen:L24')
        ],
        [
            InlineKeyboardButton(f"{tof_ll}{dict['lower_latin']}", callback_data=f'gen:LL{ll}'),
            InlineKeyboardButton(f"{tof_ul}{dict['upper_latin']}", callback_data=f'gen:UL{ul}')],
        [
            InlineKeyboardButton(f"{tof_lnl}{dict['lower_non_latin']}", callback_data=f'gen:LNL{lnl}'),
            InlineKeyboardButton(f"{tof_unl}{dict['upper_non_latin']}", callback_data=f'gen:UNL{unl}')
        ],
        [
            InlineKeyboardButton(f"{tof_dg}{dict['digits']}", callback_data=f'gen:DG{dg}'),
            InlineKeyboardButton(f"{tof_sc}{dict['special_symbols']}", callback_data=f'gen:SC{sc}')
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    return markup


def message_handler_pg(update: Update, context: CallbackContext):
    global settings_pg
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru
    if update.message.text == f"🔑 {dict['pass_gen']}":
        keyboard = [["🔙"]]
        my_txt = f"{dict['generating']}..."
        reply_markup = ReplyKeyboardMarkup(keyboard, input_field_placeholder=f"🔑 {dict['pass_gen']}", resize_keyboard=True)
        update.message.reply_text(my_txt, reply_markup=reply_markup)
        password = pass_gen(settings_pg)
        update.message.reply_text(f"<code>{password}</code>\n{dict['select_new_password']}",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=generate_keyboard())


def pass_edit(update: Update, context: CallbackContext):
    global settings_pg
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru
    query = update.callback_query
    option = query.data.replace("gen:", "")
    if option in allowed_settings:
        if option == "L8":
            settings_pg.set_length(8)
        elif option == "L16":
            settings_pg.set_length(16)
        elif option == "L24":
            settings_pg.set_length(24)
        elif option == "LLT":
            settings_pg.set_low_c_latin(False)
        elif option == "LLF":
            settings_pg.set_low_c_latin(True)
        elif option == "ULT":
            settings_pg.set_up_c_latin(False)
        elif option == "ULF":
            settings_pg.set_up_c_latin(True)
        elif option == "DGT":
            settings_pg.set_digit(False)
        elif option == "DGF":
            settings_pg.set_digit(True)
        elif option == "LNLT":
            settings_pg.set_low_c_no_latin(False)
        elif option == "LNLF":
            settings_pg.set_low_c_no_latin(True)
        elif option == "UNLT":
            settings_pg.set_up_c_no_latin(False)
        elif option == "UNLF":
            settings_pg.set_up_c_no_latin(True)
        elif option == "SCT":
            settings_pg.set_special_char(False)
        elif option == "SCF":
            settings_pg.set_special_char(True)
        if settings_pg.check_pass_empty():
            settings_pg.set_low_c_latin(True)
    query.answer()
    password = pass_gen(settings_pg)
    query.edit_message_text(f"<code>{password}</code>\n{dict['select_new_password']}",
                            parse_mode=ParseMode.HTML,
                            reply_markup=generate_keyboard())


def init(dispatcher) -> None:
    dispatcher.add_handler(CallbackQueryHandler(pass_edit, pattern=r'gen\:(.+)'))
    dispatcher.add_handler(MessageHandler(filters=Filters.regex("^🔑"), callback=message_handler_pg))
