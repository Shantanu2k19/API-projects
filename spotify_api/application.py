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
    #'Bearer BQDEzpDsPytZbnE-2MCMrKc1BStSOeQZyGUqp6-yWv09bvjGBc4K-a8uDLbil3xWqnmdlZi1o0G_7TqmtY8YnsoYwfOxM5ZMlV2kYnb3thDsaK8LWHczFeP9HVk3vkNyVfCt97-znMjOI60yRjMPrf0GRdXbWLLIOcnF6h-1WQ'
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

































"""
2acf124438b74408942da3a116267af6:5c3736bc6d65478080ada9b367eb3233

MmFjZjEyNDQzOGI3NDQwODk0MmRhM2ExMTYyNjdhZjY6NWMzNzM2YmM2ZDY1NDc4MDgwYWRhOWIzNjdlYjMyMzM=

https://accounts.spotify.com/authorize


https://accounts.spotify.com/authorize?client_id=2acf124438b74408942da3a116267af6&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fhello&scope=user-read-recently-played


%20user-read-email&state=34fFs29kd09

http://127.0.0.1:5000/hello?code=AQDP0vbaj2WrpLPz-qo3LB06u_DW7uFraGLZUUqkKjxlSToh362ejl_rxCwtwqUFMd4mql-9Id81GXbY8P9lYACKRwy71qY4H4e2gYSt1Qi3QMYh_HI_6q_FmBvXCQqtJmk_yd1Wweaeu-01-WlXbpLmHNDfHBdwDddotcuFkVKxo7MO9Uz0rMLx_bsX7wuwawfyOTtpmCvWUg

curl -H "Authorization: Basic MmFjZjEyNDQzOGI3NDQwODk0MmRhM2ExMTYyNjdhZjY6NWMzNzM2YmM2ZDY1NDc4MDgwYWRhOWIzNjdlYjMyMzM=" -d grant_type=authorization_code -d code=AQDP0vbaj2WrpLPz-qo3LB06u_DW7uFraGLZUUqkKjxlSToh362ejl_rxCwtwqUFMd4mql-9Id81GXbY8P9lYACKRwy71qY4H4e2gYSt1Qi3QMYh_HI_6q_FmBvXCQqtJmk_yd1Wweaeu-01-WlXbpLmHNDfHBdwDddotcuFkVKxo7MO9Uz0rMLx_bsX7wuwawfyOTtpmCvWUg -d redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fhello https://accounts.spotify.com/api/token



https://accounts.spotify.com/en/authorize?client_id=2acf124438b74408942da3a116267af6&response_type=code&redirect_uri=https:%2F%2Fwww.youtube.com%2F&scope=user-read-recently-played%20user-read-email&state=34fFs29kd09





http://127.0.0.1:5000/hello?code=AQDP0vbaj2WrpLPz-qo3LB06u_DW7uFraGLZUUqkKjxlSToh362ejl_rxCwtwqUFMd4mql-9Id81GXbY8P9lYACKRwy71qY4H4e2gYSt1Qi3QMYh_HI_6q_FmBvXCQqtJmk_yd1Wweaeu-01-WlXbpLmHNDfHBdwDddotcuFkVKxo7MO9Uz0rMLx_bsX7wuwawfyOTtpmCvWUg


	<p>Shantanu is listening to</p>

	{{ (res["items"][0]['track']['album']['name']) }}
<br>
	{{res["cursors"]['after']}}




curl -H "Authorization: Basic MmFjZjEyNDQzOGI3NDQwODk0MmRhM2ExMTYyNjdhZjY6NWMzNzM2YmM2ZDY1NDc4MDgwYWRhOWIzNjdlYjMyMzM=" -d grant_type=refresh_token -d refresh_token=AQB_ajqK3XpUDsKCtVZJLZJ76TfZWBMFGsOmylVciTMIHWGKa_aQjkYd2Naa4Yvj8VQsinW8TZWnN-9CCEr563nqatbjs6hD9PMBKzArWSar1xj7g7wkglVMRJrOTRVrn3U https://accounts.spotify.com/api/token




{
    "access_token": "BQCkWBWzC9f-BAJgcHqnqXTlAY2xzdhrYoyqaQSUgKSNQzx9EwYiWUYnWHeVjTIzgCAg2niKMFb4tKCDJQqscj0dYaaQFV2iht3NY777Pc0XCpSkQ-4KVP-fp0WK5CSVpwOkek8ycvKRDCcj_wSAM4slyu3mrSbXBVITOJU",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "AQB_ajqK3XpUDsKCtVZJLZJ76TfZWBMFGsOmylVciTMIHWGKa_aQjkYd2Naa4Yvj8VQsinW8TZWnN-9CCEr563nqatbjs6hD9PMBKzArWSar1xj7g7wkglVMRJrOTRVrn3U",
    "scope": "user-read-recently-played"
}
"""