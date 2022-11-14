import requests,json,time
from threading import Thread
from datetime import datetime,timedelta

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


with open("prompts.txt","r") as f:
    prompts = json.loads(f.read())

todays_prompt_data = {}

class generateImage(object):
    def __init__(self,prompt,style):
        self.prompt = prompt
        self.style = style
        self.idToken = ""
        self.taskId = ""
        self.state = ""
        self.result = ""

        print("Getting Token")
        self.getToken()
        print("Creating Task")
        self.createTask()
        print("Inputting Prompt")
        self.inputPrompt()
        while self.state != "completed":
            self.checkResult()
            time.sleep(1)
        print("Got Result:")
        print(self.result.get("final"))
    def getToken(self):
        r = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw",json={"returnSecureToken":True})
        j = json.loads(r.text)
        self.idToken = "bearer " + j.get("idToken")

        # EXAMPLE RESPONSE
        # {
        # "kind": "identitytoolkit#SignupNewUserResponse",
        # "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ3YjE5MTI0MGZjZmYzMDdkYzQ3NTg1OWEyYmUzNzgzZGMxYWY4OWYiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9wYWludC1wcm9kIiwiYXVkIjoicGFpbnQtcHJvZCIsImF1dGhfdGltZSI6MTY2ODM3Njk2MywidXNlcl9pZCI6InAzYVQ2TTlydklPYUJYdFc1MDA3R0hmamtqcjIiLCJzdWIiOiJwM2FUNk05cnZJT2FCWHRXNTAwN0dIZmpranIyIiwiaWF0IjoxNjY4Mzc2OTYzLCJleHAiOjE2NjgzODA1NjMsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiYW5vbnltb3VzIn19.OcdP15XFryy-B9JgZqG0FrBkf8pCT_k1yEO5SucAkn1Oiism27H48YX-hOvuL4CSJPyO5BaD7AZmknZsWCMKjbiuGGxmO_qoIwyRQ4qzAyMxGb9ERolz7eVnjQ3RYzy7BH9Dt93AsekQyjJPQBNyRvzeMLFp6qUDVilrSHeUsvH-nP96ZgUYeXvH6jkCdno38UrXk-JoxCpX6IJYF__tGs7ZVFj1QqkEQuT04Jm-AkmNIE94DxJnSilCaNBsttE2JI5ldyW665xESt0cWmrbcOvgYkPJPjfNh6M_rx4Sy4_NXCZ5qsIMsDvlf_sVLLm1UIB2PngpTaHZ7hmqfssDAQ",
        # "refreshToken": "AOkPPWR-vBWlsbRFjjjMAjWp8NNzy9ull_fZQjgSR6-oFsWx9rGAhGL9jn99riGjPGOM1tGFRKh6dmkE4Oczqmg_eU0Uzy9p9cvX-v7LzSYXUa12uJmcWJpEpkRYuC71GKH_OsqJcdLOkDOm9Zj7Z_HChX8eOAtH8xBYvy_Sftfg5X1x3X7yfUw",
        # "expiresIn": "3600",
        # "localId": "p3aT6M9rvIOaBXtW5007GHfjkjr2"
        # }

    def createTask(self):
        headers = {
            "authorization": self.idToken,
        }
        r = requests.post("https://paint.api.wombo.ai/api/tasks",headers=headers,json={"premium":False})
        j = json.loads(r.text)
        self.taskId = j.get("id")
        self.state = j.get("state")
        
        # EXAMPLE RESPONSE
        # {
        # "id": "59f2f96a-81ab-4129-8fc5-f4793956a9d9",
        # "user_id": "bEnVHQLf2tbZVhv7OuNUXmWvmaG3",
        # "input_spec": null,
        # "state": "input",
        # "premium": false,
        # "created_at": "2022-11-13T21:55:06.036526+00:00",
        # "updated_at": "2022-11-13T21:55:06.036526+00:00",
        # "generation_error_code": null,
        # "photo_url_list": [],
        # "generated_photo_keys": [],
        # "result": null
        # }


    def inputPrompt(self):
        headers = {
            "authorization": self.idToken,
        }
        payload = {
            "input_spec": {
                "prompt":self.prompt,
                "style":self.style,
                "display_freq":10
            }
        }
        r = requests.put(f"https://paint.api.wombo.ai/api/tasks/{self.taskId}",headers=headers,json=payload)
        j = json.loads(r.text)
        self.state = j.get("state")
        print(r.text,r.status_code)

    def checkResult(self):
        headers = {
            "authorization": self.idToken,
        }
        r = requests.get(f"https://paint.api.wombo.ai/api/tasks/{self.taskId}",headers=headers)
        j = json.loads(r.text)
        self.state = j.get("state")
        self.result = j.get("result")

def main_loop():
    print("Loop Started")
    date = datetime.now()
    date_string = date.strftime("%d-%m-%Y")
    tomorrow_string = (date+timedelta(days=1)).strftime("%d-%m-%Y")

    global todays_prompt_data
    todays_prompt_data = prompts[date_string]

    prompt = todays_prompt_data["prompt"]
    style = todays_prompt_data["style"]

    if(todays_prompt_data["link"] == ""):
        imageGenerator = generateImage(prompt=prompt,style=style)
        todays_prompt_data["link"] = imageGenerator.result["final"]
    #if(prompts[tomorrow_string]["link"] == ""):
    #    imageGenerator = generateImage(prompt=prompts[tomorrow_string]["prompt"],style=prompts[tomorrow_string]["style"])


    time.sleep(60)

loop = Thread(target=lambda: main_loop(),args=())

loop.start()

@app.route("/api/todaysPrompt")
def getTodaysPrompt():
    return json.dumps(todays_prompt_data,indent=4)

app.run()