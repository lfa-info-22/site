/**
 * Select API
 * 
 * @query [type=select]
 * 
 * @subquery button[role=toggler]
 * 
 * @subquery ul[role=option-list]
 * 
 * @subquery li>span:not(.hidden)
 */


const SELECT_API = function(ev){
    
    let select_areas = document.querySelectorAll('div[type=select]')

    for (let idx = 0; idx < select_areas.length; idx ++) {
        let select_area = select_areas[idx]

        let toggler_button = select_area.querySelector('button[role=toggler]')

        let option_ul = select_area.querySelector('ul[role=option-list]')

        toggler_button.onclick = (ev) => option_ul.classList.toggle('hidden')

        let possibilities = option_ul.querySelectorAll('li[role=option]')

        for (let jdx = 0; jdx < possibilities.length; jdx ++) {
            possibilities[jdx].onclick = (ev) => {
                option_ul.querySelectorAll('li>span:not(.hidden)').forEach((el) => el.classList.add('hidden'))
                
                let target = ev.target
                while (target.nodeName != 'LI') target = target.parentNode
                select_area.querySelector("input[type=hidden]").value = target.getAttribute("value")

                target.querySelector('span.text-indigo-600').classList.remove('hidden')

                toggler_button.querySelector('span>span').innerHTML = target.querySelector('div.flex>span').innerHTML

                let event = new CustomEvent('input', 
                    {
                        bubbles: true,
                        detail: {
                            value: toggler_button.querySelector('span>span').innerText.trim()
                        }
                    }
                )
                select_area.dispatchEvent(event);
            }
        }

        select_area.setValue = (value) => {
            let possibilities = option_ul.querySelectorAll('li')
            let possibility = undefined

            for (let jdx = 0; jdx < possibilities.length; jdx ++) {
                if (possibilities[jdx].querySelector('div>span').innerText.trim() == value) {
                    possibility = possibilities[jdx]
                    break;
                }
            }

            if (!possibility) return;

            option_ul.querySelectorAll('li>span:not(.hidden)').forEach((el) => el.classList.add('hidden'))
            
            possibility.querySelector('span.text-indigo-600').classList.remove('hidden')

            toggler_button.querySelector('span>span').innerHTML = possibility.querySelector('div.flex>span').innerHTML
            select_area.querySelector("input[type=hidden]").value = possibility.getAttribute("value")

            let event = new CustomEvent('input', 
                {
                    bubbles: true,
                    detail: {
                        value: toggler_button.querySelector('span>span').innerText
                    }
                }
            )
            select_area.dispatchEvent(event);
        }
    }

}

 document.addEventListener('DOMSubtreeModified', SELECT_API);
 document.addEventListener('DOMContentLoaded', SELECT_API);