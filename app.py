import time
import telegrambot

def main(romi_bot):
    resp = romi_bot.get_msg()
    print("Messages: ", len(resp['result']))
    for item in resp['result']:
        if 'entities' in item['message']:
            comando = item['message']['entities'][0]['type']
            if comando == "bot_command":
                romi_bot.parse(item)

romi_bot = telegrambot.telegram()
while True:
    main(romi_bot)
    time.sleep(1)