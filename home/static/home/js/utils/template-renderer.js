/**
 * API List Template
 */

function map(a, b, c) {
    return Math.min(c, Math.max(a, b))
}
function isVisible(el) {
    const rect = el.getBoundingClientRect()
    
    return map(0, window.innerHeight, rect.top) != map(0, window.innerHeight, rect.top  + rect.height)
        && map(0, window.innerWidth, rect.left) != map(0, window.innerWidth,  rect.left + rect.width)
}

const ApiListTemplate = {
    "register": function (get_next, waiter, container, template, get_parameter=(json) => json.data) {
        let last = []
        let started = false;

        function check () {
            if (isVisible(waiter) && !started) {
                started = true;
                get_next(last, (json) => {
                    let data = get_parameter(json)
                    last = data

                    for (let idx = 0; idx < data.length; idx ++) {
                        let json = data[idx]
                        let keys = Object.keys(json)
                        let HTML = template.innerHTML
                        for (let i = 0; i < keys.length; i++) {
                            HTML = HTML.split(':' + keys[i] + ':').join(json[keys[i]])
                        }

                        let div = document.createElement('div')
                        div.innerHTML = HTML

                        container.appendChild(div)
                    }
                    started = false;
                })
            }
        }

        waiter.setAttribute("_winterval", setInterval(check, 100))
        check()
    }
}

Object.freeze(ApiListTemplate)