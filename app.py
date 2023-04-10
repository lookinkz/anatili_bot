from telegram.ext import Updater, CommandHandler

updater = Updater(token='6082204807AAGlp7P-dOo1fEEMh_67BIeJOaEgLSqrbWc')

# define a command handler for the /start command


def start(update, context):
    # Greeting text is here
    greeting = "Салем!\n Менің атым Қарлығаш!\n\nБот создан для развития казахского языка."

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=greeting)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()


# define a message handler for handling all other messages
def echo(update, context):
    # get the user's message text
    message_text = update.message.text

    # echo the message back to the user
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message_text)
