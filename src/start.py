from telegram import Update, ForceReply, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from .language import *
from .localization import *

local_lang = LanguageLocalize()


def menu_run():
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru
    keyboard = [[KeyboardButton(f"🔑 {dict['pass_gen']}")],
                [KeyboardButton(f"🎲 {dict['rand_gen']}")],
                [KeyboardButton(f"⚓️ {dict['bat_sh']}")],
                [KeyboardButton("/start"), KeyboardButton(f"🗺 {dict['lang']}"), KeyboardButton("/help")]]
    placeholder = dict['place_holder']
    markup = ReplyKeyboardMarkup(keyboard, input_field_placeholder=placeholder, resize_keyboard=True)
    return markup


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    markup = menu_run()
    if local_lang.get_language() == 'en':
        loc_txt = "Hi"
    else:  # ru
        loc_txt = "Привет"
    update.message.reply_markdown_v2(fr'{loc_txt} {user.mention_markdown_v2()}\!', reply_markup=markup)


def back(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /back is issued.
    same as start but different message"""
    markup = menu_run()
    update.message.reply_text('Choose from given options:', reply_markup=markup)


def language_change(update: Update, context: CallbackContext) -> None:
    """Change language"""
    if update.message.text == "🗺 Русский":
        local_lang.set_language('ru')
        update.message.reply_text('Язык изменён на Русский')
    elif update.message.text == "🗺 English":
        local_lang.set_language('en')
        update.message.reply_text('Language changed to English')
    start(update, context)


def init(dispatcher) -> None:
    """Setup handler for the section"""
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("back", back))
    dispatcher.add_handler(MessageHandler(filters=Filters.regex("🔙"), callback=back))
    dispatcher.add_handler(MessageHandler(filters=Filters.regex("🗺"), callback=language_change))
