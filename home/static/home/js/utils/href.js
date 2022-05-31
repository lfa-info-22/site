

const HREF_API = () => {
    document.querySelectorAll("[href]").forEach((el) => {
        el.onclick = (ev) => {
            document.location.assign(el.getAttribute("href"))
        }
    })
}

document.addEventListener("DOMContentLoaded", HREF_API)
document.addEventListener("DOMSubtreeModified", HREF_API)
