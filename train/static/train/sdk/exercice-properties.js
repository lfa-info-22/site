
EXERCICE_PROPERTIES_SDK__current_exercice = undefined;
EXERCICE_PROPERTIES_SDK__current_id = -1;

function EXERCICE_PROPERTIES_SDK () {

    document.querySelectorAll('[properties-close]').forEach((button) => {
        button.onclick = (ev) => {
            let target = ev.target
            
            while (!target.hasAttribute('properties')) target = target.parentNode;

            target.classList.add('hidden')
        }
    })

    document.querySelectorAll('[exercice]').forEach((button) => {
        button.onclick = (ev) => {
            EXERCICE_PROPERTIES_SDK__current_exercice = button
            EXERCICE_PROPERTIES_SDK__current_id = button.getAttribute('exercice-id')

            document.querySelectorAll('[properties]').forEach((element) => {
                element.classList.remove('hidden')
                element.querySelector('[properties-name]').innerHTML = button.querySelector('[exercice-name]').innerHTML
            })
        }
    })

    document.querySelectorAll('[properties-add]').forEach((button) => {
        button.onclick = (ev) => {
            if (EXERCICE_PROPERTIES_SDK__current_id == -1) return ;

            let target = ev.target;
            while (!target.hasAttribute('properties')) target = target.parentNode

            let select = target.querySelector('[properties-choice]')
            let select_value = select.querySelector('input[type=hidden]').value

            if (select_value == "") return;
            
            const URL = `/api/v1/train/create/scheduler/${select_value}/exercice/${EXERCICE_PROPERTIES_SDK__current_id}`

            fetch(URL)
        }
    })
}

document.addEventListener('DOMContentLoaded', EXERCICE_PROPERTIES_SDK)
document.addEventListener('DOMSubtreeModified', EXERCICE_PROPERTIES_SDK)

