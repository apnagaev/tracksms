import datetime
import http.server
import socketserver
import urllib.parse
import re
import requests
import linecache
import json
import telebot
import urllib
from urllib.parse import unquote


print ("---------------start----------------")
with open('userdevices.txt') as devfile:
  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} open conf json file')
  devf = devfile.read()
  devj = json.loads(devf)

with open('smsconf.txt') as conffile:
  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} open conf json file')
  conff = conffile.read()
  confj = json.loads(conff)


#print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} youre configuration is\n{confj[0]}')

######must be filled
bot = telebot.TeleBot(confj[0]["botkey"])
port1=confj[0]["port"]
key=""
key='/'+key

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/x-www-form-urlencoded')
        self.end_headers()
    def do_POST(self):


        uri=urllib.parse.unquote(self.path)
        if uri.startswith(key):
          try:
            content_len = self.headers.get("Content-Length")
            body = self.rfile.read(int(content_len))
            body = urllib.parse.unquote(body)
            body = body.replace('+', ' ')
            print(f'{bcolors.HEADER}{datetime.datetime.now().strftime("%Y-%m-%d %X")} headers=\n{self.headers}\n{body}{bcolors.ENDC}')
            self._set_headers()
            self.send_response(200)
            self.end_headers()
            self.path = 'true.txt'

            for item in devj:
              titem='#deviceid'+item["devid"]
              if titem in body:
                  print(f'{bcolors.HEADER}{datetime.datetime.now().strftime("%Y-%m-%d %X")} dev {item["devid"]} in body{bcolors.ENDC}')
                  text = re.search('text=(.*)', body, re.DOTALL)
                  text = text.group(1)
                  print(f'{bcolors.HEADER}{datetime.datetime.now().strftime("%Y-%m-%d %X")} text={text}\nchatid={item["chatid"]}{bcolors.ENDC}')
                  bot.send_message(item["chatid"], text)


          except:
            print(f'{bcolors.FAIL}{datetime.datetime.now().strftime("%Y-%m-%d %X")} parsing fail!{bcolors.ENDC}')
        else:
          message = "key failure"
          self.send_response(400)
          self.path = 'fail.txt'
        if (self.path == 'true.txt'):
           print(f'{bcolors.OKGREEN}{datetime.datetime.now().strftime("%Y-%m-%d %X")} script finished for device {bcolors.ENDC}')
        else:
          print(f'{bcolors.FAIL}{datetime.datetime.now().strftime("%Y-%m-%d %X")} false={self.client_address} device={bcolors.ENDC}')
    def do_GET(self):
      self.send_response(403)
      self.path = 'fail.txt'

handler = CustomHttpRequestHandler
try:
  port=port1
  server=socketserver.TCPServer(("", port), handler)
except:
  port=port2
  server=socketserver.TCPServer(("", port), handler)
print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} Server started at port {port}. Press CTRL+C to close the server.')
try:
  server.serve_forever()
  httpd.timeout = 5
except KeyboardInterrupt:
  server.server_close()
  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} Server Closed')
