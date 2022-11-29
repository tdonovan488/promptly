var prompt = "dutiful evening"
var hints = []
var images = []

var guessedWord = false
var n = 0
var compare_string = ""
var guess = []
var guessIndex = 0
var imageIndex = 0
var selectedSpace = 0
var guessCount = 5
var hintIndex = 0
var correctLetters = {"Positions":[]}
var shownHints = {"Positions":[]}
var promptContainer = document.querySelector("body > div.grid-aligner > div")
var letterBoxes = []

var exitButtons = document.getElementsByClassName("exit-button")
var overlayContainer = document.querySelector("body > div.menus.menu-hidden")
var howToPopup = document.querySelector("body > div.menus.menu-hidden > div.how-to-play.popup.menu-hidden")
var settingsPopup = document.querySelector("body > div.menus.menu-hidden > div.settings.popup.menu-hidden")
var creditsPopup = document.querySelector("body > div.menus.menu-hidden > div.credits.popup.menu-hidden")

var keyboard = [["qwertyuiop"],["asdfghjkl"],["zxcvbnm"]]
var keyElements = []
var keyboardElement = document.querySelector("body > div.keyboard-container")

var key = document.createElement("button")
key.className = "keyboard-control-key"
key.value = "enter"
key.innerText = "Enter"
keyboardElement.children[2].appendChild(key)
keyElements.push(key)
for(var i = 0;i < keyboard.length;i++){
    for(var x = 0;x<keyboard[i][0].length;x++){
        var key = document.createElement("button")
        key.className = "keyboard-key"
        key.value = keyboard[i][0][x]
        key.innerText = keyboard[i][0][x].toUpperCase()
        keyboardElement.children[i].appendChild(key)
        keyElements.push(key)
    }
}
key = document.createElement("button")
key.className = "keyboard-control-key"
key.value = "back"
key.innerText = "Delete"
keyboardElement.children[2].appendChild(key)
keyElements.push(key)

keyElements.forEach(element => {
    element.addEventListener("click",function(){keyPress(element.value)})
});

function keyPress(key){
    if(key === "back"){
        guessIndex = findDeleteIndex()
        guess = guess.slice(0,guessIndex)
    } else if (key == "enter"){
        if(guess.length != n + 1 || guess.includes(undefined)) return;
        checkGuess()
    }else{
        guessIndex = findOpenIndex()
        guess[guessIndex] = key
    }
    selectedSpace = findOpenIndex()
    guess = guess.slice(0,n+1)
    for(var i = 0;i < correctLetters.Positions.length;i++){
        guess[correctLetters.Positions[i]] = compare_string[correctLetters.Positions[i]]
    }
    for(var i = 0;i < shownHints.Positions.length;i++){
        guess[shownHints.Positions[i]] = compare_string[shownHints.Positions[i]]
    }

    updateBoard();
}

getPrompt().then((data) => {
    console.log(data)
    prompt = data.prompt
    images = data.links
    hints = data.hints
    n = prompt.replace(" ","").length -1
    compare_string = prompt.replace(" ","")
    var child = 0;
    for(var i = 0;i < prompt.length;i++){
        if (prompt[i] == " "){
            child = 1;
            continue
        }
        var newLetter = document.createElement("div")
        newLetter.className = "letter-box"
        promptContainer.children[child].appendChild(newLetter)
        letterBoxes.push(newLetter)
    }
    document.querySelector("body > div.image-container > img").src = images[0].filelocation
})

async function getPrompt(){
    var url = "http://127.0.0.1:5000/api/todaysPrompt"
    const response = await fetch(url,{method:"GET",headers: {'Content-Type': 'application/json'},})
    return response.json()
}

function closePopup(){
    howToPopup.className = "how-to-play popup menu-hidden"
    settingsPopup.className = "settings popup menu-hidden"
    creditsPopup.className = "credits popup menu-hidden"
    overlayContainer.className = "menus menu-hidden"
}
for(var i = 0;i < exitButtons.length;i++){
    exitButtons[i].addEventListener("click",closePopup)
}

document.querySelector("body > div.image-container > button:nth-child(1)").addEventListener("click",function(){
    if(imageIndex > 0){
        imageIndex--
    } else {
        imageIndex = 2
    }
    document.querySelector("body > div.image-text").innerText = (imageIndex + 1) + "/3"
    document.querySelector("body > div.image-container > img").src = images[imageIndex].filelocation
})
document.querySelector("body > div.image-container > button:nth-child(3)").addEventListener("click",function(){
    if(imageIndex < 2){
        imageIndex++
    } else{
        imageIndex = 0
    }
    document.querySelector("body > div.image-text").innerText = (imageIndex + 1) + "/3"
    document.querySelector("body > div.image-container > img").src = images[imageIndex].filelocation
})

