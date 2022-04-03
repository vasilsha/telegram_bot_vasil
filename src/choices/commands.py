from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup, ParseMode, Dice
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CallbackQueryHandler

import random

from ..language import *
from .localization import *
from ..start import local_lang
from ..echo import last_five


def message_handler_ch(update: Update, context: CallbackContext):
    """ """
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru
    keyboard = [[f"🎲 {dict['throw_dice']}"], [f"🎲 {dict['yes_or_no']}"], [f"🎲 {dict['random_choice']}"], ["🔙"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, input_field_placeholder=f"🎲 {dict['random']}",
                                       resize_keyboard=True)
    if update.message.text == f"🎲 {dict['random_choices']}":
        my_txt = f"{dict['randomize']}..."
        update.message.reply_text(my_txt, reply_markup=reply_markup)
    elif update.message.text == f"🎲 {dict['throw_dice']}":
        update.message.reply_dice("🎲")
    elif update.message.text == f"🎲 {dict['yes_or_no']}":
        my_txt = random.choice(["👍", "👎"])
        update.message.reply_text(my_txt, reply_markup=reply_markup)
    elif update.message.text == f"🎲 {dict['random_choice']}":
        my_txt = f"{dict['enter_your_choices']}."
        keyboard = [[InlineKeyboardButton("🎲 OK", callback_data='cho:ok')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(my_txt, reply_markup=reply_markup)


def random_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    # data = query.data   """no need for this with one option"""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru
    if len(last_five) != 0:
        input_txt = last_five[-1]
        last_five.pop()
        choices_list = input_txt.split(",")
        random.shuffle(choices_list)
        my_txt = f"{dict['randomly_chosen']}: {random.choice(choices_list)}"
    else:
        my_txt = f"{dict['no_choices_to_randomize']}."
    query.answer()
    query.edit_message_text(text=my_txt)


def init(dispatcher) -> None:
    dispatcher.add_handler(CallbackQueryHandler(random_choice, pattern=r'cho\:(.+)'))
    dispatcher.add_handler(MessageHandler(filters=Filters.regex(r'^🎲'), callback=message_handler_ch))
