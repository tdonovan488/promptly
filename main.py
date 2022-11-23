import requests,json,time
from threading import Thread
from datetime import datetime,timedelta

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "8lpCnBnuSIksGaBkVIQr78zQgLkchvOT"
AUTHORIZATION = f'bearer {API_KEY}'

with open("prompts.txt","r") as f:
    prompts = json.loads(f.read())

date = datetime.now()
date_string = date.strftime("%d-%m-%Y")
tomorrow_string = (date+timedelta(days=1)).strftime("%d-%m-%Y")
todays_prompt_data = prompts[date_string]
tomorrows_prompt_data = prompts[tomorrow_string]

class generateImage():
    def __init__(self,prompt,style):
        self.prompt = prompt
        self.style = style
        self.taskId = ""
        self.state = ""
        self.result = ""
        self.filelocation = ""
        self.successful = False
        self.headers = {
            "Authorization": AUTHORIZATION,
            "Content-Type": "application/json"
        }

        print("\n\n\n--------Getting Image--------")
        print("Creating Task")
        self.createTask()
        print("Inputting Prompt")
        self.inputPrompt()
        while self.state != "completed":
            self.checkResult()
            time.sleep(3)
            if(self.state == "failed") or self.state == "input":
                return
        self.saveImage()
        self.successful = True

    def createTask(self):
        print(self.headers)
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
        print(put_payload)
        r = requests.request("PUT", f"https://api.luan.tools/api/tasks/{self.taskId}", headers=self.headers, data=json.dumps(put_payload))
        j = json.loads(r.text)
        print(r.text)
        if j.get("state"):
            self.state = j.get("state")


    def checkResult(self):
        r = requests.get(f"https://api.luan.tools/api/tasks/{self.taskId}",headers=self.headers)
        j = json.loads(r.text)
        self.state = j.get("state")
        if j.get("state") == "completed":
            self.result = j.get("result")
        print(r.text)

    def saveImage(self):
        filename = self.prompt.replace(" ","-")
        r = requests.get(self.result)
        with open(f"images/{filename}-{self.style}.jpg","wb") as f:
            f.write(r.content)
        self.filelocation = f"images/{filename}-{self.style}.jpg"

def main_loop():
    print("Loop Started")
    date = datetime.now()
    date_string = date.strftime("%d-%m-%Y")
    tomorrow_string = (date+timedelta(days=1)).strftime("%d-%m-%Y")

    global todays_prompt_data
    global tomorrows_prompt_data
    todays_prompt_data = prompts[date_string]
    tomorrows_prompt_data = prompts[tomorrow_string]

    prompt = todays_prompt_data["prompt"]
    styles = todays_prompt_data["styles"]
    for i in range(len(todays_prompt_data["links"]),3):
        imageGenerator = generateImage(prompt=prompt,style=styles[i])
        if imageGenerator.successful:
            todays_prompt_data["links"].append({"link":imageGenerator.result,"filelocation":imageGenerator.filelocation})
        time.sleep(1)
    prompts[date_string] = todays_prompt_data

    prompt = tomorrows_prompt_data["prompt"]
    styles = tomorrows_prompt_data["styles"]
    for i in range(len(tomorrows_prompt_data["links"]),3):
        imageGenerator = generateImage(prompt=prompt,style=styles[i])
        if imageGenerator.successful:
            tomorrows_prompt_data["links"].append({"link":imageGenerator.result,"filelocation":imageGenerator.filelocation})
        time.sleep(1)
    prompts[tomorrow_string] = tomorrows_prompt_data

    with open("prompts.txt","w") as f:
        f.write(json.dumps(prompts,indent=4))

    time.sleep(60)

def savePromptData():
    with open("prompts.txt","w") as f:
        f.write(json.dumps(prompts,indent=4))



@app.route("/api/todaysPrompt")
def getTodaysPrompt():
    return json.dumps(todays_prompt_data,indent=4)


# loop = Thread(target=lambda: main_loop(),args=())
# loop.start()
app.run()

def test():
    date = datetime.now()
    date_string = date.strftime("%d-%m-%Y")
    tomorrow_string = (date+timedelta(days=1)).strftime("%d-%m-%Y")
    global todays_prompt_data
    global tomorrows_prompt_data
    todays_prompt_data = prompts[date_string]
    tomorrows_prompt_data = prompts[tomorrow_string]
    prompt = todays_prompt_data["prompt"]
    styles = todays_prompt_data["styles"]
    for i in range(len(todays_prompt_data["links"]),3):
        imageGenerator = generateImage(prompt=prompt,style=styles[i])
        if imageGenerator.successful:
            todays_prompt_data["links"].append({"link":imageGenerator.result,"filelocation":imageGenerator.filelocation})
            savePromptData()
        time.sleep(1)
    prompts[date_string] = todays_prompt_data
    prompt = tomorrows_prompt_data["prompt"]
    styles = tomorrows_prompt_data["styles"]
    for i in range(len(tomorrows_prompt_data["links"]),3):
        imageGenerator = generateImage(prompt=prompt,style=styles[i])
        if imageGenerator.successful:
            tomorrows_prompt_data["links"].append({"link":imageGenerator.result,"filelocation":imageGenerator.filelocation})
            savePromptData()
        time.sleep(1)
        
    prompts[tomorrow_string] = tomorrows_prompt_data