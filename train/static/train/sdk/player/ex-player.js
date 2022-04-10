

const EXERCICE_PLAYER = {
    'register': function (exercice_name, generator, show_exercice, show_solution) {

    },

    'start_registration': function (exercice_id) {
        fetch (`/train/exercice/data/${exercice_id}?metadata=`).then(body => {
            body.json().then ( json => {
                EXERCICE_PLAYER.ID_BY_NAME[json.data.slug] = exercice_id

                fetch(`/train/exercice/data/${exercice_id}`).then(body => {
                    body.text().then ( text => {
                        console.log(text)
                    })
                })
            } )
        })
    },

    'ID_BY_NAME': {}
}

