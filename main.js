var prompt = "dutiful evening"
var hints = [
    "n",
    "e",
    "l",
    "d",
    "g"
]
var image = "https://images.wombo.art/generated/d3e2ee2d-0b70-4a31-83a9-ec46312784af/final.jpg?Expires=1675584232&Signature=VDAmXJdLyVrrt1qCx8BiDv9Ec7LsKikSAKnEWn3yy8tf4nwSvBPVApZyK851FBq6~RZlY6iDW~nMN-Uyn9MSeuXbDESaccizCa7kO-oEn9LsrF9gb94jJsJd2VKoh0Y1VI1PgRDUMulU-UYi2mTT~M1P3NkRvhOES3gJtmLupcEwHJgtXlarN9b9cPSzK8gnuQBFvHifmz8nGHs92f83~b7Hs34WqyyVsBtNJwOp~7A5VBO6ftvCIM4K~W0O5ReSToOw-jap3QYR9O0dr0w0i16nEBjt2E1~H2iZ1DNSejJS6m-I6D1p5dRqWyFGRRQEqgSwc~cpNxiLrhRhqqncLQ__&Key-Pair-Id=K1ZXCNMC55M2IL"

var guessedWord = false
var n = 0
var compare_string = ""
var guess = []
var guessIndex = 0
var selectedSpace = 0
var guessCount = 5
var hintIndex = 0
var correctLetters = {"Positions":[]}
var shownHints = {"Positions":[]}
var promptContainer = document.querySelector("body > div.grid-aligner > div")
var letterBoxes = []

getPrompt().then((data) => {
    console.log(data)
    prompt = data.prompt
    image = data.link
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
    document.querySelector("body > div.image-container > img").src = image
})

async function getPrompt(){
    
    var url = "http://127.0.0.1:5000/api/todaysPrompt"
    const response = await fetch(url,{method:"GET",headers: {'Content-Type': 'application/json'},})
    return response.json()
}

document.addEventListener("keydown",function(e){
    if(e.key === "Backspace" || e.key === "Delete"){
        if(correctLetters[guessIndex-1] || shownHints[guessIndex-1]){
            while((correctLetters[guessIndex-1] || shownHints[guessIndex-1]) && (guessIndex != 0)){
                guessIndex -=1
                console.log("Subtracted")
            }
        } else{
            if(guessIndex > 0) guessIndex -= 1
        }

        if((correctLetters[guessIndex] != void 0 || shownHints[guessIndex] != void 0) && guessIndex > 0){
            guessIndex-=1
        }

        console.log(guessIndex)
        guess = guess.slice(0,guessIndex)
        
        if(!correctLetters[guessIndex] && !shownHints[guessIndex]) selectedSpace = guessIndex
        if(correctLetters[guessIndex-1] || shownHints[guessIndex-1]){
            while((correctLetters[guessIndex-1] || shownHints[guessIndex-1]) && (guessIndex != 0)){
                guessIndex -=1
                console.log("Subtracted")
            }
        }
    } else if (e.key == "Enter"){
        if(guess.length != n + 1 || guess.includes(undefined)) return;
        checkGuess()
    }else if(((e.keyCode >= 97 && e.keyCode <= 122) || (e.keyCode >= 65 && e.keyCode <= 90))){
        if((correctLetters[guessIndex] || shownHints[guessIndex])){
            while((correctLetters[guessIndex] || shownHints[guessIndex]) && (guessIndex != n)){
                guessIndex+=1
            }
        }
        guess[guessIndex] = e.key
        if(guessIndex != n+1) guessIndex+=1
        while((correctLetters[guessIndex] || shownHints[guessIndex]) && (guessIndex != n)){
            guessIndex+=1
        }
        selectedSpace = guessIndex
    }
    guess = guess.slice(0,n+1)
    for(var i = 0;i < correctLetters.Positions.length;i++){
        guess[correctLetters.Positions[i]] = prompt.replace(" ","")[correctLetters.Positions[i]]
    }
    for(var i = 0;i < shownHints.Positions.length;i++){
        guess[shownHints.Positions[i]] = prompt.replace(" ","")[shownHints.Positions[i]]
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
        for(var i = 0;i<n;i++){
            console.log()
            if((!correctLetters[i] && !shownHints[i])){
                guessIndex = i
                selectedSpace = i
                break
            }
        }
    }
}