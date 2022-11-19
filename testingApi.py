from flask import Flask
import requests,json,time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

prompt_data = {
        "prompt": "grand cycle",
        "styles": [11],
        "styleNames": ["Mystical"],
        "hints": [
            "n",
            "c",
            "y",
            "l",
            "a",
            "e",
            "d",
            "g",
            "r"
        ],
        "links": ["images/hard-space11.jpg","images/hard-space63.jpg","images/hard-space49.jpg"]
    }

@app.route("/api/todaysPrompt")
def getTodaysPrompt():
    return json.dumps(prompt_data,indent=4)


app.run()