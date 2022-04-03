from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


last_five = []


def echo(update: Update, context: CallbackContext) -> None:
    """save last five messages"""
    global last_five
    if len(last_five) > 4:
        last_five.pop(0)
    last_five.append(update.message.text)
    """Echo the user message."""
    # update.message.reply_text(update.message.text)


def init(dispatcher) -> None:
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
