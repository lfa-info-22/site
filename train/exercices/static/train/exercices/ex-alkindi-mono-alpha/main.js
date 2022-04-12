
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
    
    const french_frequencies = ["E", "A", "S", "I", "N", "T", "R", "L", "U", "O", "D", "C", "P", "M", "V", "G", "F", "B", "Q", "H", "X", "J", "Y", "Z", "K", "W"]
    const frequencies = get_frequencies(text)

    let keys = Object.keys(frequencies)
    let sorted_frequencies = []
    for (let idx = 0; idx < keys.length; idx ++) {
        sorted_frequencies.push([ frequencies[keys[idx]], keys[idx] ])
    }

    sorted_frequencies = sorted_frequencies.sort(function compare (a, b) {
        return b[0] - a[0];
    })

    const permutations = get_permutations()
    console.log(permutations)

    const container = EXERCICE_PLAYER.get_exercice_container()

    let html = '<div class="flex flex-wrap w-fit relative center-w">'

    for(i=0;i<keys.length;i++) {
        let object = frequencies[keys[i]]
        html+=`<div class="w-8">
        <div class="h-[70px] relative w-8">
            <div class="absolute w-4 bg-black bottom-0" style="height:calc({{b}}px/2);max-height:60px;"></div>
        </div>
        <p>`+keys[i]+`</p>
        <p>`+object+`</p>
        <input maxlength="1" class='w-6 p-0 m-0' id='freq`+i+`' name="`+keys[i]+`">
        <p>`+french_frequencies[i]+`</p>
    </div>`
    }
    html+="</div>"
    container.innerHTML=html;
        /**
    {% with a=el.0 b=el.1 c=el.2 d=el.3 %}
    <div class="w-8">
        <div class="h-[70px] relative w-8">
            <div class="absolute w-4 bg-black bottom-0" style="height:calc({{b}}px/2);max-height:60px;"></div>
        </div>
        <p>{{a}}</p>
        <p>{{b}}</p>
        <input 
        maxlength="1"
        onclick='var a="{{a}}";colorier(a);' 
        class='w-6 p-0 m-0' 
        id='freq{{c}}' 
        oninput='javascript:this.value=this.value.toUpperCase();
        var j="{{c}}";var longueur="26";
        if(this.value.length==0 && Number(j)>0){
            document.getElementById(String("freq"+(Number(j)-1))).focus()
        } else if(this.value.length==0){
            document.getElementById(String("freq"+(25))).focus()
        }
        if(this.value.length==1){
            verifier(this.value,"freq"+j);
            a=document.getElementById(String("freq"+(Number(j)+1)%26));
            a.focus();
            colorier(a.name)
        };
        var a="{{a}}";
        f(a,this.value);' 
        type='text'
        onfocus='var a="{{a}}";colorier(a);'
        onkeydown='javascript:this.select();
        var i="{{c}}"
        if(event.keyCode==37 || event.keyCode==39){
            var el;
        if(event.keyCode==37 && Number(i)>0){
            el=document.getElementById(String("freq"+(Number(i)-1)))
        } else if(event.keyCode==37){
           el=document.getElementById(String("freq"+(25)))
        }
        if(event.keyCode==39 && Number(i)<25){
           el=document.getElementById(String("freq"+(Number(i)+1)))
        } else if(event.keyCode==39){
           el=document.getElementById(String("freq"+(0)))
        }
        el.focus();
    }' name="{{a}}">
        <p>{{d}}</p>
    </div>
{% endwith %}
    {% endfor %}
    

    var indices=false;
    var longueur=Number("{{longueur}}");
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
    var so="{{sol}}";
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








    */
    
    
}, async function show_solution ( exercice ) {

});

