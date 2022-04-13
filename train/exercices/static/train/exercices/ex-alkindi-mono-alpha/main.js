
function random_char_id () {
    let idx = Math.floor(Math.random() * 26) % 26

    return idx
}

function get_frequencies (text) {
    let frequencies = {};
    const DEFAULT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for (let idx = 0; idx < DEFAULT.length; idx ++)
        frequencies[DEFAULT[idx]] = 0
    console.log(text)
    for (let idx = 0; idx < text.length; idx ++) {
        frequencies[text[idx]] += 1;
    }

    return frequencies
}

function get_permutations () {
    let array = []
    for (let idx = 0; idx < 26; idx ++)
        array.push(false)
    
    let permutations = {}
    for (let idx = 0; idx < 26; idx ++) {
        let char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[idx];

        let random_char = random_char_id()
        while (array[random_char])
            random_char = random_char_id()
        
        let real_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random_char];
        permutations[char] = real_char
        array[random_char] = true;
    }

    return permutations
}

function encrypt ( text, permutations ) {
    return Array.from(text).map( ( chr ) => permutations[chr] ).join("")
}

EXERCICE_PLAYER.register ( 'alkindi-mono-alpha', function generator ( html ) {
    const API_URL = "/api/v1/train/exercices/markov/default"

    let response = { html }
    let query = fetch('/api/v1/train/exercices/markov/default')
    
    query.then((body) => {
        console.log('RECEIVED')
        let second_query = body.json()
        response.second_query = second_query
        
        second_query.then((text) => {
            console.log('CHANGED')
            response.text = text
        })
    })

    response.query = query

    return response
}, async function show_exercice ( exercice ) {
    await exercice.query;
    await exercice.second_query;

    const text = exercice.text.data;

    const permutations = get_permutations()
    const encrypted = encrypt( text, permutations);
    
    const french_frequencies = ["E", "A", "S", "I", "N", "T", "R", "L", "U", "O", "D", "C", "P", "M", "V", "G", "F", "B", "Q", "H", "X", "J", "Y", "Z", "K", "W"]
    const frequencies = get_frequencies(encrypted)

    let keys = Object.keys(frequencies)
    let sorted_frequencies = []
    for (let idx = 0; idx < keys.length; idx ++) {
        sorted_frequencies.push([ frequencies[keys[idx]], keys[idx] ])
    }

    sorted_frequencies = sorted_frequencies.sort(function compare (a, b) {
        return b[0] - a[0];
    })

    const container = EXERCICE_PLAYER.get_exercice_container()
    //generation du html
    let html = '<div class="flex flex-wrap w-fit relative center-w mt-16">'

    for(i=0;i<sorted_frequencies.length;i++) {
        let object = sorted_frequencies[i]
        html+=`<div class="w-8">
        <div class="h-[70px] relative w-8">
            <div class="absolute w-4 bg-black bottom-0" style="height:`+object[0]/2+"px"+`;max-height:60px;"></div>
        </div>
        <p>`+object[1]+`</p>
        <p>`+object[0]+`</p>
        <input maxlength="1" class='w-6 p-0 m-0' id='freq`+i+`' name="`+object[1]+`" type='text'>
        <p>`+french_frequencies[i]+`</p>
    </div>`
    }
    html+="</div>"
    html+=`<br>
    <br>
    <div class="flex flex-wrap w-fit relative center-w max-h-[45vh] overflow-y-auto max-w-[1000px]">`
    for(let idx =0;idx<encrypted.length;idx++){
        let chr = encrypted[idx]
        html+=`
        <div class="w-7">
            <p class='opacity-50 text-center'>`+chr+`</p>
            <input
             name="`+chr+`" 
             class='w-6 p-0 m-0' 
             id='input`+idx+`' 
             type='text'>
        </div>`
                    }
                    html+=`
    </div>
    
    
    <br>
    <div class="center-w relative w-fit">
    <input type="button" class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded" value="Passer l'exercice">
    <input type="button" class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded" value="Valider">
    <input type='button' class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded" value="Reinitialiser">
    </div>
    <br>
    <p class="center-w relative w-fit" id="sol"></p>`
    container.innerHTML=html;
    //generation du javascript
    var indices=false;
    var longueur=encrypted.length;
    function f(letter,correction){
        for(var i=0;i<longueur;i++){
            id="input"+i;
            a=document.getElementById(id);
            if(a.name==letter){
                a.value=correction
            }
        }
    }
    function reinit(){
        document.getElementById("sol").innerHTML='';
        for(var i=0;i<longueur;i++){
            id="input"+i;
            a=document.getElementById(id);
            a.value=''
        }
        for(var i=0;i<26;i++){
            id="freq"+i;
            a=document.getElementById(id);
            a.value=''
        }
    }
    var so=text;
    function sol(){
        indices=true;
        for(var i=0;i<longueur;i++){
            id="input"+i;
            a=document.getElementById(id);
            if(a.value==so[i].toUpperCase()){
                continue;
            }
            else if(a.value.length==0){
                a.value=so[i].toUpperCase()
            }
            else{
                a.value=so[i].toUpperCase()
                a.style.backgroundColor="#ff0000"
            }
        }
    }
    function colorier(letter){
        for(var i=0;i<longueur;i++){
            id="input"+i;
            a=document.getElementById(id);
            if(a.name==letter){
                a.style.backgroundColor='#aaaaaa'
            }
            else if(a.style.backgroundColor=="rgb(255, 0, 0)"){
                continue;
            }
            else{
                a.style.backgroundColor='white'
            }
        }
    }
    function valider(){
        for(var i=0;i<longueur;i++){
            id="input"+i;
            a=document.getElementById(id);
            if(a.value!=so[i].toUpperCase()){
                return false
            }
        }
        return true
    }
    function verifier(value,ok){
        if(value==""){
            return;
        }
        for(var i=0;i<26;i++){
            id="freq"+i;
            a=document.getElementById(id);
            if(id==ok){
                a.style.backgroundColor="white"
                continue;
            }
            if(a.value==value){
                a.style.backgroundColor="#ff0000"
            }
            else{
                a.style.backgroundColor="white"
            }
        }
    }
    
    
}, async function show_solution ( exercice ) {

});

