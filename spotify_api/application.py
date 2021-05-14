from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def checkKey(token):
    import requests
    import json

    url = "https://api.spotify.com/v1/me"
    payload={}
    headers = {
    'Authorization': token,
    'Cookie': 'sp_t=c619b1d8cf10a0d45638c388bbf6ce3b; sp_landing=https%3A%2F%2Fopen.spotify.com%2Fartist%2F3z97WMRi731dCvKklIf2X6'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.json()
    if 'error' in res:
        print('token checking : not found')
        return False
    else:
        print('token checking : Found')
        return True


def generateToken():
    import requests
    import json

    url = "https://accounts.spotify.com/api/token"

    payload='grant_type=refresh_token&refresh_token=AQB_ajqK3XpUDsKCtVZJLZJ76TfZWBMFGsOmylVciTMIHWGKa_aQjkYd2Naa4Yvj8VQsinW8TZWnN-9CCEr563nqatbjs6hD9PMBKzArWSar1xj7g7wkglVMRJrOTRVrn3U'
    headers = {
    'Authorization': 'Basic MmFjZjEyNDQzOGI3NDQwODk0MmRhM2ExMTYyNjdhZjY6NWMzNzM2YmM2ZDY1NDc4MDgwYWRhOWIzNjdlYjMyMzM=',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'sp_t=c619b1d8cf10a0d45638c388bbf6ce3b; sp_landing=https%3A%2F%2Fopen.spotify.com%2Fartist%2F3z97WMRi731dCvKklIf2X6; __Host-device_id=AQAGQMh2YD9GFBrK6r1hM9nAwkkT1cLXaRj8XQxXq5cr_AqvNOKIqdb00SrfD37dbkNe8D9m2puZGnCmcJnWRCvsnSWuTjf4dMo'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    dict = response.json()
    print('dictionary returned: gebnerated token \n', dict['access_token'])
    #print(response.text)
    lol = "Bearer "
    token = lol+dict['access_token']
    print('returning token \n',token )
    session['token']=token
    print('session token \n',session['token'] )
    return 

@app.route("/")
def index():
    import requests
    import json
    

    #generateToken()
   ####   GETTING USER DATA ####
    
    if(not checkKey(session['token'])):
        token = generateToken()
        print('token generated after checking')


    ####   GETTING PLAYLIST DETAILS  ####
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=15"

    payload={}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': session['token'],
    'Cookie': 'sp_t=c619b1d8cf10a0d45638c388bbf6ce3b; sp_landing=https%3A%2F%2Fopen.spotify.com%2Fartist%2F3z97WMRi731dCvKklIf2X6'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.json()
  
    print('json data sent')
    print('token \n\n\n\n',session['token'],'\n\n\n\n\n')
    #print(res)

    
    #### GETTING TOP ARTISTS 
    return render_template("index.html", res=res) 


@app.route("/hello")
def hello():
    return render_template("hello.html")
