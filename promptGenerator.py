from datetime import datetime,timedelta
import random,json, requests

daysToGenerate = 1095

API_KEY = "8lpCnBnuSIksGaBkVIQr78zQgLkchvOT"
AUTHORIZATION = f'bearer {API_KEY}'
headers = {
            "Authorization": AUTHORIZATION,
            "Content-Type": "application/json"
}
styleDecoder = {}
styles = []
r = requests.get("https://api.luan.tools/api/styles/",headers=headers)
j = json.loads(r.text)

for i in j:
    styles.append(i["name"])
    styleDecoder[i["name"]] = i["id"]

prompts = {}

nouns = []
with open("nouns.txt","r") as f:
    for i in f.readlines():
        if len(i) < 7:
            nouns.append(i.rstrip())

adjectives = []
with open("adjectives.txt","r") as f:
    for i in f.readlines():
        if len(i) < 7:
           adjectives.append(i.rstrip())

for i in range(daysToGenerate):
    date = datetime.now() + timedelta(days=i)
    date_string = date.strftime("%d-%m-%Y")

    prompt = random.choice(adjectives) + " " + random.choice(nouns)

    styleNames = []
    styleCodes = []
    for i in range(3):
        styleName = random.choice(styles)
        while styleName in styleNames:
            styleName = random.choice(styles)
        styleNames.append(styleName)
        styleCodes.append(styleDecoder[styleName])

    hints = [*prompt]
    random.shuffle(hints)
    hints.pop(hints.index(" "))
    hints = list(set(hints))
    print(i,date_string,prompt,styleNames,styleCodes)
    prompts[date_string] = {"prompt":prompt,"styles":styleCodes,"styleNames":styleNames,"hints":hints,"links":[]}

with open("prompts.txt","w") as f:
    f.write(json.dumps(prompts,indent=4))
