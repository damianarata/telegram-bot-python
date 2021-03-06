import requests
import os
import json
import subprocess

class telegram:
    def __init__(self):
        self.token      = os.getenv("TOKEN")
        self.url        = "https://api.telegram.org/bot{}/{}"
        self.update_id  = self.set_last_msg()
        self.operations = """
        /hello
        /console {command}

        Crypto value:
        /bitcoin
        """

    #Operations Functions
    def start(self, chatid):
        return  {
            'chat_id' : chatid,
            'text' : "This is are the operation available right now: {}".format(self.operations)
            }
    
    def hello(self, chatid, name):
        return  {
            'chat_id' : chatid,
            'text' : 'Hi {0}, welcome!!'.format(name)
            }

    def console(self, chatid, command):
        return  {
            'chat_id' : chatid,
            'text' : 'This is the response: {}'.format(subprocess.check_output(command, shell=True))
            }
    
    def bitcoin(self):
        #TODO
        pass

    #Support functions
    def get_msg(self):
        response = requests.get(url=self.url.format(self.token,"getUpdates"))
        resp = json.loads(response.text)
        return resp

    def set_last_msg(self):
        resp = self.get_msg()
        if 'result' in resp:
            return resp['result'][-1]['update_id']
        else:
            return 0

    def sendmsg(self, obj, update_id):
        resp = requests.post(url=self.url.format(self.token,"sendMessage"), data=obj)
        self.update_id = update_id
        return resp

    def parse(self, item):
        update_id = int(item['update_id'])
        if update_id > self.update_id:
            user = item['message']['from']['first_name']
            chatid = item['message']['chat']['id']
            text = item['message']['text'].split(" ")
            if text[0] == "/start":
                obj  = self.start(chatid)
            elif text[0] == "/hello":
                obj  = self.hello(chatid, user)
            elif text[0] == "/console":
                obj = self.console(chatid, text[1])
            resp = self.sendmsg(obj, update_id)
            print(resp.status_code, resp.text)
