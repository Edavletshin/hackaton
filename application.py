from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from flask import Flask, render_template
app = Flask(__name__)

TG_TOKEN = "849661734:AAEppr89hTnLZ0qRV3KacJAE8hRKV88Gx5E"

@app.route('/')
def hello_name(user):
   return render_template('hello.html', name = user)

def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Я хочу увидеть, как ты приседаешь! Я подскажу, если ты медленно убиваешь свои колени или что-то еще",
    )


def do_echo(bot: Bot, update: Update):
    text = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Ты что делаешь??? Ты что??? Ты видос должен кидать, а не баллады писать  ",
    )

def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
#    main()
   app.run(debug = True)
   app.run()
