

const EXERCICE_PLAYER = {
    'register': function (exercice_name, generator, show_exercice, show_solution) {
        let exercice_id = EXERCICE_PLAYER.ID_BY_NAME[exercice_name]

        EXERCICE_PLAYER.GENERATOR_BY_ID[exercice_id] = generator
        EXERCICE_PLAYER.EXE_SHOWER_BY_ID[exercice_id] = show_exercice
        EXERCICE_PLAYER.SOL_SHOWER_BY_ID[exercice_id] = show_solution
    },

    'start_registration': function (exercice_id) {
        if (EXERCICE_PLAYER.REGISTRATION.has(exercice_id)) return ;
        EXERCICE_PLAYER.REGISTRATION.add(exercice_id)

        fetch (`/train/exercice/data/${exercice_id}?metadata=`).then(body => {
            body.json().then ( json => {
                EXERCICE_PLAYER.ID_BY_NAME[json.data.slug] = exercice_id

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

    'REGISTRATION': new Set(),

    'ID_BY_NAME': {},
    'SHOWTEXT_BY_ID': {},

    'GENERATOR_BY_ID': {},
    'EXE_SHOWER_BY_ID': {},
    'SOL_SHOWER_BY_ID': {},
}

