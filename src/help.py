from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from .language import *
from .localization import *
from .start import local_lang


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if local_lang.get_language() == 'en':
        dict = start_menu_dict_en
    else:  # ru
        dict = start_menu_dict_ru
    update.message.reply_text(f"{dict['help']}")


def init(dispatcher) -> None:
    dispatcher.add_handler(CommandHandler("help", help_command))

