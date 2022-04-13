

const EXERCICE_PLAYER = {
    'register': function (exercice_name, generator, show_exercice, show_solution) {
        let exercice_id = EXERCICE_PLAYER.ID_BY_NAME[exercice_name]

        EXERCICE_PLAYER.GENERATOR_BY_ID[exercice_id] = generator
        EXERCICE_PLAYER.EXE_SHOWER_BY_ID[exercice_id] = show_exercice
        EXERCICE_PLAYER.SOL_SHOWER_BY_ID[exercice_id] = show_solution

        if (EXERCICE_PLAYER.start_queue.length > 0 
            && EXERCICE_PLAYER.timer == 0 
            && EXERCICE_PLAYER.start_queue[0][0] == exercice_id 
            && !EXERCICE_PLAYER.started)
            EXERCICE_PLAYER.next_exercice()
    },

    'start_registration': function (exercice_id) {
        if (EXERCICE_PLAYER.REGISTRATION.has(exercice_id)) return ;
        EXERCICE_PLAYER.REGISTRATION.add(exercice_id)

        fetch (`/train/exercice/data/${exercice_id}?metadata=`).then(body => {
            body.json().then ( json => {
                EXERCICE_PLAYER.ID_BY_NAME[json.data.slug] = exercice_id
                EXERCICE_PLAYER.EXE_DATA_BY_ID[exercice_id] = json.data

                fetch(`/train/exercice/data/${exercice_id}`).then(body => {
                    body.text().then ( text => {
                        EXERCICE_PLAYER.SHOWTEXT_BY_ID[exercice_id] = text

                        let script = document.createElement('script')
                        script.src = json.data.scriptstatic.startsWith('/') 
                            ?'/static' : '/static/' 
                            + json.data.scriptstatic;

                        document.body.appendChild(script)
                    })
                })
            } )
        })
    },

    'get_exercice_container': function () {
        return document.getElementById('exercice-container')
    },

    'add_exercice': function (metadata) {
        EXERCICE_PLAYER.start_registration(metadata.exercice)
        EXERCICE_PLAYER.start_queue.push([metadata.exercice, metadata.minutes, metadata.seconds])
    },
    'current_exercice': { timer_direction: 0 },
    'next_exercice': function () {
        EXERCICE_PLAYER.current_exercice.timer = EXERCICE_PLAYER.timer

        EXERCICE_PLAYER.started = EXERCICE_PLAYER.start_queue.length != 0
        if (EXERCICE_PLAYER.started) {
            let exercice = EXERCICE_PLAYER.start_queue[0]
            EXERCICE_PLAYER.current_exercice = exercice
            EXERCICE_PLAYER.start_queue.splice(0, 1)

            let exercice_id = exercice[0]
            EXERCICE_PLAYER.timer = 60 * exercice[1] + exercice[2]
            if (EXERCICE_PLAYER.EXE_DATA_BY_ID[exercice_id].timer_direction == 1)
                EXERCICE_PLAYER.timer = 0;

            let generator = EXERCICE_PLAYER.GENERATOR_BY_ID[exercice_id]
            let generated = generator(EXERCICE_PLAYER.SHOWTEXT_BY_ID[exercice_id])

            exercice.push(generated)

            EXERCICE_PLAYER.finished_queue.push(exercice)

            EXERCICE_PLAYER.EXE_SHOWER_BY_ID[exercice_id](generated)

            let length = EXERCICE_PLAYER.start_queue.length + EXERCICE_PLAYER.finished_queue.length;
            let finished = length - EXERCICE_PLAYER.start_queue.length
            document.getElementById('remaining-number').innerHTML = "(" + finished + " / " + length + ")"
        } else {
            document.getElementById('prev-solution').classList.remove('hidden')
            document.getElementById('next-solution').classList.remove('hidden')

            EXERCICE_PLAYER.show_solution()
        }
    },
    'finished_queue': [],
    'start_queue': [],
    'started': false,

    'solution_id': 0,
    'show_solution': function() {
        if (EXERCICE_PLAYER.solution_id < 0) EXERCICE_PLAYER.solution_id = EXERCICE_PLAYER.finished_queue.length - 1
        if (EXERCICE_PLAYER.solution_id >= EXERCICE_PLAYER.finished_queue.length) EXERCICE_PLAYER.solution_id = 0

        let exercice = EXERCICE_PLAYER.finished_queue[EXERCICE_PLAYER.solution_id]
        let exercice_id = exercice[0]

        EXERCICE_PLAYER.SOL_SHOWER_BY_ID[exercice_id](exercice[3])
        
        let length = EXERCICE_PLAYER.finished_queue.length;
        let finished = EXERCICE_PLAYER.solution_id + 1
        document.getElementById('remaining-number').innerHTML = "(" + finished + " / " + length + ")"
    },

    'timer': 0,

    'timer_interval': setInterval(() => {
        EXERCICE_PLAYER.timer += EXERCICE_PLAYER.EXE_DATA_BY_ID[EXERCICE_PLAYER.current_exercice[0]].timer_direction
        if (EXERCICE_PLAYER.timer < 0) {
            EXERCICE_PLAYER.timer = 0
            
            if (EXERCICE_PLAYER.started)
                EXERCICE_PLAYER.next_exercice()
        }

        let seconds = EXERCICE_PLAYER.timer % 60;
        let minutes = Math.round((EXERCICE_PLAYER.timer - seconds) / 60)

        let text = (minutes >= 10 ? minutes : '0' + minutes) + ':' + (seconds >= 10 ? seconds : '0' + seconds)
        
        document.getElementById('chrono').innerHTML = text
    }, 1000),

    'REGISTRATION': new Set(),

    'ID_BY_NAME': {},
    'SHOWTEXT_BY_ID': {},

    'GENERATOR_BY_ID': {},
    'EXE_SHOWER_BY_ID': {},
    'SOL_SHOWER_BY_ID': {},

    'EXE_DATA_BY_ID': {},
}

document.addEventListener('DOMContentLoaded', () => {
    for (let idx = 0; idx < METADATA.length; idx ++) {
        EXERCICE_PLAYER.add_exercice(METADATA[idx])
    }

    document.getElementById('prev-solution').onclick = (ev) => {
        EXERCICE_PLAYER.solution_id -= 1
        EXERCICE_PLAYER.show_solution()
    }
    document.getElementById('next-solution').onclick = (ev) => {
        EXERCICE_PLAYER.solution_id += 1
        EXERCICE_PLAYER.show_solution()
    }
})

