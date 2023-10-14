class Logger:
    @staticmethod
    def log_to_group(bot, message_text):
        bot.send_message(Config.LOGGER_GROUP_ID, message_text)
