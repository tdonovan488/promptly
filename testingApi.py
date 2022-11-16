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
        "link": "https://images.wombo.art/exports/4f26613b-7704-4a98-8ec4-83f9dc472e33/blank_tradingcard.jpg?Expires=1675744959&Signature=ryUCtdx2UZ3uBD0fS~lb3HLurRDDC7OS1bv0Ac8ztLEe5JWwj6bJ9Yzvz6aQFwiQzuAPpSC3IPg~o~CfV-XzSYOy0cJS0cdOcq09ejnNs5BTmtB6PPn4PScvHv4CQxo1MC21ZFYfULkutXcYn8c4JXZLAuhA7iLzvUsCNeHCRSMmSHS59qHwxI~2s8iVonslDbskHYEJeeTOlK-ZA4GAl5pydaj0zG-KSCrArg3WGqFV2pwfN~2wFZhtqSnf6kSC5tCPOqLJboGlQtoqbP-6J9Bzd1iwUJrdkNcVtcIkeyMGSzFKvIAlfi~d0M~D0jrEoB4MS9nQsGH6lOsWT~9R0g__&Key-Pair-Id=K1ZXCNMC55M2IL"
    }

@app.route("/api/todaysPrompt")
def getTodaysPrompt():
    return json.dumps(prompt_data,indent=4)


app.run()