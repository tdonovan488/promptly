from datetime import datetime,timedelta
import random,json

daysToGenerate = 1095

styles = [63,33,57,58]

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
    style = random.choice(styles)

    hints = [*prompt]
    random.shuffle(hints)
    hints.pop(hints.index(" "))
    hints = list(set(hints))
    print(i,date_string,prompt,style,hints)
    prompts[date_string] = {"prompt":prompt,"style":style,"hints":hints,"link":""}

with open("prompts.txt","w") as f:
    f.write(json.dumps(prompts,indent=4))
