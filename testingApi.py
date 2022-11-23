from flask import Flask
import requests,json,time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

prompt_data = {
        "prompt": "stark back",
        "styles": [
            7,
            63,
            41
        ],
        "styleNames": [
            "HD",
            "Spectral",
            "Street Art"
        ],
        "hints": [
            "k",
            "t",
            "b",
            "c",
            "a",
            "s",
            "r"
        ],
        "links": [
            {
                "link": "https://luan-wombo-paint.s3.amazonaws.com/generated/9169118b-17ff-401a-9d34-e969213d5424/final.jpg?AWSAccessKeyId=AKIAWGXQXQ6WCOB7PP5J&Signature=XH98kXDpSVaqtgh0bZRCP2AfJfI%3D&Expires=1669222857",
                "filelocation": "images/stark-back-7.jpg"
            },
            {
                "link": "https://luan-wombo-paint.s3.amazonaws.com/generated/9169118b-17ff-401a-9d34-e969213d5424/final.jpg?AWSAccessKeyId=AKIAWGXQXQ6WCOB7PP5J&Signature=XH98kXDpSVaqtgh0bZRCP2AfJfI%3D&Expires=1669222857",
                "filelocation": "images/hard-space11.jpg"
            },
            {
                "link": "https://luan-wombo-paint.s3.amazonaws.com/generated/9169118b-17ff-401a-9d34-e969213d5424/final.jpg?AWSAccessKeyId=AKIAWGXQXQ6WCOB7PP5J&Signature=XH98kXDpSVaqtgh0bZRCP2AfJfI%3D&Expires=1669222857",
                "filelocation": "images/hard-space49.jpg"
            }
        ]
    }

@app.route("/api/todaysPrompt")
def getTodaysPrompt():
    return json.dumps(prompt_data,indent=4)


app.run()