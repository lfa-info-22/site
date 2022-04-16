
function random_char_id() {
    let idx = Math.floor(Math.random() * 26) % 26

    return idx
}

function get_frequencies(text) {
    let frequencies = {};
    const DEFAULT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for (let idx = 0; idx < DEFAULT.length; idx++)
        frequencies[DEFAULT[idx]] = 0
    console.log(text)
    for (let idx = 0; idx < text.length; idx++) {
        frequencies[text[idx]] += 1;
    }

    return frequencies
}

function get_permutations() {
    let array = []
    for (let idx = 0; idx < 26; idx++)
        array.push(false)

    let permutations = {}
    for (let idx = 0; idx < 26; idx++) {
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

function encrypt(text, permutations) {
    return Array.from(text).map((chr) => permutations[chr]).join("")
}

EXERCICE_PLAYER.register('alkindi-mono-alpha', function generator(html) {
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
}, function show_exercice(exercice) {
    await exercice.query;
    await exercice.second_query;

    const text = exercice.text.data;
    console.log(text)
    const permutations = get_permutations()
    const encrypted = encrypt(text, permutations);
    exercice.encrypted = encrypted
    const french_frequencies = ["E", "A", "S", "I", "N", "T", "R", "L", "U", "O", "D", "C", "P", "M", "V", "G", "F", "B", "Q", "H", "X", "J", "Y", "Z", "K", "W"]
    const frequencies = get_frequencies(encrypted)

    let keys = Object.keys(frequencies)
    let sorted_frequencies = []
    for (let idx = 0; idx < keys.length; idx++) {
        sorted_frequencies.push([frequencies[keys[idx]], keys[idx]])
    }

    sorted_frequencies = sorted_frequencies.sort(function compare(a, b) {
        return b[0] - a[0];
    })

    const container = EXERCICE_PLAYER.get_exercice_container()
    //generation du html
    let html = `
    <div class="text-center p-4 mb-4">
    <div class="text-3xl flex">
        <div class="flex-1"></div>
        Chiffrement mono-alphabétique
        <div class="text-gray-400 pl-4" id="remaining-number"></div>
        <div class="flex-1"></div>
    </div>
</div><div class="flex flex-wrap w-fit relative center-w mt-2">`

    for (i = 0; i < sorted_frequencies.length; i++) {
        let object = sorted_frequencies[i]
        html += `<div class="w-8">
        <div class="h-[70px] relative w-8">
            <div class="absolute w-4 bg-black bottom-0" style="height:`+ object[0] / 2 + "px" + `;max-height:60px;"></div>
        </div>
        <p>`+ object[1] + `</p>
        <p>`+ object[0] + `</p>
        <input maxlength="1" class='w-6 p-0 m-0' id='freq`+ i + `' name="` + object[1] + `" type='text'>
        <p>`+ french_frequencies[i] + `</p>
    </div>`
    }
    html += "</div>"
    html += `<br>
    <br>
    <div class="flex flex-wrap w-fit relative center-w max-h-[45vh] overflow-y-auto max-w-[1000px]">`
    for (let idx = 0; idx < encrypted.length; idx++) {
        let chr = encrypted[idx]
        html += `
        <div class="w-7">
            <p class='opacity-50 text-center'>`+ chr + `</p>
            <input
             name="`+ chr + `" 
             class='w-6 p-0 m-0' 
             id='input`+ idx + `' 
             type='text'>
        </div>`
    }
    html += `
    </div>
    
    
    <br>
    <div class="center-w relative w-fit">
    <input type="button" class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded" id="pass" value="Passer l'exercice">
    <input type="button" class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded" id="fini" value="Valider">
    <input type='button' class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded" id="reinit" value="Reinitialiser">
    </div>
    <br>
    <p class="center-w relative w-fit" id="sol"></p>`
    container.innerHTML = html;
    //generation du javascript
    var indices = false;
    var longueur = encrypted.length;
    function f(letter, correction) {
        for (var i = 0; i < longueur; i++) {
            id = "input" + i;
            a = document.getElementById(id);
            if (a.name == letter) {
                a.value = correction
            }
        }
    }
    function reinit() {
        document.getElementById("sol").innerHTML = '';
        for (var i = 0; i < longueur; i++) {
            id = "input" + i;
            a = document.getElementById(id);
            a.value = ''
        }
        for (var i = 0; i < 26; i++) {
            id = "freq" + i;
            a = document.getElementById(id);
            a.value = ''
        }
    }
    var so = text;
    function colorier(letter) {
        for (var i = 0; i < longueur; i++) {
            id = "input" + i;
            a = document.getElementById(id);
            if (a.name == letter) {
                a.style.backgroundColor = '#aaaaaa'
            }
            else if (a.style.backgroundColor == "rgb(255, 0, 0)") {
                continue;
            }
            else {
                a.style.backgroundColor = 'white'
            }
        }
    }
    function valider() {
        for (var i = 0; i < longueur; i++) {
            id = "input" + i;
            a = document.getElementById(id);
            if (a.value != so[i].toUpperCase()) {
                return false
            }
        }
        return true
    }
    function verifier(value, ok) {
        if (value == "") {
            return;
        }
        for (var i = 0; i < 26; i++) {
            id = "freq" + i;
            a = document.getElementById(id);
            if (id == ok) {
                a.style.backgroundColor = "white"
                continue;
            }
            if (a.value == value) {
                a.style.backgroundColor = "#ff0000"
            }
            else {
                a.style.backgroundColor = "white"
            }
        }
    }
    for (let i = 0; i < sorted_frequencies.length; i++) {
        let object = sorted_frequencies[i]
        let element = document.getElementById("freq" + i)
        element.onclick = function (event) {
            colorier(object[1])
        }
        element.onfocus = function (event) {
            colorier(object[1])
        }
        element.oninput = function (event) {
            element.value = element.value.toUpperCase();
            if (element.value.length == 0 && Number(i) > 0) {
                document.getElementById(String("freq" + (i - 1))).focus()
            } else if (element.value.length == 0) {
                document.getElementById(String("freq" + (25))).focus()
            }
            if (element.value.length == 1) {
                verifier(element.value, "freq" + i);
                let a = document.getElementById(String("freq" + (i + 1) % 26));
                a.focus();
                colorier(a.name)
            };
            f(object[1], element.value);
        }
        element.onkeydown = function (event) {
            element.select();
            if (event.keyCode == 37 || event.keyCode == 39) {
                var el;
                if (event.keyCode == 37 && Number(i) > 0) {
                    el = document.getElementById(String("freq" + (Number(i) - 1)))
                } else if (event.keyCode == 37) {
                    el = document.getElementById(String("freq" + (25)))
                }
                if (event.keyCode == 39 && Number(i) < 25) {
                    el = document.getElementById(String("freq" + (Number(i) + 1)))
                } else if (event.keyCode == 39) {
                    el = document.getElementById(String("freq" + (0)))
                }
                el.focus();
            }
        }
    }
    for (let idx = 0; idx < encrypted.length; idx++) {
        let chr = encrypted[idx]
        let element = document.getElementById("input" + idx)
        element.oninput = function (event) {
            element.value = element.value.toUpperCase();
            let longueur = encrypted.length;
            if (element.value.length > 1) {
                element.value = element.value[1];
            };
            if (Number(idx) != Number(longueur) - 1 && element.value.length != 0) {
                document.getElementById(String("input" + (Number(idx) + 1))).focus()
            }
        }
    }
    //buttons
    document.getElementById("pass").onclick = function (event) {
        exercice.solved = false
        exercice.timer=EXERCICE_PLAYER.timer;
        EXERCICE_PLAYER.next_exercice();
    }
    document.getElementById("fini").onclick = function (event) {
        a = valider();
        if (a) {
            exercice.solved = true
            exercice.timer=EXERCICE_PLAYER.timer;
            EXERCICE_PLAYER.next_exercice();
        }
        else {
            document.getElementById("sol").innerHTML = "Dommage, essaie encore"
        }

    }
    document.getElementById("reinit").onclick = function (event) {
        reinit();
    }

}, async function show_solution(exercice) {
    let container = EXERCICE_PLAYER.get_exercice_container();
    EXERCICE_PLAYER.timer=exercice.timer;
    container.innerHTMl = ""
    let html = `
    <div class="text-center p-4 mb-4">
    <div class="text-3xl flex">
        <div class="flex-1"></div>
        Chiffrement mono-alphabétique
        <div class="text-gray-400 pl-4" id="remaining-number"></div>
        <div class="flex-1"></div>
    </div>
</div>
<div class='flex'>`
    if (exercice.solved == true) {
        html += `
    <div class="flex flex-wrap w-fit relative ml-16 max-h-[70vh] overflow-y-auto max-w-[1000px] flex-1">`
        for (let idx = 0; idx < exercice.text.data.length; idx++) {
            let chr = exercice.text.data[idx]
            html += `
        <div class="w-7">
            <p class='opacity-50 text-center'>`+ exercice.encrypted[idx] + `</p>
            <input disabled
             name="`+ chr + `" 
             class='w-6 p-0 m-0' 
             id='input`+ idx + `' 
             type='text' value='`+ chr + `'>
        </div>`
        }
        html += `
    </div>`
    html += `<div class='flex-1'>
        <div class="p-3 px-6 flex bg-emerald-200 text-emerald-700 rounded-md m-4 mr-8 w-auto">
            <div class="material-icons-outlined">check</div>
            <div class="ml-4">Bravo, tu as réussi !</div>
        </div>
        <div class="p-3 px-6 flex bg-sky-200 text-sky-700 rounded-md m-4 mr-8">
            <div class="material-icons-outlined">info</div>
            <div class="ml-4"><b>Introduction : </b> En français, les lettres ne sont pas toutes aussi fréquentes. Si le <b>E</b> est la lettre la plus fréquente avec près de 15% des lettres présentes en français, ce n'est pas le cas pour toutes les lettres. En effet, d'autres lettres comme le <b>W</b>, le <b>X</b> ou encore le <b>K</b> sont beaucoup moins présentes avec une fréquence aux alentours de 0.2%. On peut ainsi dresser la liste des fréquences auxquelles les lettres apparaissent en français, et comparer cette liste avec les fréquences obtenues dans le texte. Cette analyse, dite analyse de fréquences, est très efficace, mais le devient de plus en plus si le texte est long. Ici malheuresement, le texte n'est pas suffisament long pour avoir une analyse fréquentielle précise mais celle-ci nous donne une idée de la position des lettres tout de même.
            </div>
        </div>
        <div class="p-3 mb-2 text-lg mr-8">Il faut donc réussir à placer les lettres en fonction de leur fréquences tout en veillant à ce que le texte ait un sens.
      <br>  Pour ce faire, nous pouvons dans un premier temps placer la lettre <b>E</b> à coup sur en raison de sa fréquence très distincte du <b>S</b>. Ensuite, il faut faire en sort de respecter les règles du français telles que la non-succession de deux <b>A</b> ou <b>I</b> ou encore la lettre <b>Q</b> toujours suivie par un <b>U</b>. 
       <br> Ainsi, il est possible de connaître la position d'un certain nombre de lettres, et il faut reconnaître les mots à partir de celles-ci.
       <br> Cet exercice est cependant extrêmement difficile, surtout au vu de la longueur du texte, et il est donc normal que vous n'ayez pas réussi ou fait un temps qui peut vous sembler énorme. Si vous avez réussi, vous êtes déjà des experts en cryptographie !</div>
        </div>
        </div>`
    container.innerHTML = html
    }
    else {
        html += `<br>
    <br>
    <div class="flex flex-wrap w-fit relative ml-16 max-h-[70vh] overflow-y-auto max-w-[1000px] flex-1">`
        for (let idx = 0; idx < exercice.text.data.length; idx++) {
            let chr = exercice.text.data[idx]
            html += `
        <div class="w-7">
            <p class='opacity-50 text-center'>`+ exercice.encrypted[idx] + `</p>
            <input disabled
             name="`+ chr + `" 
             class='w-6 p-0 m-0' 
             id='input`+ idx + `' 
             type='text' value='`+ chr + `'>
        </div>`
        }
        html += `
    </div>`
        html += `<div class='flex-1'>
        <div class="p-3 px-6 flex bg-red-200 text-red-700 rounded-md m-4 mr-8 w-auto">
            <div class="material-icons-outlined">cancel</div>
            <div class="ml-4">Dommage, tu t'es trompé</div>
        </div>
        <div class="p-3 px-6 flex bg-sky-200 text-sky-700 rounded-md m-4 mr-8">
            <div class="material-icons-outlined">info</div>
            <div class="ml-4"><b>Introduction : </b> En français, les lettres ne sont pas toutes aussi fréquentes. Si le <b>E</b> est la lettre la plus fréquente avec près de 15% des lettres présentes en français, ce n'est pas le cas pour toutes les lettres. En effet, d'autres lettres comme le <b>W</b>, le <b>X</b> ou encore le <b>K</b> sont beaucoup moins présentes avec une fréquence aux alentours de 0.2%. On peut ainsi dresser la liste des fréquences auxquelles les lettres apparaissent en français, et comparer cette liste avec les fréquences obtenues dans le texte. Cette analyse, dite analyse de fréquences, est très efficace, mais le devient de plus en plus si le texte est long. Ici malheuresement, le texte n'est pas suffisament long pour avoir une analyse fréquentielle précise mais celle-ci nous donne une idée de la position des lettres tout de même.
            </div>
        </div>
        <div class="p-3 mb-2 text-lg mr-8">Il faut donc réussir à placer les lettres en fonction de leur fréquences tout en veillant à ce que le texte ait un sens.
      <br>  Pour ce faire, nous pouvons dans un premier temps placer la lettre <b>E</b> à coup sur en raison de sa fréquence très distincte du <b>S</b>. Ensuite, il faut faire en sort de respecter les règles du français telles que la non-succession de deux <b>A</b> ou <b>I</b> ou encore la lettre <b>Q</b> toujours suivie par un <b>U</b>. 
       <br> Ainsi, il est possible de connaître la position d'un certain nombre de lettres, et il faut reconnaître les mots à partir de celles-ci.
       <br> Cet exercice est cependant extrêmement difficile, surtout au vu de la longueur du texte, et il est donc normal que vous n'ayez pas réussi ou fait un temps qui peut vous sembler énorme. Si vous avez réussi, vous êtes déjà des experts en cryptographie !</div>
        </div>
        </div>`
        container.innerHTML = html;
    }
});
