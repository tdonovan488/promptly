from datetime import datetime,timedelta
import random,json

daysToGenerate = 1095

styles = ["Spectral","Bad Trip","Cartoonist","HDR","Realistic","Meme","Isometric","Retro-Futurism","Analogue","Paint","Polygon","Gouache","Comic","Line-Art","Malevolent","Surreal","Throwback","Street Art","No Style","Ghibli","Melancholic","Pandora","Daydream","Provenance","Arcane","Toasty","Transitory","Psychic","Rose Gold","Wuhtercuhler","Etching","Mystical","Dark Fantasy","HD","Vibrant","Fantasy Art","Steampunk","Psychedelic","Ukiyoe","Synthwave"]

styleDecoder = {
    "Spectral": 63,
    "Bad Trip": 57,
    "Cartoonist": 58,
    "HDR": 52,
    "Realistic": 32,
    "Meme": 44,
    "Isometric": 55,
    "Retro-Futurism": 54,
    "Analogue": 53,
    "Paint": 50,
    "Polygon": 49,
    "Gouache": 48,
    "Comic": 45,
    "Line-Art": 47,
    "Malevolent": 40,
    "Surreal": 37,
    "Throwback": 35,
    "Street Art": 41,
    "No Style": 3,
    "Ghibli": 22,
    "Melancholic": 28,
    "Pandora": 39,
    "Daydream": 36,
    "Provenance": 17,
    "Arcane": 34,
    "Toasty": 31,
    "Transitory": 29,
    "Psychic": 9,
    "Rose Gold": 18,
    "Wuhtercuhler": 16,
    "Etching": 14,
    "Mystical": 11,
    "Dark Fantasy": 10,
    "HD": 7,
    "Vibrant": 6,
    "Fantasy Art": 5,
    "Steampunk": 4,
    "Psychedelic": 21,
    "Ukiyoe": 2,
    "Synthwave": 1
}

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

    styleName = random.choice(styles)
    style = styleDecoder[styleName]

    hints = [*prompt]
    random.shuffle(hints)
    hints.pop(hints.index(" "))
    hints = list(set(hints))
    print(i,date_string,prompt,style,styleName)
    prompts[date_string] = {"prompt":prompt,"style":style,"styleName":styleName,"hints":hints,"link":""}

with open("prompts.txt","w") as f:
    f.write(json.dumps(prompts,indent=4))
