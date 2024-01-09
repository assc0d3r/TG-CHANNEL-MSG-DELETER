from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

class KeywordDeleter:
    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.keywords = set()

    def start(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    def add_keyword(self, update: Update, context: CallbackContext):
        keyword = ' '.join(context.args)
        self.keywords.add(keyword)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Added keyword: {keyword}")

    def delete_message(self, update: Update, context: CallbackContext):
        message_text = update.message.text
        for keyword in self.keywords:
            if keyword in message_text:
                context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                break

    def run(self):
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('addkeyword', self.add_keyword))
        dp.add_handler(MessageHandler(Filters.text & (~Filters.command), self.delete_message))
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    kd = KeywordDeleter('YOUR_BOT_TOKEN')
    kd.run()
