import requests
import json
import time
cred=""

class telegram:
    def __init__(self):
        f = open("wrapper.txt", "r")
        self.update_id = int(f.read())
        f.close


    def start(self, chatid, update_id):
        url = "https://api.telegram.org/bot{0}/sendMessage".format(cred)
        obj = {
            'chat_id' : chatid,
            'text' : "Comenzamos"
        }
        resp = requests.post(url, data = obj)
        print(resp, "start")
        f = open("wrapper.txt", "w")
        f.write(str(update_id))
        f.close
    
    def saludo(self, chatid, update_id, nombre):
        url = "https://api.telegram.org/bot{0}/sendMessage".format(cred)
        obj = {
            'chat_id' : chatid,
            'text' : 'Hola {0}, bienvenido!!'.format(nombre)
        }
        resp = requests.post(url, data = obj)
        print(resp, "saludo")
        f = open("wrapper.txt", "w")
        f.write(str(update_id))
        f.close
        

    def parseo(self, item):
        update_id = int(item['update_id'])
        if update_id > self.update_id:
            usuario = item['message']['from']['id']
            chatid = item['message']['chat']['id']
            text = item['message']['text'].split("-")
            if text[0] == "/start":
                self.start(chatid,update_id)
            if text[0] == "/saludo":
                self.saludo(chatid, update_id, text[1])

def main():
    telegrambot = telegram()
    url = "https://api.telegram.org/bot{0}/getUpdates".format(cred)
    response = requests.get(url)
    resp = json.loads(response.text)
    for item in resp['result']:
        try:
            comando = item['message']['entities'][0]['type']
            if comando == "bot_command":
                telegrambot.parseo(item)          
        except:
            pass

while True:
    main()
    time.sleep(1)