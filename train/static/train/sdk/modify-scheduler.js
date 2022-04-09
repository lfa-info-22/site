

document.addEventListener('DOMContentLoaded', () => {
    // TODO add request queue
    let request_queue = []
    let request_idx = 0
    let processing_query = false

    function process () {
        if (request_queue.length == request_idx) {
            request_queue = []
            request_idx = 0
            processing_query = false
            console.log("Finished processing")
            return ;
        }
        processing_query = true;

        fetch (request_queue[request_idx]).then(( resp ) => {
            request_idx += 1
            process()
        })
    }

    document.querySelectorAll('div[input]').forEach((element) => {
        let input = element.querySelector('input')
        
        input.addEventListener('input', (event) => {
            request_queue.push(element.getAttribute('for') + '?' + element.getAttribute('ref') + '=' + (input.value.trim() == "" ? element.getAttribute("default") : input.value))
            if (!processing_query) process()
        })
    })
});


