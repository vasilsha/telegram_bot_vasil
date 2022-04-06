#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple TG bot

Root bot ini file
"""

import os
import logging

from dotenv import load_dotenv

from src.start import init as initStart
from src.echo import init as initEcho
from src.help import init as initHelp
from src.generator import init as initGenerator
from src.battleships import init as initBattleships
from src.choices import init as initChoices

load_dotenv()

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # updater = Updater(os.environ['BOT_API_TOKEN'])
    updater = Updater('Token')
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup handlers
    initStart(dispatcher)
    initGenerator(dispatcher)
    initBattleships(dispatcher)
    initChoices(dispatcher)
    initEcho(dispatcher)
    initHelp(dispatcher)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
