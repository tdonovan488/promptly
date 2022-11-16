from flask import Flask
import requests,json,time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

prompt_data = {
        "prompt": "left field",
        "style": 63,
        "styleName": "Spectral",
        "hints": [
            "d",
            "t",
            "l",
            "e",
            "f",
            "i"
        ],
        "link": "https://luan-wombo-paint.s3.amazonaws.com/generated/930dc429-4765-4d91-83be-2d8ec193e9f5/final.jpg?AWSAccessKeyId=AKIAWGXQXQ6WCOB7PP5J&Signature=B%2BP1rCZdCX%2BK34XH09uhlUlW%2BfY%3D&Expires=1668570164"
    }

@app.route("/api/todaysPrompt")
def getTodaysPrompt():
    return json.dumps(prompt_data,indent=4)


app.run()