import requests,json,time
from threading import Thread
from datetime import datetime,timedelta

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "8lpCnBnuSIksGaBkVIQr78zQgLkchvOT"

with open("prompts.txt","r") as f:
    prompts = json.loads(f.read())

todays_prompt_data = {}

class generateImage(object):
    def __init__(self,prompt,styles):
        self.prompt = prompt
        self.style = styles
        self.idToken = f'bearer {API_KEY}'
        self.taskId = ""
        self.state = ""
        self.results = []
        self.headers = {
            "Authorization": self.idToken,
            "Content-Type": "application/json"
        }

        for style in styles:
            self.style = style
            self.state = ""
            print("Creating Task")
            self.createTask()
            print("Inputting Prompt")
            self.inputPrompt()
            while self.state != "completed" and self.state != "failed":
                print("Checking Results")
                self.checkResult()
                time.sleep(3)
            if(self.state == "failed"):
                self.results = []
                break
        if(self.state != "failed"):
            self.saveImages()

    def createTask(self):
        r = requests.post("https://api.luan.tools/api/tasks/",headers=self.headers,json={"use_target_image": False})
        print(r.text)
        j = json.loads(r.text)
        self.taskId = j.get("id")
        self.state = j.get("state")

    def inputPrompt(self):
        put_payload ={            
            "input_spec": {                    
            "style": self.style,                    
            "prompt": self.prompt,
            "width":500,
            "height":500
        }}
        r = requests.request("PUT", f"https://api.luan.tools/api/tasks/{self.taskId}", headers=self.headers, data=json.dumps(put_payload))
        j = json.loads(r.text)
        print(r.text)
        self.state = j.get("state")


    def checkResult(self):
        r = requests.get(f"https://api.luan.tools/api/tasks/{self.taskId}",headers=self.headers)
        j = json.loads(r.text)
        self.state = j.get("state")
        self.results.append(j.get("result"))
        print(r.text)

    def saveImages(self):
        filename = self.prompt.replace(" ","-")
        for i in self.results:
            r = requests.get("i")
            with open(f"images/{filename}.jpg","wb") as f:
                f.write(r.content)

def main_loop():
    print("Loop Started")
    date = datetime.now()
    date_string = date.strftime("%d-%m-%Y")
    tomorrow_string = (date+timedelta(days=1)).strftime("%d-%m-%Y")

    global todays_prompt_data
    todays_prompt_data = prompts[date_string]

    prompt = todays_prompt_data["prompt"]
    styles = todays_prompt_data["styles"]

    if(len(todays_prompt_data["links"]) == 0):
        imageGenerator = generateImage(prompt=prompt,styles=styles)
        todays_prompt_data["links"] = imageGenerator.result
        print(todays_prompt_data)
        prompts[date_string] = todays_prompt_data
        time.sleep(30)

    # if(len(prompts[tomorrow_string]["links"]) == 0):
    #     imageGenerator = generateImage(prompt=prompts[tomorrow_string]["prompt"],styles=prompts[tomorrow_string]["styles"])
    #     prompts[tomorrow_string]["links"] = imageGenerator.result
    #     time.sleep(30)

    with open("prompts.txt","w") as f:
        f.write(json.dumps(prompts,indent=4))

    time.sleep(60)

# loop = Thread(target=lambda: main_loop(),args=())
# loop.start()

@app.route("/api/todaysPrompt")
def getTodaysPrompt():
    return json.dumps(todays_prompt_data,indent=4)

# app.run()

date = datetime.now()
date_string = date.strftime("%d-%m-%Y")
todays_prompt_data = prompts[date_string]
prompt = todays_prompt_data["prompt"]
styles = todays_prompt_data["styles"]
if(len(todays_prompt_data["links"]) == 0):
    imageGenerator = generateImage(prompt=prompt,styles=styles)
    todays_prompt_data["links"] = imageGenerator.result
    print(todays_prompt_data)
    prompts[date_string] = todays_prompt_data

with open("prompts.txt","w") as f:
    f.write(json.dumps(prompts,indent=4))