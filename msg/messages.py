import telepot

bot = telepot.Bot('5339051919:AAGKrrqLkmGaXUhlBI02lDQsk637xDki7Us')
receiver_id = '655256005'


def send_message(text):
    bot.sendMessage(receiver_id, text=text)