document.querySelector("body > header > div.dropdown-container > div > div > button:nth-child(1)").addEventListener("click",function(){
    closePopup()
    howToPopup.className = "how-to-play popup"
    overlayContainer.className = "menus"
})


document.querySelector("body > header > div.dropdown-container > div > div > button:nth-child(2)").addEventListener("click",function(){
    closePopup()
    settingsPopup.className = "settings popup"
    overlayContainer.className = "menus"
})


document.querySelector("body > header > div.dropdown-container > div > div > button:nth-child(3)").addEventListener("click",function(){
    closePopup()
    creditsPopup.className = "credits popup"
    overlayContainer.className = "menus"
})


document.addEventListener("keydown",function(e){
    if(e.key === "Backspace" || e.key === "Delete"){
        guessIndex = findDeleteIndex()
        guess = guess.slice(0,guessIndex)
    } else if (e.key == "Enter"){
        if(guess.length != n + 1 || guess.includes(undefined)) return;
        checkGuess()
    }else if(((e.keyCode >= 97 && e.keyCode <= 122) || (e.keyCode >= 65 && e.keyCode <= 90))){
        guessIndex = findOpenIndex()
        guess[guessIndex] = e.key
    }
    selectedSpace = findOpenIndex()
    guess = guess.slice(0,n+1)
    for(var i = 0;i < correctLetters.Positions.length;i++){
        guess[correctLetters.Positions[i]] = compare_string[correctLetters.Positions[i]]
    }
    for(var i = 0;i < shownHints.Positions.length;i++){
        guess[shownHints.Positions[i]] = compare_string[shownHints.Positions[i]]
    }

    updateBoard();
})

function updateBoard(){
    for(var i = 0;i < letterBoxes.length;i++){
        if(correctLetters[i]){
            letterBoxes[i].className = "letter-box correct"
        } else if(shownHints[i]){
            letterBoxes[i].className = "letter-box hint"
        }else if(selectedSpace == i){
            letterBoxes[i].className = "letter-box selected"
        }else{
            letterBoxes[i].className = "letter-box"
        }
        if (guess[i]) {
            letterBoxes[i].innerText = guess[i]
        } else{
            letterBoxes[i].innerText = ""
        }
    }
}

function indexes(source, find) {
    var result = []
    for(var i = 0;i < source.length;i++){
        var new_index = source.indexOf(find,i)
        if (!result.includes(new_index) && new_index != -1) result.push(new_index)
    }
    return result;
  }

function giveHint(){
    var currentlyShown = hintIndex
    var totalHints = hints.length

    for(var x = currentlyShown;x<totalHints;x++){
        hintIndex++
        var indices = indexes(compare_string,hints[x])
        var hintNeeded = false;
        for(var i = 0;i<indices.length;i++){
            if(!correctLetters[indices[i]]){
                hintNeeded = true
                break
            }
        }
        if(hintNeeded){
            for(var i = 0;i< indices.length;i++){
                shownHints[indices[i]] = hints[x]
                shownHints.Positions.push(indices[i])
            }
        }
        if (hintNeeded) break
    }

}

function findOpenIndex(){
    for(var i = 0;i<n + 1;i++){
        if((!correctLetters[i] && !shownHints[i] && !guess[i])){
            return i
        }
    }
    return n + 1
}
function findDeleteIndex(){
    for(var i = n;i>0;i--){
        if((!correctLetters[i] && !shownHints[i] && guess[i])){
            return i
        }
    }
    return 0
}

function checkGuess(){
    guessCount--
    if(compare_string == guess.join("")){
        guessedWord = true
    }

    var words = prompt.split(" ")
    var correct_indexes = []
    for(var i = 0;i < compare_string.length;i++){
        if(guess[i] == compare_string[i]) correct_indexes.push(i)
    }

    console.log(correct_indexes)
    for(var i = 0; i < words.length;i++){
        var correctInWord = {"Positions":[]}
        for(var x = 0;x<words[i].length;x++){
            if(correct_indexes.includes(i * words[0].length + x)) {
                correctInWord[i * words[0].length + x] = words[i][x]
                correctInWord.Positions.push(i * words[0].length + x)
            }
        }

        if(correctInWord.Positions.length == words[i].length){
            correctLetters.Positions = correctLetters.Positions.concat(correctInWord.Positions)
            for(var y = 0;y < correctInWord.Positions.length;y++){
                correctLetters[correctInWord.Positions[y]] = correctInWord[correctInWord.Positions[y]]
            }
        }
    }
    if(!guessedWord){
        giveHint()
        guess = []
        i = findOpenIndex()
        guessIndex = i
        selectedSpace = i
    }
}