
document.addEventListener('DOMContentLoaded', () => {
    ApiListTemplate.register(
        function get_next( last, resolve ) {
            let ROUTE = '/api/v1/train/get/plan/all/'
            let last_seen = undefined;
            
            if (last.length != 0)
                last_seen = Math.min(...last.map((el) => el.id))
            
            if (last_seen != undefined && !isNaN(last_seen)) {
                ROUTE = ROUTE + '?last_seen=' + last_seen
            }

            fetch(ROUTE).then((body) => {
                body.json().then((json) => {
                    if (json.data.length == 0) {
                        document.querySelector('#waiter-container').classList.add('hidden')
                    } else {
                        resolve(json)
                    }
                })
            })
        }, document.querySelector('#waiter-container')
        , document.querySelector('#scheduler-container')
        , document.querySelector('#scheduler-template')
    )
})