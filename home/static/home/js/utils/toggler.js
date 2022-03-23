

/**
 * Toggle API
 * 
 * @author {LFA}
 * 
 * @query [toggle]
 * 
 * @onclick
 *   @param [<for>] : target that needs to be toggled
 *   @subquery [inner-button] : buttons that will be toggled and represent state of the container 
 */

window.addEventListener('DOMContentLoaded', function (event) {
    document.querySelectorAll('[toggle]').forEach((el) => {
        el.onclick = (ev) => {
            document.querySelectorAll(el.getAttribute('for')).forEach((container) => {
                container.classList.toggle('hidden')
            })

            el.querySelectorAll('[inner-button]').forEach((container) => {
                container.classList.toggle('hidden')
            })
        }
    })
})

