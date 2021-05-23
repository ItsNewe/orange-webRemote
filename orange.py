from configparser import ConfigParser
from flask import Flask, render_template, request, redirect
import sys
import requests

"""
MODES:
0 : envoi unique de touche
1 : appui prolongé de touche
2 : relacher la touche après un appui prolongé
"""
config = ConfigParser()
config.read('config.ini')
if not (config["DEFAULT"]['tvHost']):
    print('Configuration file is invalid, exiting.')
    sys.exit(0)

tvHost=config["DEFAULT"]['tvHost']
baseUrl=f"http://{tvHost}:8080/remoteControl/cmd?operation="

class Remote:
    def __init__(self):
        self.baseUrl=baseUrl
        self.touches={
        "ON" : "116",
        "0"     : "512",
        "1"     : "513",
        "2"     : "514",
        "3"     : "515",
        "4"     : "516",
        "5"     : "517",
        "6"     : "518",
        "7"     : "519",
        "8"     : "520",
        "9"     : "521",
        "CH+"   : "402",
        "CH-"   : "403",
        "VOL+"  : "115",
        "VOL-"  : "114",
        "MUTE"  : "113",
        "UP"    : "103",
        "DOWN"  : "108",
        "LEFT"  : "105",
        "RIGHT" : "106",
        "OK"    : "352",
        "BACK"  : "158",
        "MENU"  : "139",
        "PLAY/PAUSE" : "164",
        "FBWD"  : "168",
        "FFWD"  : "159",
        "REC"   : "167",
        "VOD"   : "393"
        }
        self.isOn=None

    def remoteInstruction(self, action, keyCode=None, mode=0):
        finalUrl=f"{self.baseUrl}01&key={self.touches.get(str.upper(action))}&mode={mode}"
        req = requests.get(finalUrl)
        return req.status_code
    
    def getStatus(self):
        req = requests.get(f"{self.baseUrl}10")
        rj = req.json()
        print(rj)
        try:
            if(rj['result']['responseCode']!=-1):
                if(rj['result']['data']['activeStandbyState']==0):
                    self.isOn=True
                else:
                    self.isOn=False
            else:
                self.isOn=False
        except:
            self.isOn=False
        return self.isOn
    
    def gotoChaine(self, chaine):
        finalUrl=f"{self.baseUrl}09&epg_id={chaineId}&uui=1"

##WEBSERVER SETUP
app = Flask(__name__)
rClient = Remote()
@app.route('/')
def index():
    return render_template('index.html', data=list(rClient.touches), isOn=rClient.getStatus())

@app.route('/keyPress', methods=["POST"])
def keyPress():
    action = request.form['action']
    rClient.remoteInstruction(action)
    return redirect('/')
    
if __name__ == "__main__":
    rConsole = Remote()
    rConsole.getStatus()
    app.run(host="0.0.0.0", port=5555)





















